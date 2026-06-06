from Scanner.scan_engine import scanAll

from ui.Dashboard import (
    showHeader,
    showTable
)
result=scanAll()
showHeader()

showTable(result)