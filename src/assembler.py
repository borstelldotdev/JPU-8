class Instruction:
    def __init__(self):
        self.unset_code = ""
        self.unset_intermediate = None
        self.set_code = ""
        self.set_intermediate = None
        self.flag = None

    @classmethod
    def parse(cls, code: str, comment: str=""):
        new = cls()
        new.comment = comment

        code = code.strip()
        if code.startswith('.'):
            tok_ = code.split(' ', maxsplit=1)
            new.flag = tok_[0].lower()[1:]
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

    def __repr__(self):
        set_c = self.set_code + (f" [{self.set_intermediate}]" if self.set_intermediate else "")
        unset_c = self.unset_code + (f" [{self.unset_intermediate}]" if self.unset_intermediate else "")

        return (f".{self.flag}" if self.flag else "\t") + \
               (unset_c if unset_c == set_c else f"{unset_c} | {set_c}")



class Preprocessor:
    def __init__(self, code: str):
        self.code = code
        self.instructions: list[Instruction] = []
        self.definitions = {}
        self.

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, 'r') as f:
            data = f.read()
            new = cls(data)
        return new

    def tokenize(self):
        codelines = self.code.split('\n')
        for line in codelines:
            if not line: continue

            code = line.split(';', maxsplit=1)[0].strip()

            if not code: continue

            if code.startswith('#'):
                self.parse_compiler_annotation(code.split())
                continue

            instruction = Instruction.parse(code)
            self.instructions.append(instruction)



    def parse_compiler_annotation(self, tokens: list[str]):
        match tokens[0].lower():
            case "#include":
                pass

            case "#define":
                pass

            case "#macro":
                pass

            case "#entrypoint":
                pass

            case "#setup_point":
                pass

    def __repr__(self):
        if self.instructions:
            return "Processed code: \n" + "\n".join([x.__repr__() for x in self.instructions])
        else:
            return "Unprocessed code" + self.code

if __name__ == "__main__":
    pre = Preprocessor.from_file("../examples/add.jsm")
    pre.tokenize()
    print(pre)
