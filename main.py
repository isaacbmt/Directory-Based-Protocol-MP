import time
from tkinter import *
from gui.create_table import create_table
from models.system import System, CacheL2, Memory, Lock
from threading import Thread
from utils.utils import format_instruction


lock = Lock()
cache_l2 = CacheL2()
memory = Memory()
system = System(cache_l2, memory, lock)
# system.change_mode(1)
system.start()


def run_gui():
    container = Canvas(root, width=940, height=40, bg='#42db8c')
    container.place(x=0, y=460)

    p_number = Entry(root)
    p_number.insert(0, 'P#')
    p_number.bind("<FocusIn>", lambda args: p_number.delete('0', 'end'))
    p_number.place(x=30, y=470, width=40)

    instruction_type = Entry(root)
    instruction_type.insert(0, 'Type')
    instruction_type.bind("<FocusIn>", lambda args: instruction_type.delete('0', 'end'))
    instruction_type.place(x=80, y=470, width=100)

    address = Entry(root)
    address.insert(0, 'Address')
    address.bind("<FocusIn>", lambda args: address.delete('0', 'end'))
    address.place(x=190, y=470, width=100)

    value = Entry(root)
    value.insert(0, 'Value')
    value.bind("<FocusIn>", lambda args: value.delete('0', 'end'))
    value.place(x=300, y=470, width=100)

    def send_instruction(processorID, type, addr, val):
        processorID = int(processorID[1:])
        system.processors[processorID].executed = False
        system.processors[processorID].instruction = [processorID, type, addr, val]
        p_number.delete('0', 'end')
        instruction_type.delete('0', 'end')
        address.delete('0', 'end')
        value.delete('0', 'end')
        print(format_instruction([processorID, type, addr, val]))

    execute = Button(root,
                     text='Run',
                     command=lambda: send_instruction(p_number.get(),
                                                      instruction_type.get(),
                                                      int(address.get()),
                                                      0 if (len(value.get()) == 0 or value.get() == 'Value')
                                                      else int(value.get())))
    execute.place(x=410, y=470)

    ins1_label = Label(root, text='')
    ins1_label.place(x=30, y=30)
    ins2_label = Label(root, text='')
    ins2_label.place(x=260, y=30)
    ins3_label = Label(root, text='')
    ins3_label.place(x=490, y=30)
    ins4_label = Label(root, text='')
    ins4_label.place(x=720, y=30)
    while True:
        # lock.acquire()
        if system.processors[0].instruction:
            ins1_label.config(text=format_instruction(system.processors[0].instruction))
        if system.processors[1].instruction:
            ins2_label.config(text=format_instruction(system.processors[1].instruction))
        if system.processors[2].instruction:
            ins3_label.config(text=format_instruction(system.processors[2].instruction))
        if system.processors[3].instruction:
            ins4_label.config(text=format_instruction(system.processors[3].instruction))
        create_table(10, 10, 'Procesador 0', system.processors[0].cacheL1.get_information(), 200, (10, 50), root)
        create_table(10, 10, 'Procesador 1', system.processors[1].cacheL1.get_information(), 200, (240, 50), root)
        create_table(10, 10, 'Procesador 2', system.processors[2].cacheL1.get_information(), 200, (470, 50), root)
        create_table(10, 10, 'Procesador 3', system.processors[3].cacheL1.get_information(), 200, (700, 50), root)
        create_table(10, 10, 'Caché L2', system.cache_l2.get_information(), 280, (320, 140), root)
        create_table(10, 10, 'Memoria', system.memory.get_information(), 180, (365, 260), root)
        # lock.release()

        time.sleep(1)


root = Tk()
root.geometry('940x500')

interface = Thread(target=run_gui)
interface.start()

root.mainloop()

s = input('ff: ')
for i in range(len(system.processors)):
    system.processors[i].join()

# interface.join()