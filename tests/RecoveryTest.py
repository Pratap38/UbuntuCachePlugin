# Manual demo script (not a pytest test - no def test_...() functions, and
# the filename does not match pytest's test_*.py / *_test.py discovery
# patterns, so it is never collected automatically).
#
# This used to call DeleteFile("/etc/passwd") and DeleteFile("/root/test.tmp")
# directly - real system paths. SafeCleaner already blocks both (neither is
# under SAFE_DELETE_PATHS), so nothing was ever actually deleted, but a real
# system path should never appear in a demo script. It now uses a throwaway
# directory under the system temp dir instead, which is outside
# SAFE_DELETE_PATHS just like /etc/passwd was, so it demonstrates the exact
# same "unsafe path blocked" + recovery-manager-logging behaviour safely.

import os
import tempfile

from cleaner.SafeCleaner import DeleteFile

from core.Errorrecover import (
    recoverymanager
)

with tempfile.TemporaryDirectory() as scratch:
    unsafe_path = os.path.join(scratch, "not_under_safe_delete_paths.tmp")
    with open(unsafe_path, "w") as f:
        f.write("demo")

    result1 = DeleteFile(unsafe_path)

    result2 = DeleteFile(
        os.path.join(scratch, "also_missing.tmp")
    )

    print(result1)

    print(result2)

    recoverymanager.TotalsummaryReport()