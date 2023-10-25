import sys

from quadtree import *


if __name__ == '__main__':
    #print(sys.getrecursionlimit())
    sys.setrecursionlimit(3000)

    filename = "files/quadtree.txt"
    win = TkQuadTree(filename)
    win.mainloop()


