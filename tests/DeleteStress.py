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