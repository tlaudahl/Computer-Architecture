"""CPU functionality."""

import sys

HLT  = 0b00000001
LDI  = 0b10000010
PRN  = 0b01000111
MUL  = 0b10100010
ADD  = 0b10100000
POP  = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET  = 0b00010001
CMP  = 0b10100111
JMP  = 0b01010100
JEQ  = 0b01010101
JNE  = 0b01010110
L    = 0 # Less-than: during a `CMP`, set to 1 if registerA is less than registerB, zero otherwise.
G    = 0 # Greater-than: during a `CMP`, set to 1 if registerA is greater than registerB, zero otherwise.
E    = 0 # Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero otherwise.


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.FL = 0b00000000 # 0
        self.reg[self.sp] = 0xf4 # 244

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
            elif IR == ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3
            elif IR == POP:
                val = self.ram[self.reg[self.sp]]
                reg = self.ram_read(self.pc + 1)
                self.reg[reg] = val
                self.reg[self.sp] += 1
                self.pc += 2
            elif IR == PUSH:
                reg = self.ram_read(self.pc + 1)
                val = self.reg[reg]
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = val
                self.pc += 2
            elif IR == CALL:
                val = self.pc+2
                reg = self.ram[self.pc+1]
                subroutine = self.reg[reg]
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = val
                self.pc = subroutine
            elif IR == RET:
                address = self.reg[self.sp]
                self.pc = self.ram[address]
                self.reg[self.sp] += 1
            elif IR == CMP:
                self.FL = CMP
                if self.reg[operand_a] < self.reg[operand_b]:
                    L = 1
                    G = 0
                    E = 0
                    self.FL = CMP - 0b00000100
                elif self.reg[operand_a] > self.reg[operand_b]:
                    L = 0
                    G = 1
                    E = 0
                    self.FL = CMP - 0b00000010
                elif self.reg[operand_a] == self.reg[operand_b]:
                    L = 0
                    G = 0
                    E = 1
                    self.FL = CMP - 0b00000001
                self.pc += 3
            elif IR == JMP:
                # Jump to the address stored in the given register.
                # Set the `PC` to the address stored in the given register.

                # Machine code:
                # 01010100 00000rrr
                # 54 0r
                self.pc = self.reg[operand_a]
            elif IR == JEQ:
                # If `equal` flag is set (true), jump to the address stored in the given register.

                # Machine code:
                # 01010101 00000rrr
                # 55 0r
                if E == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == JNE:
                # If `E` flag is clear (false, 0), jump to the address stored in the given register.

                # Machine code:
                # ```
                # 01010110 00000rrr
                # 56 0r
                # ```
                if E == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            else:
                print('Unknown Instruction', IR)
