from ctypes import c_uint8

class Instruction:
    def __init__(self, instruction_a: c_uint8, instruction_b: c_uint8,
                 im_a=c_uint8(0), im_b=c_uint8(0)):
        self.instruction_a = instruction_a
        self.instruction_b = instruction_b
        self.im_a = im_a
        self.im_b = im_b

    def get_pair(self, flag: bool) -> tuple[c_uint8, c_uint8]:
        if flag:
            return self.instruction_a, self.im_a
        else:
            return self.instruction_b, self.im_b

class JPU:
    def __init__(self, code: list[Instruction]):
        assert len(code) <= 256

        self.flag = False
        self.code = code
        self.halted = False

        self.registers = {
            "A": c_uint8(0),
            "B": c_uint8(0),
            "C": c_uint8(0),
            "D": c_uint8(0),
            "XI": c_uint8(0),
            "YI": c_uint8(0),
            "ZO": c_uint8(0),
            "IM": c_uint8(0),
            "EX": c_uint8(0),
            "MEM": c_uint8(0),
            "PC": c_uint8(0),
        }

        for key in self.registers.keys():
            self.__setattr__(key, self.registers[key])

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

    def _execute_one(self):
        instruction, im = self.code[self.PC].get_pair(self.flag)
        instruction_cls = instruction.value >> 6
        instruction_data = instruction.value & 0b00111111
        print(instruction_cls, instruction_data)

        match instruction_cls:
            case 0b00:
                # Move-instruktion
                from_ = instruction_data & 0b111000
                to_   = instruction_data & 0b000111
                from_reg = self.read[from_]
                to_reg = self.write[to_]

                to_reg.value = from_reg.value

            case 0b01:
                a, b = self.XI.value, self.YI.value
                u = []
                for _ in range(6):
                    u.append(instruction_data & 0b00000001)
                    u = u >> 1

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
                        pass
                    case 0b111111:
                        # No-op
                        pass
