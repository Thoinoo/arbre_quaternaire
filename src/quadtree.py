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
    @staticmethod
    def newQuadtreeFrame(master_frame, block, depth):
        depth += 1
        lenght = MAX_SIZE / (2 ** depth)
        for index, element in enumerate(block.getBlocks()):
            x_pos = master_frame.winfo_x() + (coord_x[index] * lenght)
            y_pos = master_frame.winfo_y() + (coord_y[index] * lenght)
            if isinstance(element, QuadTree):
                frame = Frame(master_frame, width=lenght, height=lenght)
                frame.place(x=x_pos, y=y_pos)
                TkQuadTree.newQuadtreeFrame(frame, element, depth)
            else:
                frame = Frame(master_frame, bg=color_dict[element], width=lenght, height=lenght)
                frame.place(x=x_pos, y=y_pos)

    def paint(self):
        """ TK representation of a Quadtree"""
        main_frame = Frame(self, bg="blue", width=MAX_SIZE, height=MAX_SIZE)
        main_frame.pack()
        depth = 0

        self.newQuadtreeFrame(self, self.__quadtree, depth)

    def __init__(self, filename):
        super().__init__()
        self.__quadtree = QuadTree.fromFile(filename)
        self.geometry(f"{MAX_SIZE}x{MAX_SIZE}")
        self.paint()
