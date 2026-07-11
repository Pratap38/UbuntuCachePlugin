import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.CacheSelection import CacheSelectionScreen

def main():
    app=CacheSelectionScreen()
    app.run()


if __name__=="__main__":
    main()