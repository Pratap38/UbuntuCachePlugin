# DANGER - manual-only script, NOT a pytest test (filename does not match
# test_*.py / *_test.py, so pytest never collects it). cleanAll() performs
# REAL destructive cleanup: real ~/.cache/thumbnails, real browser caches
# under ~/.cache, the real Trash, and (if run as root) a real `apt clean`.
# Only run this by hand, deliberately. Never run it in CI or as part of any
# automated test.

from cleaner.Completecleaner import cleanAll

cleanAll()