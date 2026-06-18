from Scanner.scan_engine import scanAll
from ui.Dashboard import (
    showHeader,
    showTable
)
from ui.Cachechart import showCacheChart
from cleaner.Completecleaner import  cleanAll
from Scanner.parallelScan import ParallelScan
from Scanner.AsyncScan import runAsyncscan
def runAll():
    showHeader()
    result=runAsyncscan()
    showTable(result)
    showCacheChart(result)
    cleanAll()
