"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[SP] = 0xf4 # 244

    def ram_read(self, MAR):
        if MAR > 255:
            raise Exception(f'RAM does not extend to {MAR}')
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        if MAR > 255:
            raise Exception(f'RAM does not extend to {MAR}')
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        address = 0

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.split('#')[0]
                    line = line.strip()
                    if line == '':
                        continue

                    value = int(line, 2)
                    self.ram[address] = value
                    address += 1
        except IndexError:
            print('No file given')
        except:
            print('Error')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
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

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)


            if IR == HLT:
                self.pc = 0
                running = False
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif IR == POP:
                val = self.ram[self.reg[SP]]
                reg = self.ram_read(self.pc + 1)
                self.reg[reg] = val
                self.reg[SP] += 1
                self.pc += 2
            elif IR == PUSH:
                reg = self.ram_read(self.pc + 1)
                val = self.reg[reg]
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = val
                self.pc += 2
            else:
                print('Unknown Instruction')
