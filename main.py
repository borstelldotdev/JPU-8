from sys import argv, exit
from enum import Enum

VERSION = "1.0"

class ParseableItems(Enum):
    INPUT_FILE = 1
    OUTPUT_FILE = 2
    LOG_FILE = 3 # TODO: implement

    ASSEMBLE = 10
    COMPILE = 11
    RUN = 12

if __name__ == "__main__":
    script, arguments = argv[0], argv[1:].copy()

    to_parse = [ParseableItems.INPUT_FILE]
    tasks = []

    output_file = "out"
    input_file = None
    verbose = False # TODO: Implement
    run = False

    if not arguments:
        print(f"JPU-8 compiler, assembler and simulator version {VERSION}")
        print(f"Usage: python[3] {script} [options] input_file")
        exit(0)


    # Parse arguments
    while arguments:
        arg = arguments.pop(0)
        print(arg)

        # Check for "compound argument" (e.i. -cav) and split it (e.i. -c -a -v)"
        if arg.startswith("-") and (not arg.startswith("--")) and len(arg) > 2:
            args = list(arg.lstrip("-"))
            args.reverse() # Insert at 0 in reversed order to preserve order
            for sub_arg in args:
                arguments.insert(0, "-" + sub_arg)
            continue


        if arg.startswith("-"):
            match arg:
                case "-o" | "--out" | "--output" | "--output-file":
                    to_parse.insert(0, ParseableItems.OUTPUT_FILE)

                case "-v" | "--verbose":
                    verbose = True

                case "-a" | "--assemble":
                    tasks.append(ParseableItems.ASSEMBLE)

                case "-r" | "--run" | "--run-file" | "-s" | "--simulate":
                    run = True


                # Not implemented yet
                case "-c" | "--compile":
                    # TODO: Implement compiler
                    tasks.append(ParseableItems.COMPILE)
                    raise NotImplementedError()

                case "-l" | "--log" | "--log-file":
                    # TODO: Implement logger
                    to_parse.insert(0, ParseableItems.LOG_FILE)
                    raise NotImplementedError()

        else:
            parsing = to_parse.pop(0)

            match parsing:
                case ParseableItems.INPUT_FILE:
                    input_file = arg

                case ParseableItems.OUTPUT_FILE:
                    output_file = arg

    # Run
    print(f"JPU-8-utils version {VERSION}")
    print()
    if not input_file:
        print("ERROR: no input file was given. Please provide a valid input file.")
        exit(-1)

    if not tasks:
        print("ERROR: no tasks were given. Please provide one or more tasks.")
        exit(-1)

    print(f"Found {len(tasks)} tasks")

    for task in tasks:
        match task:
            case ParseableItems.ASSEMBLE:
                print(" - Assembling...", end=" ")
                # TODO: Call assembler
                print("done")

    print()
    print(f"Wrote output to `{output_file}`")
    print("JPU-8-utils done. exiting...")
