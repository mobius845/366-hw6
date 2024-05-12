#Change filename to prog1.asm or prog2.asm
with open('prog1.asm', 'r') as f:
    lines = f.readlines()

#Dictionaries to store instructions and labels
instr_dict = {}
label_dict = {}

#Program Counter Initialization
PC = 0

for line in lines:
    line = line.strip()
    if not line:
        continue
    #If a label is present in the line, process it separately
    if ':' in line:
        label, instr = line.split(':')
        label_dict[label.strip()] = PC
        if instr:  # Check if there is an instruction after the label
            instr_dict[PC] = instr.split('#')[0].strip()  # Remove comments
            PC += 4
    else:
        instr_dict[PC] = line.split('#')[0].strip()  # Remove comments
        PC += 4

#Initialize Registers
registers = [0] * 32

#Function to evaluate each instruction
def evaluate_instruction(instruction):
    parts = instruction.split()
    if len(parts) == 0:
        return None, 0  # Skip empty lines

    op = parts[0]

    def get_register_value(register_string):
        return int(register_string.strip('$').rstrip(','))
    #Process instructions {addi, slt, beq}
    if op == 'addi':
        dest_reg = get_register_value(parts[1])
        src_reg = get_register_value(parts[2])
        immediate = int(parts[3])
        registers[dest_reg] = registers[src_reg] + immediate
    elif op == 'slt':
        dest_reg = get_register_value(parts[1])
        src_reg1 = get_register_value(parts[2])
        src_reg2 = get_register_value(parts[3])
        registers[dest_reg] = int(registers[src_reg1] < registers[src_reg2])
    elif op == 'beq':
        src_reg1 = get_register_value(parts[1])
        src_reg2 = get_register_value(parts[2])
        label = parts[3]
        if registers[src_reg1] == registers[src_reg2]:
            return label, label_dict[label]
        else:
            return None, PC + 4

    return None, 0

#Start executing instructions from the beginning
PC = 0

while PC in instr_dict:
    instruction = instr_dict[PC]
    print(f'PC: {PC}, Instruction: {instruction}')
    label, offset = evaluate_instruction(instruction)
    if label is not None:
        PC = offset
    else:
        PC += 4

print('\nRegister Values:')
for i, val in enumerate(registers):
    print(f'$r{i}: {val}')

print(f'Final PC: {PC}')