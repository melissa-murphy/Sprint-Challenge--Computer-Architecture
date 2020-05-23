"""CPU functionality."""

import sys

AND = 0b10101000  # ALU command
CMP = 0b10100111  # ALU command
HLT = 0b00000001
JEQ = 0b01010101
JMP = 0b01010100
JNE = 0b01010110
LDI = 0b10000010
MUL = 0b10100010  # ALU command
NOT = 0b01101001  # ALU command
OR = 0b10101010  # ALU command
POP = 0b01000110
PRN = 0b01000111
PUSH = 0b01000101
SHL = 0b10101100  # ALU command
SHR = 0b10101101  # ALU command
XOR = 0b10101011  # ALU command


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.PC = self.reg[0]  # program counter stored
        self.SP = self.reg[7]  # stack pointer stored
        self.FL = self.reg[4]  # flag stored

        # handle ls8 operations
        self.cmd_op = {
            # 0b10101000: self.and_func, # 168
            0b10100111: self.cmp_func,  # 167
            0b00000001: self.hlt,  # 1
            0b01010101: self.jeq,  # 85
            0b01010100: self.jmp,  # 84
            0b01010110: self.jne,  # 86
            0b10000010: self.ldi,  # 130
            0b10100010: self.mul,  # 162
            # 0b01101001: self.not_func, # 105
            # 0b10101010: self.or_func, # 170
            0b01000110: self.pop,  # 70
            0b01000111: self.prn,  # 71
            0b01000101: self.push,  # 69
            # 0b10101100: self.shl, # 172
            # 0b10101101: self.shr, # 173
            # 0b10101011: self.xor, # 171
        }

    def __repr__(self):
        return F"RAM: {self.ram} \n Register: {self.reg}"

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def hlt(self, operand_a, operand_b):  # halt program and exit
        return (0, False)

    def ldi(self, operand_a, operand_b):  # assign value to register
        self.reg[operand_a] = operand_b
        return (3, True)

    def prn(self, operand_a, operand_b):  # print value in current register
        print(self.reg[operand_a])
        return (2, True)

    # multiply values from both registers and store in first register
    def mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        return (3, True)

    def pop(self, operand_a, operand_b):
        # read starting point from stack pointer variable
        value = self.ram_read(self.SP)
        self.reg[operand_a] = value  # write to indicated register
        self.SP += 1  # increment stack pointer to next occupied memory in the stack

        return (2, True)

    def push(self, operand_a, operand_b):
        self.SP -= 1  # decrement stack point and return open spot in memory
        # gets value from operand_a current register
        value = self.reg[operand_a]
        # writes to above value to the stack pointer address
        self.ram_write(value, self.SP)

        return (2, True)

    def cmp_func(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        return (3, True)

    def jmp(self, operand_a, operand_b):
        # retrieve address from reg and set to PC
        self.PC = self.reg[operand_a]
        return (0, True)

    def jeq(self, operand_a, operand_b):
        # if flag is True (1) set pc to address retreived from reg
        if self.FL == 0b00000001:
            self.PC = self.reg[operand_a]
            return (0, True)
        return (2, True)

    def jne(self, operand_a, operand_b):
        # if flag is False (0) set pc to address retreived from reg
        if self.FL != 0b00000001:
            self.PC = self.reg[operand_a]
            return (0, True)
        return (2, True)

    def load(self, program):
        """Load a program into memory."""
        print("loading....")
        program = sys.argv[1]
        address = 0
        try:
            count = 0
            with open(program) as f:
                count += 1
                for line in f:
                    # find and ignore anything following #
                    comment_split = line.split('#')
                    number = comment_split[0].strip()  # convert binary to int

                    if number == "":
                        continue

                    value = int(number, 2)

                    self.ram_write(value, address)

                    address += 1

        except FileNotFoundError:
            print(f"{program} not found")
            sys.exit(2)

        if len(sys.argv) != 2:
            print(
                f"please format the command line: \n python3 ls8.py <filename>", file=sys.stderr)
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a]) * (self.reg[reg_b])
        elif op == "CMP":
            if self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010  # 2
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100  # 4
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001  # 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        # refactored to use pointer and operandi

        while running:
            IR = self.ram[self.PC]

            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            self.trace()

            try:
                op_output: self.cmd_op[IR](operand_a, operand_b)

                running = op_output[1]
                self.PC += op_output[0]

            except:
                print(f"Unknown Command: {IR}")
                sys.exit(1)
