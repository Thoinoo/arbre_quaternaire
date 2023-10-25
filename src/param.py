# taille maximum de l'image en pixel, préféré un puissance de deux
MAX_SIZE = 512

# couleur bichrome de représentation quadtree dans TKinter
color_dict = {0: "black", 1: "white"}

# ordre de placement des block : haut gauche, haut droite, bas gauche, bas droite
# doit correspondre à l'ordre de placement du constructeur Quadtree
coord_x = [0, 1, 0, 1]
coord_y = [0, 0, 1, 1]