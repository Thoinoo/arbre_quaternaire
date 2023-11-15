""" allow to add a Quadtree parameter in the Quadtree constructor """
from __future__ import annotations
import sys
import json
from tkinter import Tk, Frame
from param import MAX_SIZE, color_dict


class QuadTree:
    """ Quadtree """
    NB_NODES: int = 4
    """ number of node of a Quadtree, set 8 for a 3D Quadtree """

    def __init__(self, hg: bool | QuadTree,
                 hd: bool | QuadTree,
                 bd: bool | QuadTree,
                 bg: bool | QuadTree):
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
    def is_format_correct(data: list) -> bool:
        """ Check if the file is in a Quadtree list format """
        if isinstance(data, list):
            if len(data) != QuadTree.NB_NODES:
                return False
            for element in data:
                if not QuadTree.is_format_correct(element):
                    return False
        return True

    @staticmethod
    def from_file(filename: str) -> QuadTree:
        """ Open a given file, containing a textual representation of a list,
         check if the list is in a Quatree format, if not close the app"""
        try:
            with open(filename, "r", encoding='utf8') as f:
                lst = json.load(f)
        except FileNotFoundError as e:
            print("from_file() error : " + str(e))

        if not QuadTree.is_format_correct(lst):
            print(f"bad file format : {filename}")
            sys.exit()
        return QuadTree.from_list(lst)

    @staticmethod
    def from_list(qt_list: list) -> QuadTree:
        """ Generates a Quadtree from a list representation """
        qt_param = []
        for element in qt_list:
            if isinstance(element, list):
                qt_param.append(QuadTree.from_list(element))
            else:
                qt_param.append(element)
        return QuadTree(*qt_param)

    @property
    def blocks(self):
        """ return blocks property """
        return self.__blocks


class TkQuadTree(Tk):
    """ Allow to display a Quadtree """
    COORD_X: list = [0, 1, 0, 1]
    COORD_Y: list = [0, 0, 1, 1]
    """ block placement order, must match the order of the Quadtree constructor """

    @staticmethod
    def new_quadtree_frame(master_frame: Frame, qt: QuadTree, depth: int = 0):
        """
        Create 4 new frames inside master_frame
        master_frame : main frame in which will be created 4 frame
        qt: Quadtree that is going to be rendered in the master_frame
        depth: depth of the node, default = 0 to render the image fully
        """
        depth += 1
        lenght = MAX_SIZE // (2 ** depth)
        for index, element in enumerate(qt.blocks):
            x_pos = master_frame.winfo_x() + (TkQuadTree.COORD_X[index] * lenght)
            y_pos = master_frame.winfo_y() + (TkQuadTree.COORD_Y[index] * lenght)
            if isinstance(element, QuadTree):
                frame = Frame(master_frame, width=lenght, height=lenght)
                frame.place(x=x_pos, y=y_pos)
                TkQuadTree.new_quadtree_frame(frame, element, depth)
            else:
                frame = Frame(master_frame, bg=color_dict[element], width=lenght, height=lenght)
                frame.place(x=x_pos, y=y_pos)

    def __init__(self, filename: str):
        """ Initiate a TKinter windows with a representation of a Quadtree (filename) """
        super().__init__()
        self.__quadtree = QuadTree.from_file(filename)
        self.geometry(f"{MAX_SIZE}x{MAX_SIZE}")
        self.new_quadtree_frame(self, self.__quadtree)
        self.title(f"{filename} | Depth : {str(self.__quadtree.depth)} layer(s)")
