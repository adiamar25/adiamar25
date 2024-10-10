"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    parser = Parser(input_file)
    symbol_table = SymbolTable()

    # First pass
    label_counter = 0
    while parser.has_more_commands():
        parser.advance()
        cur_command = parser.get_current_command()
        cur_type = parser.command_type()
        if cur_type == "L_COMMAND":
            symbol = parser.symbol()
            symbol_table.add_entry(symbol, label_counter)
        else:
            label_counter += 1

    parser.restart()
    # Second pass
    n = 16
    while parser.has_more_commands():
        machine_instruction = ""
        parser.advance()
        if parser.command_type() == "A_COMMAND":
            a_number: int = 0
            symbol = parser.symbol()
            if symbol.isdecimal():
                a_number = int(symbol)
            elif symbol_table.contains(symbol):
                a_number = symbol_table.get_address(symbol)
            else:
                a_number = n
                symbol_table.add_entry(symbol, a_number)
                n += 1
            machine_instruction = format(a_number, "016b") + "\n"
            output_file.write(machine_instruction)

        elif parser.command_type() == "C_COMMAND":
            start_bits = "111"
            cur_command = parser.get_current_command()
            if "<<" in cur_command or ">>" in cur_command:
                start_bits = "101"
            comp = Code.comp(parser.comp())
            dest = Code.dest(parser.dest())
            jump = Code.jump(parser.jump())

            machine_instruction = start_bits + comp + dest + jump + "\n"
            output_file.write(machine_instruction)

    output_file.close()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)