# """CPU functionality."""

# import sys


# class CPU:
#     """Main CPU class."""

#     def __init__(self):
#         """Construct a new CPU."""
#         self.pc = 0
#         self.reg = [0] * 8
#         self.ram = [0] * 256
#         self.stack_pointer = 0xF4 # binary = 11110100, decimal = 244

#     def ram_read(self, address):
#         return self.ram[address]

#     def ram_write(self, address, value):
#         self.ram[address] = value

#     def load(self):
#         """Load a program into memory."""

#         address = 0
#         program = sys.argv[1]

#         try:
#             with open(program) as f:
#                 count = 0
#                 for line in f:
#                     count += 1
#                 # find and ignore anything following #
#                 comment_split = line.split('#')

#                 # convert binary to int
#                 number = comment_split[0].strip()
#                 try:
#                     x = int(number, 2)
#                 except ValueError:
#                     print('ValueError')

#                 self.ram[address] = x
#                 address += 1

#         except FileNotFoundError:
#             print(f"{sys.argv[0]}: {sys.argv[1]} not found")
#             sys.exit(2)

#         # For now, we've just hardcoded a program:

#         # program = [
#         #     # From print8.ls8
#         #     0b10000010,  # LDI R0,8
#         #     0b00000000,
#         #     0b00001000,
#         #     0b01000111,  # PRN R0
#         #     0b00000000,
#         #     0b00000001,  # HLT
#         # ]

#         # for instruction in program:
#         #     self.ram[address] = instruction
#         #     address += 1

#     def alu(self, op, reg_a, reg_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[reg_a] += self.reg[reg_b]
#         # elif op == "SUB": etc
#         else:
#             raise Exception("Unsupported ALU operation")

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             # self.fl,
#             # self.ie,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()

#     def run(self):
#         """Run the CPU."""
#         running = True
#         while running is True:
#             # instruction register
#             IR = self.ram_read(self.pc)
#             # read bytes from RAM, convert to variables
#             operand_a = self.ram_read(self.pc+1)
#             operand_b = self.ram_read(self.pc+2)
#             # self.trace()

#             # elif cascade LS8 specs
#             # HLT: stop program and exit emulator
#             if IR == 0b00000001:  # = 1
#                 running = False

#             # LDI: set value of register to an integer
#             if IR == 0b10000010:  # = 130
#                 self.reg[operand_a] = operand_b
#                 self.pc += 3

#             # PRN: print value stored in specified register
#             if IR == 0b01000111:  # = 71
#                 print(self.reg[operand_a])
#                 self.pc += 2

#             # MUL: multiply value is 2 registers and store product in regA
#             if IR == 0b10100010:  # = 162
#                 self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
#                 self.pc += 3

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
            # 0b10101000: self.and_func,
            0b10100111: self.cmp_func,
            0b00000001: self.hlt,
            0b01010101: self.jeq,
            0b01010100: self.jmp,
            0b01010110: self.jne,
            0b10000010: self.ldi,
            0b10100010: self.mul,
            # 0b01101001: self.not_func,
            # 0b10101010: self.or_func,
            0b01000110: self.pop,
            0b01000111: self.prn,
            0b01000101: self.push,
            # 0b10101100: self.shl,
            # 0b10101101: self.shr,
            # 0b10101011: self.xor,
        }

    def __repr__(self):
        return F"RAM: {self.ram} \n Register: {self.reg}"

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def htl(self, operand_a, operand_b):
        return (0, False)

    def ldi(self, operand_a, operand_b):
        pass

    def prn(self, operand_a, operand_b):
        pass

    def mul(self, operand_a, operand_b):
        pass

    def pop(self, operand_a, operand_b):
        pass

    def push(self, operand_a, operand_b):
        pass

    def cmp_func(self, operand_a, operand_b):
        pass

    def jmp(self, operand_a, operand_b):
        pass

    def jeq(self, operand_a, operand_b):
        pass

    def jne(self, operand_a, operand_b):
        pass

    def load(self, program):
        """Load a program into memory."""
        print("loading....")

        try:
            address = 0

            with open(program) as f:
                for line in f:
                    # find and ignore anything following #
                    comment_split = line.split('#')
                    # convert binary to int
                    number = comment_split[0].strip()
                    if number == "":
                        continue

                    value = int(number, 2)

                    self.ram_write(value, address)

                    address += 1

        except FileNotFoundError:
            print(f"{program} not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a]) * (self.reg[reg_b])
        
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

            operand_a = self.ram_read(self.PC+1)
            operand_b = self.ram_read(self.PC+2)

            try:
                op_output: self.commands[IR](operand_a, operand_b)

                running = op_output[1]
                self.PC += op_output[0]

            except:
                print(f"Unknown Command: {IR}")
                sys.exit(1)

        # while running is True:
        #     # instruction register
        #     IR = self.ram_read(self.PC)
        #     # read bytes from RAM, convert to variables
        #     operand_a = self.ram_read(self.PC+1)
        #     operand_b = self.ram_read(self.PC+2)
        #     # self.trace()

        #     # elif cascade LS8 specs
        #     # HLT: stop program and exit emulator
        #     if IR == 0b00000001:  # = 1
        #         running = False

        #     # LDI: set value of register to an integer
        #     if IR == 0b10000010:  # = 130
        #         self.reg[operand_a] = operand_b
        #         self.PC += 3

        #     # PRN: print value stored in specified register
        #     if IR == 0b01000111:  # = 71
        #         print(self.reg[operand_a])
        #         self.PC += 2

        #     # MUL: multiply value is 2 registers and store product in regA
        #     if IR == 0b10100010:  # = 162
        #         self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
        #         self.PC += 3
