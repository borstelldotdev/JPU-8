import logging
from ctypes import c_uint8
from abc import ABC, abstractmethod
from code import InteractiveConsole
from array import array


class Instruction:
    def __init__(self, instruction_a: c_uint8, instruction_b: c_uint8,
                 im_a=c_uint8(0), im_b=c_uint8(0)):
        self.instruction_b = instruction_b
        self.im_a = im_a
        self.im_b = im_b

    def get_pair(self, flag: bool) -> tuple[c_uint8, c_uint8]:
        if flag:
            return self.instruction_a, self.im_a
        else:
            return self.instruction_b, self.im_b

    @classmethod
    def from_binary(cls, data: int):
        im_b =  c_uint8(data & 0xFF)
        instruction_b =  c_uint8((data >> 8) & 0xFF)
        im_a =  c_uint8((data >> 16) & 0xFF)
        instruction_a = c_uint8((data >> 24) & 0xFF)
        new = cls(instruction_a, instruction_b, im_a, im_b)
        return new

    def __repr__(self):
        pass

class SupportsValueReadWrite(ABC):
    @property
    @abstractmethod
    def value(self):
        raise NotImplementedError()

    @value.setter
    @abstractmethod
    def value(self, val):
        raise NotImplementedError()

class Register(SupportsValueReadWrite):
    def __init__(self):
        super().__init__()
        self.val = c_uint8(0)

    @property
    def value(self):
        return self.val.value & 0xFF

    @value.setter
    def value(self, val):
        self.val.value = val & 0xFF

class Memory(SupportsValueReadWrite):
    def __init__(self):
        super().__init__()
        self.val = array("B", [0] * 256)
        self.addr = c_uint8(0)

    @property
    def value(self):
        return self.val[self.addr.value] & 0xFF

    @value.setter
    def value(self, val):
        self.val[self.addr.value] = val & 0xFF

class ExpansionPort(SupportsValueReadWrite):
    def __init__(self):
        super().__init__()
        self.mode = c_uint8(0)

    @property
    def value(self):
        match self.mode.value:
            case 0:
                val = int(input("IN  < ")) & 0xFF
                return val
            case 1:
                # Binära tal
                # TODO: Implement
                raise NotImplementedError()
            case 2:
                # Hexadecimala tal
                # TODO: Implement
                raise NotImplementedError()
            case 8:
                val = ord(input("IN  < ")[0])
                return val
            case _:
                raise ValueError("No such expansion port mode")

    @value.setter
    def value(self, val):
        match self.mode.value:
            case 0:
                print("OUT >", val)
            case 1:
                # Binära tal
                # TODO: Implement
                raise NotImplementedError()
            case 2:
                # Hexadecimala tal
                # TODO: Implement
                raise NotImplementedError()
            case 8:
                print(chr(val), end="")
            case _:
                raise ValueError("No such expansion port mode")


class JPU:
    class Repl(InteractiveConsole):
        def __init__(self, namespace=None):
            super().__init__(locals=namespace or {})
            self.instance = namespace["JPU"]

        def interact(self, banner="", exitmsg=""):
            try:
                super().interact(banner=banner, exitmsg=exitmsg)
            except SystemExit:
                print("Exiting REPL...")
                print()

        def runsource(self, source, filename="<input>", symbol="single"):
            match source.lower():
                case ".exit":
                    raise SystemExit
                case ".step":
                    self.instance.step()
                case ".dump":
                    for reg in self.instance.registers.keys():
                        print(f"{reg}: {self.instance.registers[reg].value}")
                    print("Flag:", self.instance.flag)
                case _:
                    super().runsource(source, filename=filename, symbol=symbol)


    def __init__(self, code: list[Instruction], logger: logging.Logger):
        assert len(code) <= 256

        self.flag = False
        self.code = code
        self.halted = True
        self.debug_mode = False
        self.logger = logger

        self.registers: dict[str, SupportsValueReadWrite] = {
            "A": Register(),
            "B": Register(),
            "C": Register(),
            "D": Register(),
            "XI": Register(),
            "YI": Register(),
            "ZO": Register(),
            "IM": Register(),
            "MEM": Memory(),
            "PC": Register(),
        }

        for key in self.registers.keys():
            self.__setattr__(key, self.registers[key])

        self.EX = ExpansionPort()

        self.read = {
            0b000: self.A,
            0b001: self.B,
            0b010: self.C,
            0b011: self.D,
            0b100: self.ZO,
            0b101: self.IM,
            0b110: self.EX,
            0b111: self.MEM
        }

        self.write = {
            0b000: self.A,
            0b001: self.B,
            0b010: self.C,
            0b011: self.D,
            0b100: self.XI,
            0b101: self.YI,
            0b110: self.EX,
            0b111: self.MEM
        }

    @classmethod
    def load_from_bin(cls, bin_data: str, logger: logging.Logger):
        instructions = []
        for line in bin_data.splitlines():
            raw = int(line.replace(" ", ""), 2)
            instruction = Instruction.from_binary(raw)
            instructions.append(instruction)
        return cls(instructions, logger)

    def start(self):
        self.halted = False
        self.debug_mode = False
        while not self.halted:
            try:
                self.step()
            except KeyboardInterrupt:
                logging.info("Received keyboard interrupt. Exiting...")

    def debug(self):
        self.halted = False
        self.debug_mode = True
        self.logger.info("Debug mode enabled")
        while not self.halted:
            try:
                self.step()
            except KeyboardInterrupt:
                logging.info("Received keyboard interrupt. Exiting...")

    def step(self):
        instruction, im = self.code[self.PC.value].get_pair(self.flag)
        instruction_cls = instruction.value >> 6
        instruction_data = instruction.value & 0b00111111
        # noinspection PyAttributeOutsideInit
        self.IM.value = im.value

        match instruction_cls:
            case 0b00:
                # Move-instruktion
                from_ = (instruction_data & 0b111000) >> 3
                to_   = instruction_data & 0b000111
                from_reg = self.read[from_]
                to_reg = self.write[to_]

                # Sätt minnesadress
                if type(from_reg) == Memory:
                    from_reg.addr.value = self.IM.value

                if type(to_reg) == Memory:
                    to_reg.addr.value = self.IM.value

                to_reg.value = from_reg.value

            case 0b01:
                a, b = self.XI.value, self.YI.value
                u = []
                for _ in range(6):
                    u.append(instruction_data & 0b00000001)
                    instruction_data = instruction_data >> 1

                flg, not_z, carry, op_, not_y, not_x = u
                a = a ^ (not_x * 0b11111111)
                b = b ^ (not_y * 0b11111111)
                if op_:
                    out = a | b
                else:
                    out = a + b + carry
                    if flg:
                        self.flag = bool(a + b + carry > 255)

                out = out ^ (not_z * 0b11111111)
                if op_:
                    self.flag = out == 0b00000000

                self.ZO.value = out

            case 0b10:
                raise NotImplementedError

            case 0b11:
                match instruction_data:
                    case 0b000000:
                        # Halt
                        self.halted = True
                    case 0b000001:
                        # Pause
                        if self.debug_mode:
                            print()
                            if input("[Debugger] Breakpoint reached. Do you wish to open the live REPL? (Y/N): ") \
                                    .lower().startswith("y"):
                                self.PC.value += 1
                                print("Welcome to the live REPL!")
                                print("Access registers with JPU.<REGISTER_NAME>")
                                print("Step with .step")
                                print("Dump registers with .dump")
                                print("Exit with .exit")


                                ns =  {
                                    "JPU": self
                                }

                                repl = self.Repl(ns)
                                repl.interact(banner="", exitmsg="")
                                return

                        input("Press enter to continue... ")
                    case 0b000010:
                        pass
                    case 0b000011:
                        pass
                    case 0b000100:
                        pass
                    case 0b001100:
                        pass
                    case 0b010100:
                        pass
                    case 0b011100:
                        pass
                    case 0b100100:
                        pass
                    case 0b101100:
                        pass
                    case 0b110100:
                        pass
                    case 0b111100:
                        pass
                    case 0b000100:
                        pass
                    case 0b001100:
                        pass
                    case 0b010100:
                        pass
                    case 0b011100:
                        pass
                    case 0b100100:
                        pass
                    case 0b101100:
                        pass
                    case 0b110100:
                        pass
                    case 0b111100:
                        pass
                    case 0b111101:
                        # Set device
                        self.EX.mode.value = self.IM.value
                    case 0b111111:
                        # No-op
                        pass

        self.PC.value += 1
