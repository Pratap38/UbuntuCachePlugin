from Scanner.scan_engine import scanAll

from ui.Cachechart import showCacheChart

results = scanAll()

showCacheChart(results)