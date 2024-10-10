"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from typing import Optional
import typing

class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:

        self.__file_lines: list = input_file.read().splitlines()
        self.__input_lines: list = []
        for line in self.__file_lines:
            line = self.remove_spaces(self.remove_comments(line))
            if line:
                self.__input_lines.append(line)
        self.__command_number: int = -1
        self.__current_command: Optional[str] = None
        self.__command_type: str = ""

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return len(self.__input_lines) - 1 > self.__command_number

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        self.__command_number += 1
        self.__current_command = self.__input_lines[self.__command_number]
        # commentsless_command = self.remove_comments(self.__input_lines[self.__command_number])
        # self.__current_command = self.remove_spaces(commentsless_command)
        # while self.__current_command == "":
        #     self.__command_number += 1
        #     self.__current_command = self.remove_comments(self.__input_lines[self.__command_number])

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self.__current_command[0] == "@":
            self.__command_type = "A_COMMAND"
            return "A_COMMAND"
        if self.__current_command[0] == "(":
            self.__command_type = "L_COMMAND"
            return "L_COMMAND"
        else:
            self.__command_type = "C_COMMAND"
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        # Your code goes here!
        if self.__command_type == "A_COMMAND":
            return self.__current_command[1:]
        if self.__command_type == "L_COMMAND":
            return self.__current_command[1:-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if "=" in self.__current_command:
            dest = self.__current_command.split("=")[0]
            return dest
        return ""

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        comp = self.__current_command
        if "=" in comp:
            comp = comp.partition("=")[2]
        comp = comp.partition(";")[0]
        return comp

        # if "=" in self.__current_command:
        #     comp = self.__current_command.split("=")[1]
        # else:
        #     comp = self.__current_command.split(";")[0]
        # return comp


    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if ";" in self.__current_command:
            jump = self.__current_command.split(";")[-1]
            return jump
        return ""

    def remove_spaces(self, command: str) -> str:
        return "".join(command.split())

    def remove_comments(self, command: str) -> str:
        return command.split("//")[0]
    
    def get_command_number(self) -> int:
        return self.__command_number

    def get_current_command(self):
        return self.__current_command

    def is_not_command(self, line):
        return line[0:2] == "//" or not line

    def restart(self) -> None:
        """Restarts the parser for reprocessing."""
        self.__current_command = ""
        self.__command_number = -1
        