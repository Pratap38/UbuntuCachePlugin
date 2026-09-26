# Manual stress script (not a pytest test - filename does not match
# test_*.py / *_test.py, so pytest never collects it automatically).
# Creates 1000 scratch files under a local "stress_delete" folder. That
# folder is not under SAFE_DELETE_PATHS, so DeleteFile() below is expected
# to refuse every deletion (this only measures/creates load, it does not
# verify real cleanup) - it does not touch any real user/system path.

import os

from cleaner.SafeCleaner import DeleteFile


ROOT = "stress_delete"


os.makedirs(
    ROOT,
    exist_ok=True
)

for i in range(1000):

    filePath = os.path.join(
        ROOT,
        f"file_{i}.tmp"
    )

    with open(
        filePath,
        "w"
    ) as f:

        f.write("test")


count = 0

for file in os.listdir(ROOT):

    filePath = os.path.join(
        ROOT,
        file
    )

    if DeleteFile(filePath):

        count += 1


print(
    f"Deleted: {count}"
)