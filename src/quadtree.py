from __future__ import annotations
from param import *
import json
from tkinter import *


class QuadTree:
    NB_NODES: int = 4

    def __init__(self, hg: bool | QuadTree, hd: bool | QuadTree, bd: bool | QuadTree, bg: bool | QuadTree):
        """
        hg: top left block
        hd: top rigth block
        bd: bottom right block
        bg: bottom left block
        """
        self.__blocks = [hg, hd, bd, bg]

    @property
    def depth(self) -> int:
        """ Recursion depth of the quadtree """
        max_depth = 0

        for block in self.__blocks:
            if isinstance(block, QuadTree) and block.depth > max_depth:
                max_depth = block.depth
        return max_depth + 1

    @staticmethod
    def fromFile(filename: str) -> QuadTree:
        """ Open a given file, containing a textual representation of a list """
        try:
            with open(filename, "r") as f:
                lst = json.load(f)
                return QuadTree.fromList(lst)
        except Exception as e:
            print("fromfile() error : " + str(e))

    @staticmethod
    def fromList(qt_list: list) -> QuadTree:
        """ Generates a Quadtree from a list representation """
        qt_param = []
        for element in qt_list:
            if not isinstance(element, list):
                qt_param.append(element)
            else:
                qt_param.append(QuadTree.fromList(element))
        return QuadTree(qt_param[0], qt_param[1], qt_param[2], qt_param[3])

    def getBlocks(self):
        return self.__blocks


class TkQuadTree(Tk):
    COORD_X: list = [0, 1, 0, 1]
    COORD_Y: list = [0, 0, 1, 1]
    """ block placement order, must match the order of the Quadtree constructor """

    @staticmethod
    def newQuadtreeFrame(master_frame: Frame, qt: QuadTree, depth: int = 0):
        """
        Create 4 new frames inside master_frame
        master_frame : main frame in which will be created 4 frame
        qt: Quadtree that is going to be rendered in the master_frame
        depth: depth of the node, default = 0 to render the image fully
        """
        depth += 1
        lenght = MAX_SIZE / (2 ** depth)
        for index, element in enumerate(qt.getBlocks()):
            x_pos = master_frame.winfo_x() + (TkQuadTree.COORD_X [index] * lenght)
            y_pos = master_frame.winfo_y() + (TkQuadTree.COORD_Y[index] * lenght)
            if isinstance(element, QuadTree):
                frame = Frame(master_frame, width=lenght, height=lenght)
                frame.place(x=x_pos, y=y_pos)
                TkQuadTree.newQuadtreeFrame(frame, element, depth)
            else:
                frame = Frame(master_frame, bg=color_dict[element], width=lenght, height=lenght)
                frame.place(x=x_pos, y=y_pos)

    def __init__(self, filename: str):
        """ Initiate a TKinter windows with a representation of a Quadtree (filename) """
        super().__init__()
        self.__quadtree = QuadTree.fromFile(filename)
        self.geometry(f"{MAX_SIZE}x{MAX_SIZE}")
        self.newQuadtreeFrame(self, self.__quadtree)
        self.title(f"{filename} | Depth : {str(self.__quadtree.depth)} layer(s)")
