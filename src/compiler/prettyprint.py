def indent(text: str):
    lines = text.splitlines()
    lines = ["\t" + line for line in lines]
    return "\n".join(lines)

def repr_object(obj):
    if isinstance(obj, list) or isinstance(obj, tuple):
        return repr_iterable(obj)
    if isinstance(obj, dict):
        return repr_dict(obj)
    return obj.__repr__()

def repr_iterable(obj):
    vals = []
    for val in obj:
        vals.append(repr_object(val))
    return "\n" + indent("\n".join(vals))

def repr_dict(obj: dict):
    vals = []
    for val in obj:
        if val == "parent":
            continue

        vals.append(val + ": " + repr_object(obj[val]))

    return "\n" + indent("\n".join(vals))