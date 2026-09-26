# Manual cleanup helper for the folder tests/StressTest.py creates (not a
# pytest test - filename does not match test_*.py / *_test.py). The repo
# checkout path below is not under SAFE_DELETE_PATHS, so DeleteFolder() is
# expected to refuse this deletion under the current SafeCleaner rules; it
# is left here only to mirror the leftover "stress_test" folder's location,
# not as a verified cleanup mechanism. It does not touch any real
# user/system cache path.

from cleaner.SafeCleaner import DeleteFolder

result = DeleteFolder(
    "/home/pratap/Desktop/UbuntuCacheCLeaner/stress_test"
)

print(result)