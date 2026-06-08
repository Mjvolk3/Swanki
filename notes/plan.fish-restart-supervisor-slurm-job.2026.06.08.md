---
id: 0nd509oe4pl9hffokl7e7gl
title: 08
desc: ''
updated: 1780944114688
created: 1780944114688
---

## Context

The SLURM-native per-job path (`scripts/swanki_job.sbatch`) brings up a Fish Speech TTS server in-job via `apptainer exec --nv` on the single allocated GPU (lines 87-94), exports its port as `SWANKI_FISH_PORTS` (line 107), then runs swanki generation + delivery. Fish is launched **once**. There is no supervisor. When the in-job Fish dies mid-generation the port goes dead, swanki's TTS calls fail, and the job exits non-zero — generation never reaches DONE.

The observed failure is not a transient HTTP blip. Fish gets hard-killed mid-token (SIGKILL/SIGSEGV) after dozens of chunks, silently: no Python traceback, no CUDA OOM, no dmesg OOM-killer line, GPU VRAM flat at ~23-25GB, port simply stops answering. The three LONGEST chapters (CH04/05/07) failed all three batch runs; in the last batch all three died at the **same millisecond across three different GPUs** while CH03 completed at that instant — a shared/node-level kill event, not per-job VRAM flakiness. Root cause is still unknown; this plan makes the job **survive** the kill rather than diagnose it (crash instrumentation is added to feed later diagnosis).

Commit `0d95eaf` already added a client-side retry in `_tts_fish_speech` (`swanki/audio/_common.py`, lines 1003-1036): on `httpx.HTTPError` or non-200 it backs off and re-discovers a healthy server on the same port. That is **Layer 1** and is necessary but not sufficient — re-runs showed `retries=3` then still FAILED, because per-job Fish was launched once with no supervisor: the retry had **nothing to reconnect to**. This plan adds **Layer 2**: a restart-supervisor inside the sbatch (no new process, no daemon, no PID file) that respawns the dead Fish (~30s model reload) on the same port so the Layer-1 retry's re-discovery finds the fresh server and the run continues to DONE. The layers compose by the locked principle of commit `0d95eaf` — "keep the HTTP/server boundary, harden the client" — with Layer 2 respawning the server behind that boundary while the client retry reconnects across it. Plus crash-time instrumentation (exit code, dmesg tail, `nvidia-smi -q` Xid) appended to a job-scoped crash log.

## Relevant Files

| Path | Action | Purpose | Stance |
| --- | --- | --- | --- |
| `scripts/swanki_job.sbatch` | MODIFY | Add inline unified poll-loop supervisor around the generation step (line 128); export raised `SWANKI_FISH_TTS_ATTEMPTS`; crash-time capture | in-flux |
| `notes/scripts.swanki_job.md` | MODIFY | Append dated section documenting the supervisor (convention: ship rationale here) | in-flux |
| `swanki/audio/_common.py` | REFERENCE | Layer-1 client retry (`_tts_fish_speech` 1003-1036), discovery (`_discover_fish_speech_servers` 922-956), reference registration (`ensure_fish_speech_reference` 1039-1084). NOT edited — it is in-flux from today and owns the HTTP boundary | in-flux |
| `swanki/pipeline/pipeline.py` | REFERENCE | Calls `ensure_fish_speech_reference` ONCE at TTS setup (line 2159), not per-TTS — load-bearing for Open Question 1 | undocumented |
| `notes/swanki.audio._common.md` | REFERENCE | Layer-1 design note; its 2026.06.08 entry forward-references "swanki_job.sbatch needs a restart-supervisor (layer 2)" — this plan | in-flux |

## Key Design Decisions

1. **Supervisor is a single unified poll loop inside the sbatch, not a separate watcher process.** Background swanki (`swanki & ; swanki_pid=$!`) and poll every ~2-3s: `kill -0 "$swanki_pid"` (gone -> `wait` it, capture exit status, break) and `kill -0 "$fish_pid"` (gone -> capture crash, reap old PID, respawn same port, re-wait health, continue). Why one loop: a separate background watcher would need IPC to signal the main shell and could orphan swanki or the watcher itself on job teardown. One shell owning both PIDs is the simplest correct shape and keeps the EXIT/TERM/INT trap (line 96) authoritative. Rejected: a sidecar `bash watcher.sh &` process (extra teardown surface, no benefit); `wait -n` on both PIDs (can't re-arm cleanly after a Fish respawn changes `$fish_pid`).

2. **Trap keeps reading the shell variable `$fish_pid` by name; no PID file.** The trap `trap 'kill "$fish_pid" ...' EXIT TERM INT` is late-bound — it reads `$fish_pid` at fire time. Because one shell owns the variable, reassigning `fish_pid` after each respawn is automatically seen by the trap, so it always reaps the **current** Fish. Why not a PID file: it would be redundant state that could go stale and adds a read/write race for zero gain. Rejected: writing `$fish_pid` to `$QUEUE_DIR/fish.pid` and having the trap read the file.

3. **Supervisor stays INLINE in the sbatch — no `scripts/lib/`, no bats harness.** There is no bash test harness in the repo (Python tests only) and no `scripts/lib/` precedent. A bats harness could not exercise a real Fish/GPU crash anyway, so it would test mocks of the exact thing that matters. Keep the logic where the variables and trap already live. Rejected: extracting a `fish_supervisor.sh` library + bats tests (net-new infra, untestable core path).

4. **Gate behind `SWANKI_FISH_RESTART_ENABLED` (default ON); bound respawns with `SWANKI_FISH_MAX_RESTARTS` (default 3).** Default ON means the happy path is a no-op (Fish never dies -> loop just polls until swanki exits). The flag is a kill-switch for crash-loop debugging (set `=0` to get the old launch-once behavior and a fast failure). The bound prevents an infinite respawn loop from burning unlimited walltime on a node-level kill storm: on exceeding it, do a final crash capture and exit non-zero (stays resumable). Why default ON not OFF: the whole point is unattended batch runs surviving crashes; an opt-in flag would mean the next batch fails the same way. Rejected: unbounded respawns (walltime burn); default OFF (defeats the purpose).

5. **Do NOT edit the backoff tuple in `_common.py`; instead the sbatch EXPORTS a higher `SWANKI_FISH_TTS_ATTEMPTS` (~8) before launching swanki.** `_FISH_TTS_MAX_ATTEMPTS` reads that env (line 912, default 4) and the backoff tuple `(2,5,15,30)` clamps to its last value for attempts beyond index 3 (line 1024). With the default 4 attempts the client's total patience (~52s of sleeps plus up to 60s connect-timeout each) can be tight against a ~30-60s reload+coldstart racing the supervisor's respawn+health-wait. Raising attempts to ~8 stretches the client's reconnect window to comfortably outlast a respawn, with each extra attempt sleeping the clamped 30s. Why via env not code: `_common.py` is in-flux from today and owns the HTTP boundary; the SLURM path owns its own config. This also keeps the change to card/audio content at exactly zero. Rejected: editing `_FISH_TTS_BACKOFF_S` / the default in `_common.py` (touches shared code, would affect the live Docker-fleet path too).

6. **Only the GENERATION step (line 128) is wrapped; delivery (130-168) and the exit-75 Anki-deferred path stay outside the loop, untouched.** Per commit `4533c9c`, the supervisor matters only during generation — that is the only phase issuing TTS. Delivery is short, network-bound to Zotero/Anki/ABS, and not Fish-dependent. Wrapping it would entangle the resumable exit-75 semantics with respawn logic for no benefit. Rejected: a job-wide supervisor spanning delivery.

7. **Restructure line 128 into background + `wait`, preserving exit-1-on-failure under `pipefail`.** Today: `swanki "${args[@]}" || { echo ...; exit 1; }`. New shape: `swanki "${args[@]}" & ; swanki_pid=$!`, then the poll loop, and on swanki-exit `wait "$swanki_pid"; rc=$?` -> if non-zero, `echo ... >&2; exit 1`. `set -uo pipefail` is in effect (NOT `set -e`), so `wait` returning non-zero will not auto-exit — the explicit `exit 1` keeps the original semantics and the DONE-invariant (non-zero on unrecoverable failure -> resumable). Rejected: leaving line 128 foreground (cannot concurrently watch Fish).

## Approach

The change is confined to `scripts/swanki_job.sbatch` between the existing health-wait (line 106) and the generation call (line 128), plus turning line 128 into a backgrounded process the loop supervises.

**Factor the existing launch into a reusable shell function.** Lines 87-106 today launch Fish, set `fish_pid`, install the trap, and wait for `/v1/health`. Extract the launch+health-wait into a function (e.g. `start_fish`) so the supervisor can call the identical code path to respawn. The function reassigns the shell-global `fish_pid` (so the late-bound trap follows it) and returns non-zero if Fish never goes healthy within its own bounded timeout. The very first call replaces the current inline launch; respawns reuse it. Keep `apptainer exec` (NOT `instance start`) on respawn for the same reason as the initial launch (commit `8a1416d`: a daemon survives scancel and leaks ~22GB VRAM into the next job).

**Reaping before respawn must be complete, then reuse the SAME port.** Before respawning, kill the old `fish_pid` and `wait` on it so the process is fully gone and its socket released — the host port may sit in `TIME_WAIT` (EADDRINUSE) for ~30-60s if reaped sloppily. The supervisor reuses the same `$port` (it is already derived and exported as `SWANKI_FISH_PORTS`; changing it would desync the client). A brief settle `sleep` after the reap, before `apptainer exec`, avoids the bind race.

**The unified poll loop.** Gate the whole thing on `SWANKI_FISH_RESTART_ENABLED` (default 1); when 0, fall back to the foreground launch-once-and-fail behavior. When enabled, export `SWANKI_FISH_TTS_ATTEMPTS="${SWANKI_FISH_TTS_ATTEMPTS:-8}"` before launching swanki (honor a caller override). Launch swanki in the background, then loop:

```bash
restarts=0
while true; do
    if ! kill -0 "$swanki_pid" 2>/dev/null; then
        wait "$swanki_pid"; gen_rc=$?     # swanki finished — capture true rc
        break
    fi
    if ! kill -0 "$fish_pid" 2>/dev/null; then
        capture_fish_crash "$restarts"     # best-effort, never aborts
        wait "$fish_pid" 2>/dev/null        # fully reap, free the port
        restarts=$(( restarts + 1 ))
        if [ "$restarts" -gt "${SWANKI_FISH_MAX_RESTARTS:-3}" ]; then
            echo "ERROR: Fish exceeded max restarts ($restarts)" >&2
            capture_fish_crash "final"
            kill "$swanki_pid" 2>/dev/null
            exit 1
        fi
        sleep "${SWANKI_FISH_RESPAWN_SETTLE:-5}"
        start_fish || { echo "ERROR: respawned Fish never healthy" >&2; \
                        capture_fish_crash "respawn-unhealthy"; \
                        kill "$swanki_pid" 2>/dev/null; exit 1; }
    fi
    sleep "${SWANKI_FISH_POLL_S:-3}"
done
[ "$gen_rc" -eq 0 ] || { echo "ERROR: swanki generation failed (rc=$gen_rc)" >&2; exit 1; }
```

Note the subtlety guarded above: under `set -u` every `kill -0` is wrapped in `2>/dev/null` and an explicit `if !` (decision 2 + gotcha 1) so a transiently-missing PID never trips an unbound-variable or unexpected-exit edge. The `wait "$swanki_pid"` after the `kill -0` returns the process's real exit code (not the loop's), preserving the original `|| exit 1` contract (decision 7).

**Respawn re-health-checks with its OWN bounded timeout.** `start_fish` already curls `/v1/health` up to `SWANKI_FISH_HEALTH_TIMEOUT` (default 300, line 100). On respawn it reuses that bound; if the new Fish never goes healthy it returns non-zero and the loop gives up (counts against the bound, final crash capture, exit non-zero). Do NOT poll health forever inside walltime.

**Crash capture (`capture_fish_crash`).** Append a timestamped event block to `$QUEUE_DIR/logs/swanki-job-$SLURM_JOB_ID-fish-crash.log` (fall back to `/tmp/` if `$QUEUE_DIR/logs` is not writable — `$QUEUE_DIR` is under `$HOME`, not the 69%-full `/scratch`). Each event records: restart index, wall timestamp, the dead `fish_pid` and its exit status (from the `wait`), `dmesg | tail -n 50` (best-effort; fall back to `journalctl -k -n 50` or `/var/log/messages`), and `nvidia-smi -q | grep -iA3 xid` (unprivileged-OK) to catch GPU Xid errors. Every command in the capture is best-effort and the function always returns 0 — instrumentation must never abort the job (gotcha 9).

## Gotchas

1. **`set -uo pipefail` is in effect but NOT `set -e`.** Don't rely on auto-exit, and guard every `kill -0` with `2>/dev/null` inside an explicit `if !` so a missing PID under `set -u` neither errors nor silently mis-branches.
2. **The trap is late-bound on `$fish_pid` — keep one shell owning it.** Reassign `fish_pid` (don't `local`-scope it inside a subshell) on each respawn so the trap reaps the current Fish. A subshell or pipe segment would get a copy and break this.
3. **Wait-vs-poll deadlock.** Do NOT `wait "$swanki_pid"` as the loop's blocking primitive — it would block the shell so Fish death goes unwatched. Poll both with `kill -0` and only `wait` the swanki PID once `kill -0` already shows it gone (to harvest the exit code without blocking).
4. **Port reuse race (EADDRINUSE / TIME_WAIT).** Fully `wait`-reap the old `fish_pid` and `sleep` a few seconds before re-`exec` on the same port; the socket can linger ~30-60s otherwise. Same port (client targets `SWANKI_FISH_PORTS=$port`), `apptainer exec` not `instance start`.
5. **Client patience vs reload time.** Default 4 client attempts (~52s sleeps) can be tight against respawn+coldstart; exporting `SWANKI_FISH_TTS_ATTEMPTS=8` stretches the reconnect window. Verify the math holds against observed reload time during the smoke test (raise further if needed).
6. **`/v1/health` 200 may precede TTS-readiness.** The model can report healthy before it can serve a TTS request — see Open Question 2; a short post-health grace may be needed.
7. **SLURM is NOT cut over.** The live box still runs the Docker Fish fleet + bash drainer; `squeue --me` is empty. Editing `swanki_job.sbatch` does not disturb the running drainer, so this is safe to land, but it also cannot be smoke-tested against real SLURM scheduling until cutover — test the loop logic standalone.
8. **No bash test harness exists.** Validate with shellcheck + a standalone harness driving the loop functions against a fake "Fish" (a backgrounded `sleep`/`nc` you `kill` to simulate death). Do not add bats.
9. **Crash capture must never fail the job.** Wrap every `dmesg`/`journalctl`/`nvidia-smi` in best-effort form; the function returns 0 unconditionally. Log to `$HOME`-based `$QUEUE_DIR/logs`, `/tmp` fallback.
10. **`dmesg` may be restricted.** `kernel.dmesg_restrict=0` now, but wrap it best-effort with `journalctl -k` / `/var/log/messages` fallbacks; `nvidia-smi -q` works unprivileged.
11. **Respawned Fish has fresh memory — the voice reference is GONE.** `ensure_fish_speech_reference` runs ONCE at setup (`pipeline.py:2159`), not per-TTS; `_tts_fish_speech` keeps sending `reference_id` in its payload to the respawned server that never registered it. See Open Question 1 — this is the highest-risk unknown.

## Verification

- `shellcheck scripts/swanki_job.sbatch` — must stay clean (existing file already carries targeted `# shellcheck disable` directives; don't regress).
- **Standalone loop smoke test (no GPU/SLURM):** define `start_fish` to background a stub server (`python -m http.server $port` answering `/v1/health`, or a `sleep` + a flag file) and drive the poll loop. Kill the stub mid-loop; assert the supervisor captures a crash event, respawns the stub on the same port, and the loop continues. Then let the "swanki" stub exit 0 and assert the loop breaks with `gen_rc=0`; exit the stub non-zero and assert the job exits 1.
- **Bound test:** force the stub to die immediately on every spawn; assert the job stops after `SWANKI_FISH_MAX_RESTARTS+1` respawns, writes a `final` crash event, and exits non-zero.
- **Kill-switch test:** `SWANKI_FISH_RESTART_ENABLED=0` reproduces the old launch-once behavior (no supervisor, fast fail on Fish death).
- **Crash-log smoke:** confirm `$QUEUE_DIR/logs/swanki-job-<id>-fish-crash.log` is created and appended per event with timestamps; force `$QUEUE_DIR/logs` unwritable and confirm `/tmp` fallback; confirm a `dmesg`/`nvidia-smi` failure does not abort.
- **Real run (post-cutover or manual `sbatch`):** re-queue a LONGEST chapter (CH04/05/07) and confirm a mid-run Fish death respawns and the job reaches DONE. Tail the crash log to confirm exit code / dmesg / Xid capture populates.
- **No-content-change check:** `git diff` touches only `scripts/swanki_job.sbatch` (+ the dendron note); zero diff under `swanki/` confirms card/audio generation is untouched.

## Open Questions

1. **Does the Layer-1 retry re-register the voice reference after a respawn?** Evidence says NO: `ensure_fish_speech_reference` is called once at TTS setup (`swanki/pipeline/pipeline.py:2159`), and `_tts_fish_speech`'s retry (`_common.py` 1003-1036) only re-discovers the server — it never re-registers, yet keeps sending `reference_id` in the payload. A respawned Fish has empty reference memory, so the first post-respawn TTS likely fails the reference lookup (or silently falls back to no-voice). **Verify during implementation** whether Fish accepts an unknown `reference_id` gracefully or errors; if it errors, the supervisor must trigger re-registration after respawn (e.g. the sbatch re-runs the reference-add against the new server, OR a follow-up `_common.py` change makes `_tts_fish_speech` self-heal by calling `ensure_fish_speech_reference` on a reference-not-found response). Checkable in code, not a user question.
2. **Is `/v1/health` 200 sufficient evidence the respawned model can accept TTS?** Health may return 200 before the model is fully loaded enough to serve a TTS request (gotcha 6). **Verify during implementation** by issuing a tiny TTS probe immediately after the first post-respawn health-200; if it fails, add a short bounded grace (`SWANKI_FISH_RESPAWN_GRACE`) or a probe-until-success step after health in `start_fish`.
