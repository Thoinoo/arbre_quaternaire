from __future__ import annotations
import json

from tkinter import *
from param import *


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
                return QuadTree.fromList(lst)
        except Exception as e:
            print("fromfile() error : " + str(e))

        # depuis main.py le chemin des fichiers doit être modifié
        try:
            with open("../" + filename, "r") as f:
                lst = json.load(f)
                return QuadTree.fromList(lst)
        except Exception as e:
            print("fromfile() error : " + str(e))

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

    def getBlocks(self):
        return self.__blocks


class TkQuadTree(Tk):

    """
    def newQuadtreeFrame(self,master_frame, block, depth):
        for index, element in enumerate(block.getBlocks()):
            if isinstance(element, QuadTree):
                self.newQuadtreeFrame(self, element)
            else:
                frame = Frame(master_frame, bg=color_dict[element], width=MAX_SIZE / 2, height=MAX_SIZE / 2)
                frame.place(x=coord_x[index], y=coord_y[index])
    """

    def paint(self):
        """ TK representation of a Quadtree"""
        main_frame = Frame(self, bg="black", width=MAX_SIZE, height=MAX_SIZE)
        main_frame.pack()
        depth = 1
        lenght = MAX_SIZE / 2**depth

        print(type(self.__quadtree.getBlocks()))
        print(len(self.__quadtree.getBlocks()))

        for index, block in enumerate(self.__quadtree.getBlocks()):
            if isinstance(block, QuadTree):
                pass
                # self.newQuadtreeFrame(main_frame, block)
                # frame = self.newQuadtreeFrame(self,block)
                # frame.place(x=coord_x[index], y=coord_y[index])
            else:
                frame = Frame(main_frame, bg=color_dict[block], width=lenght, height=lenght)
                frame.place(x=coord_x[index] * lenght, y=coord_y[index] * lenght)

        """
        frame1 = Frame(self, bg="black", width=512, height=512)
        frame1.pack()

        # Frame 2
        frame2 = Frame(frame1, bg="white", width=256, height=256)
        # frame2.pack(side=TOP, anchor=NW)
        frame2.place(x=0, y=0)

        frame3 = Frame(frame1, bg="blue", width=256, height=256)
        # frame3.pack(side=TOP, anchor=NE)
        frame3.place(x=256, y=0)

        frame4 = Frame(frame1, bg="red", width=256, height=256)
        # frame4.pack(side=BOTTOM, anchor=SW)
        frame4.place(x=0, y=256)
        """
        pass

    def __init__(self, filename):
        super().__init__()
        self.__quadtree = QuadTree.fromFile(filename)
        self.geometry(f"{MAX_SIZE}x{MAX_SIZE}")
        self.paint()
