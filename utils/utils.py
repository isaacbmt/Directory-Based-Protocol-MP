from numpy import random


def create_instruction(processorID):
    instr_type = random.binomial(2, 0.4)
    # READ
    if instr_type == 0:
        return [processorID, 'READ', random.binomial(7, 0.5), 0]
    elif instr_type == 1:
        return [processorID, 'WRITE', random.binomial(7, .7), random.binomial(65535, 0.5)]
    else:
        return [processorID, 'CALC', 0, 0]


def format_instruction(instr):
    if instr[1] == 'READ':
        return f'P{instr[0]}: READ { bin(instr[2]) }'
    elif instr[1] == 'WRITE':
        return f'P{instr[0]}: WRITE { bin(instr[2]) }; { hex(instr[3]) }'
    else:
        return f'P{instr[0]}: CALC'
