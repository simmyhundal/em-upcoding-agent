#!/bin/sh
# The fast checks to run before every merge (about a minute, no model calls, no paid run); the full suite runs once per release.
# Usage: sh tests/run_fast.sh
cd "$(dirname "$0")/.." || exit 1
fail=0
for t in test_readme_sync test_readme_columns test_concepts test_figures test_parity_table test_release_table test_seed_registry test_score_42 test_agent_53 test_eval_modes; do
  if python3 "tests/$t.py" >/dev/null 2>&1; then echo "ok   $t"; else echo "FAIL $t"; fail=1; fi
done
exit $fail
