import os

from quadtree import *

if __name__ == '__main__':

    pictures = {}
    key = 1
    for file in os.listdir('../files/'):
        if ".txt" in file:
            pictures[str(key)] = file
            key += 1

    usr_input = "0"
    while not usr_input in pictures:
        for key in pictures:
            print(f"{key} : {pictures[key]}")
        print("Quel fichier afficher ?")
        usr_input = input()

    filename = pictures[usr_input]

    win = TkQuadTree("../files/" + filename)
    win.mainloop()
