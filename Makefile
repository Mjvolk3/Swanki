# Swanki convenience targets.
#
# This repo's real task-running lives in the `swanki` CLI and scripts/*.sh; this
# Makefile is only a thin set of shortcuts that delegate to those scripts. (Docs
# have their own Makefile under docs/.)
.DEFAULT_GOAL := help

.PHONY: help queue queue-list queue-clean-failed

help: ## List available targets
	@grep -E '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) \
		| sed 's/:.*## /\t/' | sort | awk -F '\t' '{printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

queue: ## Show the generation-queue dashboard (drainer, running, pending, archives)
	@bash scripts/swanki_dequeue.sh --status

queue-list: ## List pending jobs with their slice indices
	@bash scripts/swanki_dequeue.sh --list

queue-clean-failed: ## Purge the failed-job archive (irreversible)
	@bash scripts/swanki_dequeue.sh --state failed --all --purge
