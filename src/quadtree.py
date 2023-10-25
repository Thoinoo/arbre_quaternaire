from __future__ import annotations
import json
import os.path


class QuadTree:
    NB_NODES: int = 4

    def __init__(self, hg: bool | QuadTree, hd: bool | QuadTree, bd: bool | QuadTree, bg: bool | QuadTree):
        self.__blocks = [hg, hd, bd, bg]

    @property
    def depth(self) -> int:
        """ Recursion depth of the quadtree"""
        max_depth = 0

        for block in self.__blocks:
            if isinstance(block, QuadTree) and block.depth > max_depth:
                max_depth = block.depth
        return max_depth + 1

    @staticmethod
    def fromFile(filename: str) -> QuadTree:
        """ Open a given file, containing a textual representation of a list"""
        try:
            with open(filename, "r") as f:
                lst = json.load(f)
        except Exception as e:
            print("fromfile() error : " + str(e))

        return QuadTree.fromList(lst)


    @staticmethod
    def fromList(qt_list: list) -> QuadTree:
        """ Generates a Quadtree from a list representation"""
        qt_param = []
        for element in qt_list:
            if not isinstance(element, list):
                qt_param.append(element)
            else:
                qt_param.append(QuadTree.fromList(element))
        return QuadTree(qt_param[0], qt_param[1], qt_param[2], qt_param[3])


class TkQuadTree(QuadTree):
    def paint(self):
        """ TK representation of a Quadtree"""
        pass
