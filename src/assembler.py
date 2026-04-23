import logging
import os

class Instruction:
    def __init__(self):
        self.unset_code = ""
        self.unset_intermediate = None
        self.set_code = ""
        self.set_intermediate = None
        self.label = None

    @classmethod
    def parse(cls, code: str):
        new = cls()

        code = code.strip()
        if code.startswith('.'):
            tok_ = code.split(' ', maxsplit=1)
            new.label = tok_[0].lower()[1:]
            code = tok_[1] if len(tok_) > 1 else ""

        if "|" in code:
            set_s, unset_s = code.split("|", maxsplit=1)
        else:
            set_s, unset_s = code, code

        if set_s.endswith("]") and "[" in set_s:
            new.set_code, new.set_intermediate = set_s[:-1].split("[", maxsplit=1)
        else:
            new.set_code = set_s

        if unset_s.endswith("]") and "[" in unset_s:
            new.unset_code, new.unset_intermediate = unset_s[:-1].split("[", maxsplit=1)
        else:
            new.unset_code = unset_s

        new.unset_code, new.set_code = new.unset_code.strip(), new.set_code.strip()

        return new

    def compile(self, assembler: Assembler) -> int:
        s = self._compile(self.set_code, assembler)
        si = self._compile(self.set_intermediate, assembler) if self.set_intermediate else 0x00
        u = self._compile(self.unset_code, assembler)
        ui = self._compile(self.unset_intermediate, assembler) if self.unset_intermediate else 0x00

        return s << 24 | si << 16 | u << 8 | ui

    @staticmethod
    def _compile(code: str, assembler: Assembler):
        tokens = code.split(" ")
        compiled = 0b00000000
        idx = 0

        if tokens[0] in assembler.definitions.keys():
                # Hantera definitionskedjor rekursivt
                return Instruction._parse_token(assembler.definitions[token], assembler)

        for token in tokens:
            compiled = compiled | Instruction._parse_token(token, assembler, idx=idx)
            idx += 1

        return compiled


    @staticmethod
    def _parse_token(token: str, assembler: Assembler, idx=None):
        if token in assembler.definitions.keys():
            # Hantera definitionskedjor rekursivt
            return Instruction._parse_token(assembler.definitions[token], assembler)

        if idx and f"{token}{{{idx}}}" in assembler.definitions.keys():
            return Instruction._parse_token(assembler.definitions[f"{token}{{{idx}}}"], assembler)

        try:
            value = int(token, 0)  # Auto-detektera 20, 0x16, 0b1010, 0o24 osv
        except ValueError:
            raise ValueError(f"Could not parse `{token}`")
        except TypeError:
            raise ValueError(f"Could not parse `{token}`")
        return value & 0xFF # modda med 256


    def __repr__(self):
        set_c = self.set_code + (f" [{self.set_intermediate}]" if self.set_intermediate else "")
        unset_c = self.unset_code + (f" [{self.unset_intermediate}]" if self.unset_intermediate else "")

        return (f".{self.label}\n\t" if self.label else "\t") + \
               (unset_c if unset_c == set_c else f"{unset_c} | {set_c}")



class Assembler:
    BASE_LIB_PATH = "./lib/"

    def __init__(self, code: str, logger: logging.Logger):
        self.code = code
        self.logger = logger
        self.instructions: list[Instruction] = []
        self.assembled: list[int] = []

        self.definitions = {}
        self.procs = {}
        self.dependencies: list[str] = []
        self.entrypoint = None

        self.parsing_proc = ""
        self.current_proc: list[str] = []

    @classmethod
    def from_file(cls, filename: str, logger):
        with open(filename, 'r') as f:
            data = f.read()
            new = cls(data, logger)
        return new

    def assemble(self):
        if not self.instructions:
            self.tokenize(self.code)
            self.merge()

        if not self.assembled:

            if self.entrypoint:
                self.instructions.append(Instruction.parse(f"SYS JMP {self.entrypoint}"))
            else:
                self.logger.warning("No entrypoint configured. Please consider adding a #enerypoint <.label>")

            self.define_labels()

            self._assemble_instructions()
        return self.asm_to_text()

    def _tokenize_line(self, line: str):
        code = line.split(';', maxsplit=1)[0].strip()

        if not code: return

        if code.startswith('#'):
            self.parse_compiler_annotation(code.split())
            return

        if self.parsing_proc:
            self.current_proc.append(code)
        else:
            instruction = Instruction.parse(code)
            self.instructions.append(instruction)

    def tokenize(self, code):
        codelines = code.split('\n')
        i = 0
        while i < len(codelines):
            self._tokenize_line(codelines[i])
            i += 1

    def merge(self):
        ptr = 0
        flg = None
        while ptr < len(self.instructions):
            ins = self.instructions[ptr]
            if ins.label and not (ins.unset_code or ins.set_code):
                flg = self.instructions.pop(ptr).label
            else:
                if flg:
                    ins.label = flg
                    flg = None
                ptr += 1

    def define_labels(self):
        line = 0
        for instruction in self.instructions:
            if instruction.label:
                self.definitions["." + instruction.label] = str(line)
            line += 1

    def _assemble_instructions(self):
        for instruction in self.instructions:
            asm_ = instruction.compile(self)
            self.assembled.append(asm_)

    def parse_compiler_annotation(self, tokens: list[str]):
        match tokens[0].lower():
            case "#include":
                assert len(tokens) == 2
                lib = tokens[1].lstrip("<").rstrip(">")
                if lib in self.dependencies: # To prevent recursive inclusions
                    return

                self.dependencies.append(lib)

                with open(self.BASE_LIB_PATH + lib, "r") as f:
                    data = f.read()

                self.tokenize(data)

            case "#define":
                assert len(tokens) == 3
                self.definitions[tokens[1]] = tokens[2]

            case "#proc":
                assert len(tokens) == 2
                self.parsing_proc = tokens[1]

            case "#end":
                self.procs[self.parsing_proc] = self.current_proc
                self.parsing_proc = ""
                self.current_proc = []

            case "#entrypoint":
                assert len(tokens) == 2
                self.entrypoint = tokens[1]

            case "#setup_point":
                # TODO: Implement
                raise NotImplementedError()

            case "#":
                raise ValueError(f"No such compiler annotation `#`. Did you add a space? (in {" ".join(tokens)})")

            case _:
                raise ValueError(f"No such compiler annotation `{tokens[0]}` (in {" ".join(tokens)})")

    def asm_to_text(self):
        return "\n".join([" ".join([f"{x:032b}"[i:i+8] for i in range(0,32,8)]) for x in self.assembled])

    def __repr__(self):
        if self.assembled:
            return "Assembled code: \n" + self.asm_to_text()
        if self.instructions:
            return "Processed code: \n" + "\n".join([x.__repr__() for x in self.instructions])
        return "Unprocessed code" + self.code

if __name__ == "__main__":
    os.chdir("..")
    asm = Assembler.from_file("./examples/add.jsm", logger=logging.getLogger(__name__))
    print(asm.assemble())
    asm.assemble()
    print(asm)