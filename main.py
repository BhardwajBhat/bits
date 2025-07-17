from typing import Callable, Dict, List

import pyray as rl


class CPU:
    def __init__(self, program: List[str]) -> None:
        self.registers: Dict[str, int] = {f"R{i}": 0 for i in range(4)}
        self.pc: int = 0
        self.sp: int = 127
        self.program: List[str] = program
        self.instructions: Dict[str, Callable[..., None]] = {
            "ADD": self.op_add,
            "SUB": self.op_sub,
            "PUSH": self.op_push,
            "POP": self.op_pop,
            "STORE": self.op_store,
            "LOAD": self.op_load,
            "JMP": self.op_jmp,
        }
        self.flags: Dict[str, bool] = {
            "CARRY": False,
            "ZERO": False,
            "NEGATIVE": False,
        }
        self.memory: List[int] = [0] * 128

    def get_value(self, operand: str) -> int:
        if operand in self.registers:
            return self.registers[operand]
        return int(operand)

    def execute_instruction(self, line: str):
        parts = line.strip().split()

        if len(parts) < 2:
            raise ValueError("Instruction must have at least OPCODE and DEST")

        op = parts[0]
        args = parts[1:]

        if op not in self.instructions:
            raise ValueError(f"Unknown opcode: {op}")
        if args[0] not in self.registers:
            raise ValueError(f"Invalid register: {args[0]}")

        self.instructions[op](*args)

        self.print_registers()

    def op_add(self, dest: str, src: str) -> None:
        self.registers[dest] += self.get_value(src)
        if self.registers[dest] < 0:
            self.flags["NEGATIVE"] = True
        if self.registers[dest] == 0:
            self.flags["ZERO"] = True

    def op_sub(self, dest: str, src: str) -> None:
        self.registers[dest] -= self.get_value(src)
        if self.registers[dest] < 0:
            self.flags["NEGATIVE"] = True
        if self.registers[dest] == 0:
            self.flags["ZERO"] = True

    def op_store(self, dest: str, src: str) -> None:
        self.memory[self.get_value(dest)] = self.get_value(src)

    def op_load(self, dest: str, src: str) -> None:
        self.registers[dest] = self.memory[self.get_value(src)]

    def op_push(self, dest: str) -> None:
        self.memory[self.sp] = self.get_value(dest)
        self.sp -= 1

    def op_pop(self, dest: str) -> None:
        self.sp += 1
        self.registers[dest] = self.memory[self.sp]

    def op_jmp(self, dest: str) -> None:
        self.pc = self.get_value(dest) - 1

    def print_registers(self) -> None:
        print("  ".join(f"{reg}={val}" for reg, val in self.registers.items()))


def draw_cpu(cpu: CPU) -> None:
    rl.draw_text("CPU Registers:", 20, 20, 20, rl.WHITE)
    y = 50
    for reg, val in cpu.registers.items():
        rl.draw_text(f"{reg}: {val}", 20, y, 20, rl.YELLOW)
        y += 30

    rl.draw_text(f"PC: {cpu.pc}", 100, 50, 20, rl.YELLOW)
    rl.draw_text(f"SP: {cpu.sp}", 100, 80, 20, rl.YELLOW)

    rl.draw_text("Instructions:", 20, 200, 20, rl.WHITE)
    for idx, line in enumerate(cpu.program):
        if cpu.pc == idx:
            color = rl.RED
        else:
            color = rl.WHITE

        rl.draw_text(line, 20, 230 + idx * 30, 20, color)

    rl.draw_text("Flags:", 300, 20, 20, rl.WHITE)
    rl.draw_text(f"ZERO={cpu.flags['ZERO']}", 300, 50, 20, rl.WHITE)
    rl.draw_text(f"NEGATIVE={cpu.flags['NEGATIVE']}", 300, 80, 20, rl.WHITE)
    rl.draw_text(f"CARRY={cpu.flags['CARRY']}", 300, 110, 20, rl.WHITE)

    y = 0
    x = 0
    rl.draw_text("Memory:", 20, 400, 20, rl.WHITE)
    for idx, data in enumerate(cpu.memory):
        if idx % 16 == 0:
            y += 30
            x = idx % 16
        x += 1
        rl.draw_text(f"{data}", 20 + x * 40, 410 + y, 20, rl.YELLOW)


def main() -> None:
    program: List[str] = [
        "ADD R0 100",
        "ADD R1 2",
        "PUSH R0",
        "SUB R0 1",
        "JMP R1",
    ]

    cpu = CPU(program)

    rl.init_window(720, 720, "dumb")
    rl.set_target_fps(30)
    run: bool = False

    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        draw_cpu(cpu)

        if cpu.pc > len(cpu.program):
            continue

        if run is True:
            cpu.execute_instruction(program[cpu.pc])
            cpu.pc += 1
            rl.wait_time(0.05)

        if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE):
            cpu.execute_instruction(program[cpu.pc])
            cpu.pc += 1

        if rl.is_key_pressed(rl.KeyboardKey.KEY_P):
            run = not run

        rl.end_drawing()

    rl.close_window()


if __name__ == "__main__":
    main()
