"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """
    
    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.__vm_output_file = output_stream

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """
        # Your code goes here!
        if segment == "CONST":
            segment = "constant"
        if segment == "ARG":
            segment = "argument"
        if segment == "LCL":
            segment = "local"
        self.__vm_output_file.write(f"push {segment.lower()} {index}")
        self.new_line()

    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.

        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        # Your code goes here!
        if segment == "CONST":
            segment = "constant"
        if segment == "ARG":
            segment = "argument"
        if segment == "LCL":
            segment = "local"
        self.__vm_output_file.write(f"pop {segment.lower()} {index}")
        self.new_line()

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG", 
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
        """
        # Your code goes here!
        self.__vm_output_file.write(command.lower())
        self.new_line()
            
    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        # Your code goes here!
        self.__vm_output_file.write(f"label {label}")
        self.new_line()

    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        self.__vm_output_file.write(f"goto {label}")
        self.new_line()

    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        self.__vm_output_file.write(f"if-goto {label}")
        self.new_line()

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        # Your code goes here!
        self.__vm_output_file.write(f"call {name} {n_args}")
        self.new_line()

    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        # Your code goes here!
        self.__vm_output_file.write(f"function {name} {n_locals}")
        self.new_line()

    def write_return(self) -> None:
        """Writes a VM return command."""
        # Your code goes here!
        self.__vm_output_file.write("return")
        self.new_line()

    def write_int_const(self, n: int):
        self.write_push("constant", n)

    def write_string_const(self, str_const: str):
        str_const = str_const[1:-1]
        self.write_push("constant", len(str_const))
        self.write_call("String.new", 1)
        for char in str_const:
            self.write_push("constant", ord(char))
            self.write_call("String.appendChar", 2)
    
    def new_line(self):
        self.__vm_output_file.write("\n")

    def indentation(self):
        self.__vm_output_file.write('  ')