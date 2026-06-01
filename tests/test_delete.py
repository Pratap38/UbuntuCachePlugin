from cleaner.SafeCleaner import DeleteFile
from cleaner.SafeCleaner import DeleteFolder


testFile = "/etc/passwd"

# result = DeleteFile(testFile)
result=DeleteFolder(testFile)

print(result)