from sys import argv, exit
from enum import IntEnum
import logging

from src.assembler import Assembler
from src.simulator import JPU

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)

VERSION = "1.0"

class ParseableItems(IntEnum):
    INPUT_FILE = 1
    OUTPUT_FILE = 2
    LOG_FILE = 3

    COMPILE = 10
    ASSEMBLE = 11
    SAVE = 19
    RUN = 20

if __name__ == "__main__":
    script, arguments = argv[0], argv[1:].copy()

    to_parse: list[ParseableItems] = [ParseableItems.INPUT_FILE]
    tasks: list[ParseableItems] = [ParseableItems.SAVE]

    output_file = None
    input_file = None
    run = False
    debug = False

    if not arguments:
        print(f"JPU-8 compiler, assembler and simulator version {VERSION}")
        print(f"Usage: python[3] {script} [options] input_file")
        print(f"Use `python[3] {script} --help` for more information")
        exit(0)


    # Parse arguments
    while arguments:
        arg = arguments.pop(0).lower()

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

                case "-a" | "--assemble":
                    tasks.append(ParseableItems.ASSEMBLE)

                case "-r" | "--run" | "--run-file" | "-s" | "--simulate":
                    tasks.append(ParseableItems.RUN)

                case "-d" | "--debug" | "--debugger":
                    tasks.append(ParseableItems.RUN)
                    debug = True

                # Not implemented yet
                case "-c" | "--compile":
                    # TODO: Implement compiler
                    tasks.append(ParseableItems.COMPILE)
                    raise NotImplementedError()

                case "-l" | "--log" | "--log-file":
                    to_parse.insert(0, ParseableItems.LOG_FILE)

                case "-v" | "--verbose":
                    logger.setLevel(logging.DEBUG)

                case "--info":
                    logger.setLevel(logging.INFO)

                case "--warning":
                    logger.setLevel(logging.WARNING)

                case "--help":
                    print(f"JPU-8 compiler, assembler and simulator version {VERSION}")
                    print(f"Usage: python[3] {script} [options] input_file")
                    print(" -o | --out | --output | --output-file <output_file> : configure the output file path")
                    print(" -a | --assemble : assemble the file using the assembler")
                    print(" -r | --run | --run-file | -s | --simulate : run the file with the simulator")
                    print(" -l | --log | --log-file <output_file> : configure the log file path")
                    print(" -v | --verbose | --debug : set the logging level to `debug`")
                    print(" --info : set the logging level to `info` (default)")
                    print(" --warning : set the logging level to `warning`")
                    exit(0)


        else:
            parsing = to_parse.pop(0)

            match parsing:
                case ParseableItems.INPUT_FILE:
                    input_file = arg

                case ParseableItems.OUTPUT_FILE:
                    output_file = arg

                case ParseableItems.LOG_FILE:
                    logger.addHandler(logging.FileHandler(arg, encoding="utf-8"))

    # Run
    print(f"JPU-8-utils version {VERSION}")
    print()

    current = ""
    tasks = sorted(tasks)

    if not input_file:
        logger.error("ERROR: no input file was given. Please provide a valid input file.")
        exit(-1)

    if not tasks:
        logger.error("ERROR: no tasks were given. Please provide one or more tasks.")
        exit(-1)

    logger.info(f"Loading `{input_file}`...")
    with open(input_file, "r") as f:
        current = f.read()
    logger.debug(f"Successfully loaded `{input_file}`")

    logger.info(f"Found {len(tasks)} tasks")

    for task in tasks:
        match task:
            case ParseableItems.ASSEMBLE:
                logger.info(" - Assembling...")
                asm = Assembler(current, logger)
                current = asm.assemble()
                logger.debug("  Done assembling")

            case ParseableItems.SAVE:
                if current:
                    if not output_file:
                        logger.warning("No output file was specified. The output will be discarded")
                        continue

                    logger.info(f" - Writing output to `{output_file}`")
                    with open(output_file, "w") as f:
                        f.write(current)
                    logger.info(f"   Successfully wrote output to `{output_file}`")

            case ParseableItems.RUN:
                logger.info(" - Executing...")
                print()
                interpreter = JPU.load_from_bin(current, logger)
                if debug:
                    interpreter.debug()
                else:
                    interpreter.start()
                current = None
                print()
                logger.info("   Done executing")




    print()
    print("JPU-8-utils done. exiting...")
    exit(0)