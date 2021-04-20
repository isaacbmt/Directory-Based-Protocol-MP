from tkinter import *


def create_table(x, y, title, matrix, width, pos, root):
    rows = len(matrix)
    columns = len(matrix[0])
    width_table = width
    height_table = (rows + 1) * 20

    container = Canvas(root, width=width_table+8, height=height_table+8)
    container.place(x=pos[0], y=pos[1])
    container.create_rectangle(x, y, x + width_table, y + height_table, outline='black')

    i = 10
    container.create_text(x + width_table / 2, y + i, text=title)
    container.create_rectangle(x, y, x + width_table, y + 20)
    for item in matrix:
        i += 20
        j = 0
        for subitem in item:
            container.create_text(x + width_table/(columns*2) + j * width_table/columns, y + i, text=subitem)
            j += 1
