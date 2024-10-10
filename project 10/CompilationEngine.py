"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from typing import Optional
from JackTokenizer import *


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    OP_LIST = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
    UNARY_OP_LIST = ['-', '~', '^', '#']
    
    def __init__(self, input_stream: JackTokenizer, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.__tokenizer = input_stream
        # self.__token_stream.read()
        self.__output_stream = open(output_stream.name, "w+")
        # self.__curr_indentation: int = 0

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # class: 'class' className '{' classVarDec* subroutineDec* '}'
        # Your code goes here!
        if self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            self.open_tag("class")
            self.new_line()
            if self.is_expected_token(["class"]):
                self.write_xml_line("keyword")  # <keyword> class </keyword>
            if self.is_identifier():
                # <identifier> className </identifier>
                self.write_xml_line("identifier")
            if self.is_expected_token(["{"]):
                self.write_xml_line("symbol")  # <symbol> { </symbol>
            while self.current_token() in ('static', 'field'):
                self.compile_class_var_dec()
            while self.current_token() in ('constructor', 'function', 'method'):
                self.compile_subroutine()
            if self.is_expected_token(["}"]):
                self.write_xml_line("symbol")  # <symbol> } </symbol>
            self.close_tag("class")
        self.new_line()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        # Your code goes here!
        self.open_tag("classVarDec")
        self.new_line()
        if self.is_expected_token(['static', 'field']):
            # <keyword> (static | field) </keyword>
            self.write_xml_line("keyword")
        # types
        if self.is_keyword():
            # <keyword> (int | char | boolean) </keyword>
            self.write_xml_line("keyword")
        elif self.is_identifier():
            # <identifier> className </identifier>
            self.write_xml_line("identifier")
        if self.is_identifier():
            self.write_xml_line("identifier")
        while self.__tokenizer.symbol() == ",":  # (',' varName)*
            self.write_xml_line("symbol")  # <symbol> , </symbol>
            # <identifier> varName </identifier>
            self.write_xml_line("identifier")
        self.write_xml_line("symbol")  # <symbol> ; </symbol>
        self.close_tag("classVarDec")
        self.new_line()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        # subroutineDec: ('constructor' | 'function' | 'method') ('void' | type)
        # subroutineName '('parameterList')' subroutineBody
        self.open_tag("subroutineDec")
        self.new_line()
        if self.is_expected_token(['constructor', 'function', 'method']):
            # <keyword> ('constructor' | 'function' | 'method') </keyword>
            self.write_xml_line("keyword")
        if self.is_keyword():  # current_token is 'void' or type ('int', 'char', 'boolean')
            # <keyword> (void | int | char | boolean) </keyword>
            self.write_xml_line("keyword")
        elif self.is_identifier():  # type className
            # <identifier> className </identifier>
            self.write_xml_line("identifier")
        if self.is_identifier():
            # <identifier> subroutineName </identifier>
            self.write_xml_line("identifier")
        if self.is_expected_token(["("]):
            self.write_xml_line("symbol")  # <symbol> ( </symbol>
        self.compile_parameter_list()  # 'parameterList' - optional
        if self.is_expected_token([")"]):
            self.write_xml_line("symbol")  # <symbol> ) </symbol>
        # self.compile_subroutine_body()
        # subroutineBody: '{' varDec* statements '}'
        self.open_tag("subroutineBody")  # <subroutineBody>
        self.new_line()
        if self.is_expected_token(["{"]):
            self.write_xml_line("symbol")  # <symbol> { </symbol>
        while self.current_token() == 'var':
            self.compile_var_dec()  # varDec: 'var' type varName (',' varName)* ';'
        self.compile_statements()
        if self.is_expected_token(["}"]):
            self.write_xml_line("symbol")  # <symbol> } </symbol>
        self.close_tag("subroutineBody")
        self.new_line()
        self.close_tag("subroutineDec")
        self.new_line()

    def compile_subroutine_body(self):
        """compiles a subroutine body"""
        # subroutineBody: '{' varDec* statements '}'
        if self.is_expected_token(["{"]):
            self.write_xml_line("symbol")  # <symbol> { </symbol>
        while self.current_token() == 'var':
            self.compile_var_dec()  # varDec: 'var' type varName (',' varName)* ';'
        self.compile_statements()
        if self.is_expected_token(["}"]):
            self.write_xml_line("symbol")  # <symbol> } </symbol>
        self.close_tag("subroutineBody")
        self.new_line()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # parameterList: ((type varName) (',' type varName)*)?
        # Your code goes here!
        self.open_tag("parameterList")
        self.new_line()
        if self.current_token() != ")":
            """type: 'int' | 'char' | 'boolean' | className"""
            if self.is_keyword():  # if type is 'int', 'char' or 'boolean'
                # <keyword> ('int' | 'char' | 'boolean') </keyword>
                self.write_xml_line("keyword")
            elif self.is_identifier(): # if type is classNmae
                self.write_xml_line("identifier")  # <identifier> className </identifier>
            else:
                raise TypeError
            if self.is_identifier():
                self.write_xml_line("identifier")  # <identifier> varName </identifier>
            # (',' type varName)* - 0 or more times
            while self.__tokenizer.symbol() == ",":
                self.write_xml_line("symbol")  # <symbol> , </symbol>
                """type: ('int' | 'char' | 'boolean' | className)"""
                if self.is_keyword():  # if type is 'int', 'char' or 'boolean'
                    # <keyword> ('int' | 'char' | 'boolean') </keyword>
                    self.write_xml_line("keyword")
                elif self.is_identifier():  # if type is classNmae
                    self.write_xml_line("identifier")  # <identifier> className </identifier>
                else:
                    raise TypeError
                if self.is_identifier():
                    self.write_xml_line("identifier")  # <identifier> varName </identifier>
        self.close_tag("parameterList")
        self.new_line()

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # varDec: 'var' type varName (',' varName)* ';'
        # Your code goes here!
        self.open_tag("varDec")
        self.new_line()
        self.write_xml_line("keyword")  # <keyword> var </keyword>
        if self.is_keyword():  # type is ('int' | 'char' | 'boolean')
            self.write_xml_line("keyword")  # <keyword> ('int' | 'char' | 'boolean') </keyword>
        elif self.is_identifier():  # type is className
            self.write_xml_line("identifier")  # <identifier> className </identifier>
        else:
            raise TypeError
        if self.is_identifier():
            self.write_xml_line("identifier")  # <identifier> varName </identifier>
        while self.is_symbol() and self.__tokenizer.symbol() == ",":
            self.write_xml_line("symbol")  # <symbol> , </symbol>
            if self.is_identifier():
                self.write_xml_line("identifier") #<identifier> varName </identifier>
        if self. is_expected_token([";"]):
            self.write_xml_line("symbol") # <symbol> ; </symbol>
        self.close_tag("varDec")
        self.new_line()

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # statements: statement*
        # statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement
        # Your code goes here!
        self.open_tag("statements")  # <statement>
        self.new_line()
        while self.is_keyword() and self.is_expected_token(['let', 'if', 'while', 'do', 'return']):
            if self.__tokenizer.keyword() == "LET":
                self.compile_let()
            elif self.__tokenizer.keyword() == "IF":
                self.compile_if()
            elif self.__tokenizer.keyword() == "WHILE":
                self.compile_while()
            elif self.__tokenizer.keyword() == "DO":
                self.compile_do()
            elif self.__tokenizer.keyword() == "RETURN":
                self.compile_return()
        self.close_tag("statements")
        self.new_line()

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # doStatement: 'do' subroutineCall ';'
        # subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName
        # '(' expressionList ')'
        # Your code goes here!
        self.open_tag("doStatement")
        self.new_line()
        if self.is_expected_token(["do"]):
            self.write_xml_line("keyword")  # <keyword> do </keyword>
        if self.is_identifier():
            self.write_xml_line("identifier")  # <identifier> (subroutineName | classNmae | varName) </identifier>
        if self.is_symbol() and self.__tokenizer.symbol() == '(':
            self.write_xml_line("symbol")  # <symbol> ( </symbol>
            self.compile_expression_list()
            if self.is_expected_token([")"]):
                self.write_xml_line("symbol")  # <symbol> ) </symbol>
        elif self.is_symbol() and self.__tokenizer.symbol() == ".":
            self.write_xml_line("symbol")  # <symbol> . </symbol>
            if self.is_identifier():
                self.write_xml_line("identifier")  # <identifier> subroutineName </identifier>
                if self.is_symbol() and self.__tokenizer.symbol() == '(':
                    self.write_xml_line("symbol")  # <symbol> ( </symbol>
                    self.compile_expression_list()
                    if self.is_expected_token([")"]):
                        self.write_xml_line("symbol")  # <symbol> ) </symbol>
        if self.is_expected_token([";"]): 
            self.write_xml_line("symbol")  # <symbol> ; </symbol>
        self.close_tag("doStatement")
        self.new_line()

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
        # Your code goes here!
        self.open_tag("letStatement")  # <letStatement>
        self.new_line()
        if self.is_expected_token(["let"]):
            self.write_xml_line("keyword")  # <keyword> let </keyword>
        if self.is_identifier(): 
            self.write_xml_line("identifier")  # <identifier> varName </identifier>
        if self.is_symbol() and self.__tokenizer.symbol() == '[':
            self.write_xml_line("symbol")  # <symbol> [ </symbol>
            self.compile_expression()
            if self.is_expected_token(["]"]):
                self.write_xml_line("symbol")  # <symbol> ] </symbol>
        if self.is_expected_token(["="]):
            self.write_xml_line("symbol")  # <symbol> = </symbol>
        self.compile_expression()
        if self.is_expected_token([";"]):
            self.write_xml_line("symbol")  # <symbol> ; </symbol>
        self.close_tag("letStatement")  # </letStatement>
        self.new_line()

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
        # Your code goes here!
        self.open_tag("whileStatement")  # <whileStatement>
        self.new_line()
        if self.is_expected_token(['while']):
            self.write_xml_line("keyword")  # <keyword> 'while' </keyword>
        if self.is_expected_token(["("]):  # checks if the current token is '('
            self.write_xml_line("symbol")  # <symbol> ( </symbol>
        self.compile_expression()  # compile the expression that between the brackets
        if self.is_expected_token([")"]):
            self.write_xml_line("symbol")  # <symbol> ) </symbol>
        if self.is_expected_token(["{"]):  # checks if the current token is '{'
            self.write_xml_line("symbol")  # <symbol> { </symbol>
        self.compile_statements()  # compile the statements that between the brackets
        if self.is_expected_token(["}"]):  # checks if the current token is '}'
            self.write_xml_line("symbol")  # <symbol> } </symbol>
        self.close_tag("whileStatement")  # </whileStatement>
        self.new_line()

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # returnStatement: 'return' expression? ';'
        # Your code goes here!
        self.open_tag("returnStatement")  # <returnStatement>
        self.new_line()
        if self.is_expected_token(["return"]):
            self.write_xml_line("keyword")  # <keyword> return </keyword>
        if not self.is_symbol():  # current token isn't ';'
            self.compile_expression()
        if self.is_expected_token([';']):
            self.write_xml_line("symbol")  # <symbol> ; </symbol>
        self.close_tag("returnStatement")  # </returnStatement>
        self.new_line()

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        # Your code goes here!
        self.open_tag("ifStatement") # <ifStatement>
        self.new_line()
        if self.is_expected_token(["if"]):
            self.write_xml_line("keyword")  # <keyword> if </keyword>
        if self.is_expected_token(["("]):
            self.write_xml_line("symbol")  # <symbol> ( </symbol>
        self.compile_expression()
        if self.is_expected_token([")"]):
            self.write_xml_line("symbol")  # <symbol> ) </symbol>
        if self.is_expected_token(["{"]):
            self.write_xml_line("symbol")  # <symbol> { </symbol>
        self.compile_statements()
        if self.is_expected_token(["}"]):
            self.write_xml_line("symbol")  # <symbol> } </symbol>
        if self.is_keyword() and self.__tokenizer.keyword() == "ELSE":
            self.write_xml_line("keyword")  # <keyword> else </keyword>
            if self.is_expected_token(["{"]):
                self.write_xml_line("symbol")  # <symbol> { </symbol>
            self.compile_statements()
            if self.is_expected_token(["}"]):
                self.write_xml_line("symbol")  # <symbol> } </symbol>
        self.close_tag("ifStatement")
        self.new_line()

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # expression: term (op term)*
        # Your code goes here!
        self.open_tag("expression")  # <expression>
        self.new_line()
        self.compile_term()
        while self.is_symbol() and self.__tokenizer.symbol() in self.OP_LIST:
            self.write_xml_line("symbol")  # <symbol> op </symbol>
            self.compile_term()
        self.close_tag("expression")
        self.new_line()

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # term: integerConstant | stringConstant | keywordConstant | varName |
        # varName '['expression']' | subroutineCall | '(' expression ')' | unaryOp term
        # Your code goes here!
        self.open_tag("term")  # <term>
        self.new_line()
        if self.__tokenizer.token_type() == "INT_CONST":
            self.write_xml_line("integerConstant")  # <integerConstant> integerConstant </integerConstant>
        elif self.__tokenizer.token_type() == "STRING_CONST":
            self.write_xml_line("stringConstant")  # <string> stringConstant </string>
        elif self.__tokenizer.token_type() == "KEYWORD":
            self.write_xml_line("keyword")  # <keyword> keywordConstant </keyword>
        elif self.__tokenizer.token_type() == "IDENTIFIER":
            self.write_xml_line("identifier")  # <identifier> (varName | className | subroutineName) </identifier>
            if self.is_symbol() and self.__tokenizer.symbol() == "[":  # varName '['expression']' case
                self.write_xml_line("symbol")  # <symbol> [ </symbol>
                self.compile_expression()
                if self.is_expected_token(["]"]):
                    self.write_xml_line("symbol")  # <symbol> ] </symbol>
            elif self.is_symbol() and self.__tokenizer.symbol() == "(":  # subroutineName '(' expressionList ')' case
                self.write_xml_line("symbol")  # <symbol> ( </symbol>
                self.compile_expression_list()
                if self.is_expected_token([")"]):
                    self.write_xml_line("symbol")  # <symbol> ) </symbol>
            elif self.is_symbol() and self.__tokenizer.symbol() == ".":  # (className | varName) '.' subroutineName '(' expressionList ')'
                self.write_xml_line("symbol")  # <symbol> . </symbol>
                if self.is_identifier():
                    self.write_xml_line("identifier")  # <identifier> subroutineName </identifier>
                if self.is_symbol() and self.__tokenizer.symbol() == "(":  # subroutineName '(' expressionList ')' case
                    self.write_xml_line("symbol")  # <symbol> ( </symbol>
                    self.compile_expression_list()
                if self.is_expected_token([")"]):
                    self.write_xml_line("symbol")  # <symbol> ) </symbol>
        elif self.is_symbol() and self.__tokenizer.symbol() == "(":  # '(' expression ')' case
            self.write_xml_line("symbol")  # <symbol> ( </symbol>
            self.compile_expression()
            if self.is_expected_token([")"]):
                self.write_xml_line("symbol")  # <symbol> ) </symbol>
        elif self.is_symbol() and self.__tokenizer.symbol() in self.UNARY_OP_LIST:  # unaryOp term
            self.write_xml_line("symbol")  # <symbol> unaryOp </symbol>
            self.compile_term()
        self.close_tag("term")  # </term>
        self.new_line()

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # expressionList: (expression (',' expression)* )?
        # Your code goes here!
        self.open_tag("expressionList") # <expressionList>
        self.new_line()
        start_symbols = self.UNARY_OP_LIST + ["("]
        if not self.is_symbol() or self.__tokenizer.symbol() in start_symbols:
            self.compile_expression()
        while self.is_symbol() and self.__tokenizer.symbol() == ",":
            self.write_xml_line("symbol") # <symbol> , </symbol>
            self.compile_expression()
        self.close_tag("expressionList") # </expressionList>
        self.new_line()

    def is_expected_token(self, expected_list: list[str]) -> Optional[bool]:
        """If the current token is different than all the string options we expect to get,
           an error is raised. else, return True.
           Note that is_expected_token function should be called ONLY if the next token has to
           be one of the expected_list of tokens. if it COULD be a token from this list, but not HAS TO, we
           should use other conditions."""
        for element in expected_list:
            if self.current_token() == element:
                return True
        raise NameError

    def open_tag(self, tag_name: str) -> None:
        """Writes the open tag for the .xml file."""
        tag = f"<{tag_name}>"
        self.write_to_xml(tag)

    def close_tag(self, tag_name: str) -> None:
        """Writes the close tag for the .xml file."""
        tag = f"</{tag_name}>"
        self.write_to_xml(tag)

    def write_to_xml(self, text: str) -> None:
        """Writes any string we wish to the .xml file."""
        self.__output_stream.write(text)

    def new_line(self) -> None:
        """Starts a new line in the .xml file."""
        self.write_to_xml("\n")

    def indentation(self) -> None:
        """Make the wanted indentation indentation in the .xml file."""
        for _ in range(self.__curr_indentation):
            self.write_to_xml("  ")

    def current_token(self) -> str:
        """Return the current token."""
        return self.__tokenizer.get_current_token()

    def write_current_token(self) -> None:
        """Writes the next token from the tokenizer."""
        if self.__tokenizer.token_type() == "KEYWORD":
            token = self.__tokenizer.keyword().lower()
        elif self.__tokenizer.token_type() == "SYMBOL":
            token = self.__tokenizer.symbol()
            if token == '&':
                token = '&amp;'
            elif token == '<':
                token = '&lt;'
            elif token == '>':
                token = '&gt;'
        elif self.__tokenizer.token_type() == "IDENTIFIER":
            token = self.__tokenizer.identifier()
        elif self.__tokenizer.token_type() == "INT_CONST":
            token = str(self.__tokenizer.int_val())
        elif self.__tokenizer.token_type() == "STRING_CONST":
            token = self.__tokenizer.string_val()
        else:
            raise TypeError
        self.write_to_xml(f" {token} ")

    def write_xml_line(self, tag: str):
        self.open_tag(f"{tag}")  # <tag>
        self.write_current_token()
        self.close_tag(f"{tag}")  # </tag>
        self.new_line()
        if self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()

    def is_keyword(self) -> bool:
        if self.__tokenizer.token_type() == 'KEYWORD':
            return True
        return False
    
    def is_symbol(self) -> bool:
        if self.__tokenizer.token_type() == "SYMBOL":
            return True
        return False

    def is_identifier(self) -> bool:
        if self.__tokenizer.token_type() == 'IDENTIFIER':
            return True
        return False

    def is_string_const(self) -> bool:
        if self.__tokenizer.token_type() == 'STRING_CONST':
            return True
        return False

    def is_int_const(self) -> bool:
        if self.__tokenizer.token_type() == 'INT_CONST':
            return True
        return False

