import sys

PRINT_BEEJ = 1
HALT = 2
PRINT_NUM = 3


memory = [
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    PRINT_BEEJ,
    HALT
]

pc = 0
running = True

while running:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print('Beej!')

    elif command == HALT:
        running = False

    else:
        print(f'Unknown instruction given', memory[pc])
        sys.exit(1)

    pc += 1