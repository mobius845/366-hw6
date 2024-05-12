addi $6, $0, -3
addi $7, $0, 5
addi $8, $0, -1
loop:
addi $8, $8, 3
addi $7, $7, -1
slt $9, $6, $7
beq $9, $0, out
beq $0, $0, loop
out:
addi $10, $8, -10