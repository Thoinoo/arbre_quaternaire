from quadtree import *


if __name__ == '__main__':
    text = 0
    while text != "1" and text != "2" and text != "3":
        print("\n1 : quadtree.txt\n2 : quadtree_easy.txt\n3 : test.txt\n quel fichier afficher ? ")
        text = input()

    match text:
        case "1":
            filename = "quadtree.txt"
        case "2":
            filename = "quadtree_easy.txt"
        case "3":
            filename = "test.txt"

        case _:
            filename = "test.txt"

    win = TkQuadTree("../files/" + filename)
    win.mainloop()


