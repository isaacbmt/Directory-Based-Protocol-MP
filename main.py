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

    p_numbers = ["P0", "P1", "P2", "P3"]
    p_number_var = StringVar()
    p_number_var.set("P0")
    p_number = OptionMenu(root, p_number_var, *p_numbers)
    p_number.place(x=30, y=470, width=50)

    instruction_types = ["READ", "WRITE", "CALC"]
    instruction_type_var = StringVar()
    instruction_type_var.set("READ")
    instruction_type = OptionMenu(root, instruction_type_var, *instruction_types)
    instruction_type.place(x=90, y=470, width=100)

    addresses = [bin(0), bin(1), bin(2), bin(3), bin(4), bin(5), bin(6), bin(7)]
    address_var = StringVar()
    address_var.set(bin(0))
    address = OptionMenu(root, address_var, *addresses)
    address.place(x=200, y=470, width=100)

    value = Entry(root)
    value.insert(0, 'Value')
    value.bind("<FocusIn>", lambda args: value.delete('0', 'end'))
    value.place(x=310, y=470, width=100)

    def send_instruction(processorID, type, addr, val):
        processorID = int(processorID[1:])
        # system.lock.acquire()
        system.processors[processorID].instruction = [processorID, type, addr, val]
        system.chosen_cpu = processorID
        system.processors[processorID].executed = False
        # system.lock.release()
        system.resume_stop_button(1, 'step', True)
        # value.delete('0', 'end')

    execute = Button(root,
                     text='Run',
                     command=lambda: send_instruction(p_number_var.get(),
                                                      instruction_type_var.get(),
                                                      int(address_var.get().replace("0b", ""), 2),
                                                      0 if (len(value.get()) == 0 or value.get() == 'Value')
                                                      else int(value.get())))
    execute.place(x=425, y=470)

    pause_button = Button(root, text='Pause', command=lambda: system.resume_stop_button(0, system.run_mode, False))
    pause_button.place(x=470, y=470)

    step_button = Button(root, text='Step', command=lambda: system.resume_stop_button(0, 'step', False))
    step_button.place(x=520, y=470)

    continuous_button = Button(root, text='Continuous execution',
                               command=lambda: system.resume_stop_button(0, 'continuous', False))
    continuous_button.place(x=570, y=470)

    stop_while_button = Button(root, text='Exit', command=system.end)
    stop_while_button.place(x=840, y=470)

    ins1_label = Label(root, text='')
    ins1_label.place(x=30, y=30)
    ins2_label = Label(root, text='')
    ins2_label.place(x=260, y=30)
    ins3_label = Label(root, text='')
    ins3_label.place(x=490, y=30)
    ins4_label = Label(root, text='')
    ins4_label.place(x=720, y=30)

    ins1_old_label = Label(root, text='')
    ins1_old_label.place(x=30, y=2)
    ins2_old_label = Label(root, text='')
    ins2_old_label.place(x=260, y=2)
    ins3_old_label = Label(root, text='')
    ins3_old_label.place(x=490, y=2)
    ins4_old_label = Label(root, text='')
    ins4_old_label.place(x=720, y=2)

    pause_label = Label(root, text='', font='times 24')
    pause_label.place(x=100, y=230)
    while system.run_while:
        lock.acquire()
        pause_label.config(text='Pause' if system.pause else '')
        if system.processors[0].instruction:
            ins1_label.config(text=format_instruction(system.processors[0].instruction))
        if system.processors[1].instruction:
            ins2_label.config(text=format_instruction(system.processors[1].instruction))
        if system.processors[2].instruction:
            ins3_label.config(text=format_instruction(system.processors[2].instruction))
        if system.processors[3].instruction:
            ins4_label.config(text=format_instruction(system.processors[3].instruction))

        if system.processors[0].instruction_old:
            ins1_old_label.config(text=format_instruction(system.processors[0].instruction_old))
        if system.processors[1].instruction_old:
            ins2_old_label.config(text=format_instruction(system.processors[1].instruction_old))
        if system.processors[2].instruction_old:
            ins3_old_label.config(text=format_instruction(system.processors[2].instruction_old))
        if system.processors[3].instruction_old:
            ins4_old_label.config(text=format_instruction(system.processors[3].instruction_old))

        create_table(10, 10, 'Procesador 0', system.processors[0].cacheL1.get_information(), 200, (10, 50), root)
        create_table(10, 10, 'Procesador 1', system.processors[1].cacheL1.get_information(), 200, (240, 50), root)
        create_table(10, 10, 'Procesador 2', system.processors[2].cacheL1.get_information(), 200, (470, 50), root)
        create_table(10, 10, 'Procesador 3', system.processors[3].cacheL1.get_information(), 200, (700, 50), root)
        create_table(10, 10, 'Caché L2', system.cache_l2.get_information(), 320, (280, 140), root)
        create_table(10, 10, 'Memoria', system.memory.get_information(), 180, (365, 260), root)
        lock.release()

        time.sleep(0.5)


root = Tk()
root.geometry('940x500')

interface = Thread(target=run_gui)
interface.start()

root.mainloop()

s = input('ff: ')

for i in range(len(system.processors)):
    system.processors[i].join()

interface.join()
