# # checking app internal log history 

import logging 
import os

LogDir="logs"

if not os.path.exists(LogDir):
    os.makedirs(LogDir)

logging.basicConfig(
    filename="logs/cache_cleaner.log",  ##log sare save honge isme 
    level=logging.INFO,                                                
                                                                       
    format="%(asctime)s - %(levelname)s - %(message)s"  ##2026-05-25 12:40:11 - INFO - Scan started#    


)
logger=logging.getLogger("CacheCleaner")

 ##{-->Logging levels
 # Level	Meaning
# DEBUG	developer details
# INFO	normal events
# WARNING	suspicious
# ERROR	failures
# CRITICAL	severe crash#}##