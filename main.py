from typing import Dict, Callable, List
import pyray as rl


class CPU:
    def __init__(self, program: List[str]) -> None:
        self.registers: Dict[str, int] = {f"R{i}": 0 for i in range(4)}
        self.pc: int = 0
        self.program: List[str] = program
        self.instructions: Dict[str, Callable[[str, str], None]] = {
            "ADD": self.op_add,
            "SUB": self.op_sub,
        }

    def get_value(self, operand: str) -> int:
        if operand in self.registers:
            return self.registers[operand]
        return int(operand)

    def execute_instruction(self, line: str):
        print(f"Executing: {line}")
        try:
            op, dest, src = line.strip().split()
            if op not in self.instructions:
                raise ValueError(f"Unknown opcode: {op}")
            if dest not in self.registers:
                raise ValueError(f"Invalid register: {dest}")

            self.instructions[op](dest, src)
            self.print_registers()
        except Exception as e:
            print(f"Error: {e}")

    def op_add(self, dest: str, src: str) -> None:
        self.registers[dest] += self.get_value(src)

    def op_sub(self, dest: str, src: str) -> None:
        self.registers[dest] -= self.get_value(src)

    def print_registers(self) -> None:
        print("  ".join(f"{reg}={val}" for reg, val in self.registers.items()))


def draw_cpu(cpu: CPU) -> None:
    rl.draw_text("CPU Registers:", 20, 20, 20, rl.WHITE)
    y = 50
    for reg, val in cpu.registers.items():
        rl.draw_text(f"{reg}: {val}", 20, y, 20, rl.YELLOW)
        y += 30

    rl.draw_text("Instructions:", 20, 200, 20, rl.WHITE)
    for idx, line in enumerate(cpu.program):
        if cpu.pc == idx:
            color = rl.RED
        else:
            color = rl.WHITE

        rl.draw_text(line, 20, 230 + idx * 30, 20, color)


def main() -> None:
    program: List[str] = [
        "ADD R1 10",
        "ADD R2 20",
        "ADD R1 R2",
    ]

    cpu = CPU(program)

    rl.init_window(720, 720, "dumb")
    rl.set_target_fps(30)

    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        draw_cpu(cpu)

        if cpu.pc < len(program) and rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE):
            cpu.execute_instruction(program[cpu.pc])
            cpu.pc += 1

        rl.end_drawing()

    rl.close_window()


if __name__ == "__main__":
    main()
