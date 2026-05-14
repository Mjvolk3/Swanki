"""
swanki/voice_clone/denoise.py
[[swanki.voice_clone.denoise]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/voice_clone/denoise.py
Test file: tests/test_voice_clone_denoise.py

Thin wrapper around DeepFilterNet for cleaning archival voice-clone references.
DFN's pretrained model handles tape hiss, room tone, and broadband noise found
in old YouTube uploads while preserving voice prosody — the qualities that
matter for Fish Speech voice cloning.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def denoise_with_deepfilternet(
    input_wav: Path,
    output_wav: Path,
) -> dict[str, str]:
    """Denoise *input_wav* with DeepFilterNet, writing *output_wav*.

    Args:
        input_wav: Path to the noisy input wav (any sample rate; DFN resamples).
        output_wav: Where to write the cleaned wav.

    Returns:
        A small dict suitable for stamping into a voice-ref metadata block:
        ``{"method": "deepfilternet", "model": "<DFN model name>"}``.
    """
    # Imported lazily so callers without DFN installed can still load this module.
    # DFN 0.5.6 imports torchaudio.backend.common.AudioMetaData, which was
    # removed in torchaudio 2.1+. Shim a stub so the import resolves.
    import dataclasses
    import sys
    import types
    import torchaudio
    if "torchaudio.backend" not in sys.modules:
        @dataclasses.dataclass
        class _AudioMetaDataShim:
            sample_rate: int = 0
            num_frames: int = 0
            num_channels: int = 0
            bits_per_sample: int = 0
            encoding: str = ""

        backend_mod = types.ModuleType("torchaudio.backend")
        common_mod = types.ModuleType("torchaudio.backend.common")
        common_mod.AudioMetaData = _AudioMetaDataShim  # type: ignore[attr-defined]
        sys.modules["torchaudio.backend"] = backend_mod
        sys.modules["torchaudio.backend.common"] = common_mod
        torchaudio.backend = backend_mod  # type: ignore[attr-defined]
        backend_mod.common = common_mod  # type: ignore[attr-defined]
    from df.enhance import enhance, init_df, load_audio, save_audio

    assert input_wav.exists(), f"input wav not found: {input_wav}"
    output_wav.parent.mkdir(parents=True, exist_ok=True)

    # Bypass df.io (which uses removed torchaudio APIs) — load + save manually.
    import soundfile as sf
    import torch

    logger.info(f"Loading DeepFilterNet model")
    model, df_state, _ = init_df()
    target_sr = df_state.sr()

    logger.info(f"Reading {input_wav.name}")
    audio_np, src_sr = sf.read(str(input_wav), dtype="float32", always_2d=True)
    audio_t = torch.from_numpy(audio_np.T)  # (channels, samples)

    if src_sr != target_sr:
        from torchaudio.functional import resample
        audio_t = resample(audio_t, src_sr, target_sr)

    logger.info(f"Denoising with DeepFilterNet (sr={target_sr})")
    enhanced = enhance(model, df_state, audio_t)
    enhanced_np = enhanced.detach().cpu().numpy().T  # (samples, channels)

    sf.write(str(output_wav), enhanced_np, target_sr, subtype="PCM_16")
    logger.info(f"Wrote {output_wav}")
    return {"method": "deepfilternet", "model": "DeepFilterNet3"}
