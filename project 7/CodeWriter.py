"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from typing import Optional
import os


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        
        self.__asm_file = open(output_stream.name, 'w')
        self.__current_file: Optional[str] = None
        self.__label_number = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.__current_file = filename.replace(".vm", "").split("/")[-1]

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        """The list of the arithmetic commands: *add, *sub, *and, *or, 
            *eq, *gt, *lt, *neg, *not, shiftleft, shiftright"""
        if command in ("add", "sub"):
            self.add_sub_arithmetic(command)
        if command in ("and", "or", "not", "neg"):
            self.bool_arithmetic(command)
        if command in ("eq", "gt", "lt"):
            self.eq_gt_lt(command)
        if command in ("shiftleft", "shiftright"):
            self.shiftleft_shiftright(command)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        i = str(index)
        if command == "C_PUSH":
            if segment == "local":
                self.load_segment_index("LCL", index)
            if segment == "argument":
                self.load_segment_index("ARG", index)
            if segment == "this":
                self.load_segment_index("THIS", index)
            if segment == "that":
                self.load_segment_index("THAT", index)
            if segment == "constant":
                self.write_to_asm(f"@{i}")
                self.write_to_asm("D=A")
                self.push_D_to_stack()
            if segment == "static":
                self.write_to_asm(f"@{self.__current_file}.{i}")
            if segment == "temp":
                temp_index = 5 + index
                self.write_to_asm(f"@R{str(temp_index)}")
            if segment == "pointer":
                # if index == 0 then we go to "THIS" segment, which is R3
                # if index == 1, then we go to "THAT" segment, which is R4.
                # therefore the Register R3+index will always gives the wanted Register
                pointer_index = 3 + index
                self.write_to_asm(f"@R{str(pointer_index)}")
            if segment != "constant":
                self.write_to_asm("D=M")
                self.push_D_to_stack()
            
        if command == "C_POP":
            if segment == "local":
                self.load_segment_index("LCL", index)
            if segment == "argument":
                self.load_segment_index("ARG", index)
            if segment == "this":
                self.load_segment_index("THIS", index)
            if segment == "that":
                self.load_segment_index("THAT", index)
            if segment == "static":
                self.write_to_asm(f"@{self.__current_file}.{i}") 
            if segment == "temp":
                temp_index = 5 + index
                self.write_to_asm(f"@R{str(temp_index)}")
            if segment == "pointer":
                pointer_index = 3 + index
                self.write_to_asm(f"@R{str(pointer_index)}")
            self.write_to_asm("D=A")
            self.write_to_asm("@R13")
            self.write_to_asm("M=D")
            self.pop_stack_to_D()
            self.write_to_asm("@R13")
            self.write_to_asm("A=M")
            self.write_to_asm("M=D")

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass

    def push_D_to_stack(self):
        """push the value from D into the top of the stack"""
        self.write_to_asm("@SP")
        self.write_to_asm("A=M")
        self.write_to_asm("M=D")
        self.increment_SP()

    def pop_stack_to_D(self):
        """pop the value from the top of the stack into D"""
        self.decrement_SP()
        self.write_to_asm("A=M")
        self.write_to_asm("D=M")

    def increment_SP(self):
        self.write_to_asm("@SP")
        self.write_to_asm("M=M+1")

    def decrement_SP(self):
        self.write_to_asm("@SP")
        self.write_to_asm("M=M-1")

    def add_sub_arithmetic(self, command: str):
        self.pop_stack_to_D()
        self.decrement_SP()
        self.write_to_asm("@SP")
        self.write_to_asm("A=M")
        if command == "add":
            self.write_to_asm("M=D+M")
        else:  # command == "sub"
            self.write_to_asm("M=M-D")
        self.increment_SP()

    def bool_arithmetic(self, command: str):
        """This function handles the boolian commands:
            'and, 'or', 'not', 'neg'"""
        if command == "and" or command == "or":
            self.pop_stack_to_D()
        self.decrement_SP()
        self.write_to_asm("@SP")
        self.write_to_asm("A=M")
        if command == "and":
            self.write_to_asm("M=D&M")
        elif command == "or":
            self.write_to_asm("M=D|M")
        elif command == "not":
            self.write_to_asm("M=!M")
        else:  # if command == "neg"
            self.write_to_asm("M=-M")
        self.increment_SP()

    def eq_gt_lt(self, command: str):
        jump_label = "Label" + str(self.__label_number)
        self.__label_number += 1
        self.pop_stack_to_D()
        self.decrement_SP()
        self.write_to_asm("A=M")
        self.write_to_asm("D=M-D")
        self.write_to_asm("M=-1")
        self.increment_SP()
        self.write_to_asm(f"@{jump_label}")
        if command == "eq":
            self.write_to_asm("D;JEQ")
        if command == "gt":
            self.write_to_asm("D;JGT")
        if command == "lt":
            self.write_to_asm("D;JLT")
        self.write_to_asm("@SP")
        self.write_to_asm("A=M-1")
        self.write_to_asm("M=0")
        self.write_to_asm(f"({jump_label})")

    def shiftleft_shiftright(self, command: str):
        self.decrement_SP()
        self.write_to_asm("@SP")
        self.write_to_asm("A=M")
        if command == "shiftleft":
            self.write_to_asm("M=<<M")
        else:  # command == "shiftright"
            self.write_to_asm("M=>>M")
            
    def load_segment_index(self, segment: str, index: int):
        self.write_to_asm("@" + segment)
        self.write_to_asm("D=M")
        self.write_to_asm("@" + str(index))
        self.write_to_asm("A=D+A")
        
    def write_to_asm(self, command: str):
        command += "\n"
        self.__asm_file.write(command)

    def close_file(self):
        self.__asm_file.close()
