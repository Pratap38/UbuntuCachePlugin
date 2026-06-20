from cleaner.SafeCleaner import DeleteFile

from core.Errorrecover import (
    recoverymanager
)

result1 = DeleteFile(
    "/root/test.tmp"
)

result2 = DeleteFile(
    "/etc/passwd"
)

print(result1)

print(result2)

recoverymanager.TotalsummaryReport()