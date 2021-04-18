from tkinter import *


def createTable(x, y, title, matrix, width, pos):
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
    print(rows)
    for item in matrix:
        i += 20
        j = 0
        for subitem in item:
            print(j)
            container.create_text(x + width_table/(columns*2) + j * width_table/columns, y + i, text=subitem)
            j += 1


root = Tk()
root.geometry('780x500')

createTable(10, 10, 'Procesador 0', [['1', '2', '3', '4'],
                                     ['1', '2', '3', '4']], 160, (10, 10))
createTable(10, 10, 'Procesador 1', [['1', '2', '3', '4'],
                                     ['1', '2', '3', '4']], 160, (200, 10))
createTable(10, 10, 'Procesador 2', [['3', '3', '3', '4'],
                                     ['1', '2', '3', '4']], 160, (390, 10))
createTable(10, 10, 'Procesador 3', [['3', '3', '3', '4'],
                                     ['1', '2', '3', '4']], 160, (580, 10))
createTable(10, 10, 'Caché L2', [['3', '3', '3', '4', '5'],
                                 ['1', '2', '3', '4', '5'],
                                 ['1', '2', '3', '4', '5'],
                                 ['1', '2', '3', '4', '5']], 160, (290, 120))
createTable(10, 10, 'Memoria', [ ['3', '3'],
                                 ['1', '2'],
                                 ['1', '2'],
                                 ['1', '2'],
                                 ['3', '3'],
                                 ['1', '2'],
                                 ['1', '2'],
                                 ['1', '2']
                                ], 160, (290, 260))


root.mainloop()
