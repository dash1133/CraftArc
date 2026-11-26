#!/usr/bin/env bash
# Runs the automated steps of the website change checklist (CLAUDE.md) in order.
# Usage: bash website/tests/check_all.sh     Exit code is non-zero if any required step fails.
# The launch check is informational: it reports NOT READY while placeholders are on the site.
set -u
cd "$(dirname "$0")/../.."
fail=0
step() { echo; echo "== $1"; }

step "0. Code lint and static build (Next.js export to website/out)"
[ -d website/node_modules ] || (cd website && npm ci --no-audit --no-fund >/dev/null) || fail=1
(cd website && npm run lint --silent) || fail=1
out=$(cd website && npm run build 2>&1); rc=$?
echo "$out" | grep -E "Compiled|Exporting|rror" ; [ "$rc" -eq 0 ] || { echo "$out" | tail -30; fail=1; }

step "1. AI-writing fingerprints and word rules: the checks themselves still work"
python3 website/tests/copy_lint.py --self-test || fail=1

step "1-3. Copy lint: fingerprints, banned words, word rules, American spelling, ASD-STE100, numbers"
out=$(python3 website/tests/copy_lint.py 2>&1); rc=$?
echo "$out" | grep -v "  WARN " ; [ "$rc" -eq 0 ] || fail=1

step "5. Browser tests: every section, the story player, the tabs, the briefing form, the footer"
out=$(node website/tests/e2e.mjs 2>&1); rc=$?
echo "$out" | grep -E "FAIL|passed, " ; [ "$rc" -eq 0 ] || fail=1

step "10. Launch check (informational)"
python3 website/tests/launch_check.py | tail -1

echo
if [ "$fail" -eq 0 ]; then echo "AUTOMATED CHECKS PASSED. Now finish the manual items in CLAUDE.md (visual check, docs, report)."; else echo "AUTOMATED CHECKS FAILED. Fix them before completing the request."; fi
exit $fail
