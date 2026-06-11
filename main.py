# from Scanner.scan_engine import scanDirectory, scanAll

# import os

# from core.utils import bytes_to_mb, format_size
# from core.logger import logger
# from core.permission import checkSystemAccess




# checkSystemAccess()
# path = os.path.expanduser("~/.cache")

# logger.info("Application started")


# size, file = scanDirectory(path)

# print(f"Total Scanned Path : {path}")
# print(f"Total Files        : {file}")
# print(f"Total Size         : {bytes_to_mb(size):.2f} MB")


# results = scanAll()

# print("\n************ CACHE ANALYSIS *************\n")

# totalSize = 0
# totalFile = 0

# for category in results:

#     totalSize += category.size
#     totalFile += category.files

#     print(f"Category     : {category.name}")
#     print(f"Path         : {category.path}")
#     print(f"Risk Level   : {category.riskLevel}")
#     print(f"Files        : {category.files}")
#     print(f"Size         : {format_size(category.size)}")

    


# print("\n************ FINAL SUMMARY *************\n")

# print(f"Total Files  : {totalFile}")
# print(f"Total Size   : {format_size(totalSize)}")


#updated new one

from core.logger import logger
from core.permission import checkSystemAccess

from ui.app import runAll


def main():

    logger.info("Application Started")

    checkSystemAccess()

    runAll()


if __name__ == "__main__":

    main()