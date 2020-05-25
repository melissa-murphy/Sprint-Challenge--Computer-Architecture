"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.sp = 0xF4
        self.fl = 0b00000000

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        program = sys.argv[1]
        address = 0

        try:
            with open(program) as f:
                count = 0
                for line in f:
                    count += 1
                    # Process comments, and ignore them.
                    # Ignore anything after a # symbol
                    comment_split = line.split('#')

                    # Convert numbers from binary strings to integers
                    num = comment_split[0].strip()
                    try:
                        x = int(num, 2)
                    except ValueError:
                        continue
                    # print(f"{x:08b}: {x:d}")

                    self.ram[address] = x
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found.")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""
        return {
            'ADD': lambda: self.reg[reg_a] + self.reg[reg_b],
            'SUB': lambda: self.reg[reg_a] - self.reg[reg_b],
            'MUL': lambda: self.reg[reg_a] * self.reg[reg_b],
            'MOD': lambda: self.reg[reg_a] % self.reg[reg_b],
            'AND': lambda: self.reg[reg_a] & self.reg[reg_b],
            'OR': lambda: self.reg[reg_a] | self.reg[reg_b],
            'XOR': lambda: self.reg[reg_a] ^ self.reg[reg_b],
            'NOT': lambda: ~self.reg[reg_b],
            'SHL': lambda: self.reg[reg_a] << self.reg[reg_b],
            'SHR': lambda: self.reg[reg_a] >> self.reg[reg_b],

        }.get(op, lambda: 'Not a valid operation')()

        # if op == "ADD":
        #     self.reg[reg_a] += self.reg[reg_b]
        # elif op == "MUL":
        #     self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        # elif op == "MOD":
        #     self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        # elif op == "AND":
        #     self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        # elif op == "OR":
        #     self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        # elif op == "XOR":
        #     self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        # elif op == "NOT":
        #     self.reg[reg_a] = ~self.reg[reg_a]
        # elif op == "SHL":
        #     self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        # elif op == "SHR":
        #     self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]

        # else:
        #     raise Exception("Unsupported ALU operation")

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
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # self.trace()

            # HLT or HALT! -- Halt the CPU (and exit the emulator).
            if IR == 0b00000001:
                running = False

            # LDI register immediate -- Set the value of a register to an integer.
            elif IR == 0b10000010:
                self.reg[operand_a] = operand_b
                self.pc += 3

            # PRN register pseudo-instruction -- Print numeric value stored in the given register.
            elif IR == 0b01000111:
                print(self.reg[operand_a])
                self.pc += 2

            # stack op

            # PUSH register -- Push the value in the given register on the stack.
            elif IR == 0b01000101:
                # Decrement the SP
                # Copy the value in the given register to the address pointed to by SP
                self.sp -= 1
                self.ram[self.sp] = self.reg[operand_a]
                self.pc += 2

            # POP register -- Pop the value at the top of the stack into the given register.
            elif IR == 0b01000110:
                # Copy the value from the address pointed to by SP to the given register.
                # Increment SP.
                self.reg[operand_a] = self.ram[self.sp]
                self.sp += 1
                self.pc += 2

            # subroutine

            # CALL register - Calls a subroutine (function) at the address stored in the register.
            elif IR == 0b01010000:
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2
                self.pc = self.reg[operand_a]

            # RET - Return from subroutine.
            elif IR == 0b00010001:
                # Pop the value from the top of the stack and store it in the PC
                self.pc = self.ram[self.sp]
                self.sp += 1

            # CMP registerA registerB -- Compare the values in two registers
            # FL bits: 00000LGE
            elif IR == 0b10100111:
                if self.reg[operand_a] == self.reg[operand_b]:
                    self.fl = 0b00000001
                elif self.reg[operand_a] > self.reg[operand_b]:
                    self.fl = 0b00000010
                else:
                    self.fl = 0b00000100
                self.pc += 3

           # sprint challenge

            # JMP register
            elif IR == 0b01010100:
                # Jump to the address stored in the given register; set pc to stored address

                self.pc = self.reg[operand_a]

            # JEQ register -- If equal flag is set (true), jump to the address stored
            elif IR == 0b01010101:
                # use bin() here so self.fl isn't passed as a decimal
                if bin(self.fl)[-1] == '1':
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            # JNE register -- If E flag is (false, 0), jump to the address stored
            elif IR == 0b01010110:
                if bin(self.fl)[-1] == '0':
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            # ALU OP

            # ADD + the value in two registers and store the result in registerA.
            elif IR == 0b10100000:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3

            # MUL * the values in two registers together and store the result in registerA.
            elif IR == 0b10100010:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            # MOD
            elif IR == 0b10100100:
                if self.reg[operand_b] != 0:
                    self.alu("MOD", operand_a, operand_b)
                    self.pc += 3
                else:
                    print("Error with R[b] in MOD")
                    running = False

            # AND
            elif IR == 0b10101000:
                self.alu("AND", operand_a, operand_b)
                self.pc += 3
            # OR
            elif IR == 0b10101010:
                self.alu("OR", operand_a, operand_b)
                self.pc += 3

            # XOR - XOR registerA registerB - Perform a bitwise-XOR between the values in registerA and registerB, storing the result in registerA.
            elif IR == 0b10101011:
                self.alu('XOR', operand_a, operand_b)
                self.pc += 3

            # NOT
            elif IR == 0b01101001:
                self.alu("NOT", operand_a, operand_b)
                self.pc += 2

            # SHL
            elif IR == 0b10101100:
                self.alu("SHL", operand_a, operand_b)
                self.pc += 3
            # SHR
            elif IR == 0b10101101:
                self.alu("SHR", operand_a, operand_b)
                self.pc += 3
