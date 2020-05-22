"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.stack_pointer = 0xF4 # binary = 11110100, decimal = 244

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0
        program = sys.argv[1]

        try:
            with open(program) as f:
                count = 0
                for line in f:
                    count += 1
                # find and ignore anything following #
                comment_split = line.split('#')

                # convert binary to int
                num = comment_split[0].strip()
                try:
                    x = int(num, 2)
                except ValueError:
                    print('ValueError')

                self.ram[address] = x
                address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
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
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running is True:
            # instruction register
            IR = self.ram_read(self.pc)
            # read bytes from RAM, convert to variables
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            # self.trace()

            # elif cascade LS8 specs
            # HLT: stop program and exit emulator
            if IR == 0b00000001:  # = 1
                running = False

            # LDI: set value of register to an integer
            if IR == 0b10000010:  # = 130
                self.reg[operand_a] = operand_b
                self.pc += 3

            # PRN: print value stored in specified register
            if IR == 0b01000111:  # = 71
                print(self.reg[operand_a])
                self.pc += 2

            # MUL: multiply value is 2 registers and store product in regA
            if IR == 0b10100010:  # = 162
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
                self.pc += 3
