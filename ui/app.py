from Scanner.scan_engine import scanAll
from ui.Dashboard import (
    showHeader,
    showTable
)
from ui.Cachechart import showCacheChart
from cleaner.Completecleaner import  cleanAll
from Scanner.parallelScan import ParallelScan
def runAll():
    showHeader()
    result=ParallelScan()
    showTable(result)
    showCacheChart(result)
    cleanAll()
