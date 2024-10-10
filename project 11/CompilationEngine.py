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
from SymbolTable import *
from VMWriter import *


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    OP_LIST = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
    UNARY_OP_LIST = ['-', '~', '^', '#']
    ARITHMETIC = {
        '+': 'add',
        '-': 'sub',
        '=': 'eq',
        '>': 'gt',
        '<': 'lt',
        '&': 'and',
        '|': 'or'
    }

    ARITHMETIC_UNARY = {
        '-': 'neg',
        '~': 'not'
    }
    
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
        self.__output_stream = open(output_stream.name, "w+")
        self.__symbol_table = SymbolTable()
        self.__vm_writer = VMWriter(self.__output_stream)
        self.__class_name = ''
        self.__subroutine_type = ''
        self.__subroutine_name = ''
        self.__return_type = ''
        self.__curr_indentation = ''
        self.__while_labels_count = 0
        self.__if_labels_count = 0
        self.__n_args = 0

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # class: 'class' className '{' classVarDec* subroutineDec* '}'
        # Your code goes here!
        if self.__tokenizer.has_more_tokens():
            self.next_token()  # 'class'
            self.next_token()  # className
            self.__class_name = self.current_token()
            self.next_token()  # '{'
            self.next_token()
            while self.current_token() in ('static', 'field'):
                self.compile_class_var_dec()  # classVarDec*
                self.next_token()
            while self.current_token() in ('constructor', 'function', 'method'):
                self.compile_subroutine()  # subroutineDec*
                if self.__tokenizer.has_more_tokens():
                    self.next_token()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        # Your code goes here!
        # checks if there are static vars or field vars to add to the symbol table
        # get the name, type and kind of the next token
        var_kind = self.current_token().upper()
        self.next_token()  # type ('int', 'char', 'boolean', className)
        var_type = self.current_token()
        self.next_token()
        var_name = self.current_token()
        self.__symbol_table.define(var_name, var_type, var_kind)  # adds the current token to the symbol table
        self.next_token()
        while self.current_token() == ",":  # (',' varName)*, there is another class var declaration
            self.next_token()  # varName
            var_name = self.current_token()
            self.__symbol_table.define(var_name, var_type, var_kind)
            self.next_token()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        # subroutineDec: ('constructor' | 'function' | 'method') ('void' | type)
        # subroutineName '('parameterList')' subroutineBody
        self.__symbol_table.start_subroutine()
        self.__if_labels_count = 0
        self.__while_labels_count = 0
        self.__subroutine_type = self.current_token()  # 'constructor' | 'function' | 'method'
        self.next_token()  # ('void' | type)
        self.__return_type = self.current_token()
        self.next_token()  # subroutineName
        self.__subroutine_name = self.current_token()
        if self.__subroutine_type == 'method':
            self.__symbol_table.define('this', self.__class_name, 'ARG')
        self.next_token()  # '('
        self.next_token()  # parameterList
        self.compile_parameter_list()
        self.next_token()  # '{'
        self.compile_subroutine_body()

    def compile_subroutine_body(self):
        """compiles a subroutine body"""
        # subroutineBody: '{' varDec* statements '}'
        self.next_token()  # varDec*
        while self.current_token() == 'var':
            self.compile_var_dec()  # varDec: 'var' type varName (',' varName)* ';'
            self.next_token()
        function_name = f"{self.__class_name}.{self.__subroutine_name}"
        lcl_num = self.__symbol_table.var_count('VAR')
        self.__vm_writer.write_function(function_name, lcl_num)
        if self.__subroutine_type == 'constructor':
            var_count = self.__symbol_table.var_count("FIELD")
            self.__vm_writer.write_push('constant', var_count)  # push constant that is the amount of arguments/fields
            self.__vm_writer.write_call('Memory.alloc', 1)  # allocate space in the RAM of the previous constant
            self.__vm_writer.write_pop('pointer', 0)  # pop the index in the ram allocated before into pointer 0 (this)
        if self.__subroutine_type == 'method':
            self.__vm_writer.write_push('argument', 0)  # push argument 0, which represents of the current object (this)
            self.__vm_writer.write_pop('pointer', 0)  # pop it to pointer 0, to anchor it into this segment
        self.compile_statements()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # parameterList: ((type varName) (',' type varName)*)?
        # Your code goes here!
        if self.current_token() != ')':
            cur_type = self.current_token()
            self.next_token()  # varName
            self.__symbol_table.define(self.current_token(), cur_type, 'ARG')  # (varName, type, ARG)
            self.next_token()
            while self.current_token() == ',':
                self.next_token()  # type ('int' | 'char' | 'boolean', className)
                cur_type = self.current_token()
                self.next_token()  # varName
                self.__symbol_table.define(self.current_token(), cur_type, 'ARG')  # (varName, type, ARG)
                self.next_token()

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # varDec: 'var' type varName (',' varName)* ';'
        # Your code goes here!
        self.next_token()  # type (int | char | boolean | className)
        var_type = self.current_token()
        self.next_token()  # varName
        var_name = self.current_token()
        self.__symbol_table.define(var_name, var_type, 'LCL')
        self.next_token()
        while self.current_token() == ',':
            self.next_token()  # varName
            var_name = self.current_token()
            self.__symbol_table.define(var_name, var_type, 'LCL')
            self.next_token()

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # statements: statement*
        # statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement
        # Your code goes here!
        while self.current_token() in ('let', 'if', 'while', 'do', 'return'):
            if self.current_token() == "let":
                self.compile_let()
            elif self.current_token() == "if":
                self.compile_if()
            elif self.current_token() == "while":
                self.compile_while()
            elif self.current_token() == "do":
                self.compile_do()
            elif self.current_token() == "return":
                self.compile_return()
            self.next_token()

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # doStatement: 'do' subroutineCall ';'
        # subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName
        # '(' expressionList ')'
        # Your code goes here!
        self.next_token()  # subroutineCall
        self.compile_term()  # subroutineCall is kind of term
        self.__vm_writer.write_pop('temp', 0)  # pop to avoid filling the stack with garbage
        self.next_token()  # ';'

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
        # Your code goes here!
        self.next_token()  # varName
        var_name = self.current_token()
        var_kind = self.__symbol_table.kind_of(var_name)
        var_index = self.__symbol_table.index_of(var_name)
        self.next_token()  # '[' or '='
        if self.current_token() == '[':  # if varName is an array, we have to do some array manipulations in VM code
            self.next_token()  # expression1
            # VM code for array assignment
            # VM code for computing and pushing the value of the expression1
            self.compile_expression()
            self.__vm_writer.write_push(self.correct_var_kind(var_kind), var_index)
            self.__vm_writer.write_arithmetic('ADD')  # top stack value = RAM address of arr[expression1
            self.next_token()  # '='
            self.next_token()  # expression2
            # VM code for computing and pushing the value of the expression2
            self.compile_expression()
            self.__vm_writer.write_pop('temp', 0)
            # temp0 = the value of expression2
            # top stack value = RAM address of arr[expression1]
            self.__vm_writer.write_pop('pointer', 1)
            self.__vm_writer.write_push('temp', 0)
            self.__vm_writer.write_pop('that', 0)
        else:  # varName is not an array
            self.next_token()  # expression
            self.compile_expression()
            # pop the value of the expression into the address of the var
            self.__vm_writer.write_pop(self.correct_var_kind(var_kind), var_index)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # whileStatement: 'while' '(' expression ')' '{' statements '}'
        # Your code goes here!
        self.next_token()  # '('
        self.next_token()  # expression
        label1 = f"WHILE_EXP{self.__while_labels_count}"
        label2 = f"WHILE_END{self.__while_labels_count}"
        self.__vm_writer.write_label(label1)
        self.compile_expression()
        self.__vm_writer.write_arithmetic('NOT')  # negate the compiled expression
        self.__vm_writer.write_if(label2)
        self.next_token()  # '{'
        self.next_token()  # statements
        self.__while_labels_count += 1
        self.compile_statements()
        self.__vm_writer.write_goto(label1)
        self.__vm_writer.write_label(label2)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # returnStatement: 'return' expression? ';'
        # Your code goes here!
        self.next_token()  # expression (this) | ;
        if self.current_token() == 'this':
            self.__vm_writer.write_push('pointer', 0)
            self.next_token()  # ';'
        elif self.current_token() != ';':
            self.compile_expression()
        else:  # the statement is: 'return;'
            self.__vm_writer.write_push('constant', 0)
        self.__vm_writer.write_return()

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        # Your code goes here!
        self.next_token()  # '('
        true_label = f"IF_TRUE{self.__if_labels_count}"
        false_label = f"IF_FALSE{self.__if_labels_count}"
        end_label = f"IF_END{self.__if_labels_count}"
        self.next_token()  # expression
        self.compile_expression()
        self.next_token()  # '{'
        self.__vm_writer.write_if(true_label)
        self.__vm_writer.write_goto(false_label)
        self.__vm_writer.write_label(true_label)
        self.next_token()  # statements
        self.__if_labels_count += 1
        self.compile_statements()
        self.next_token()

        if self.current_token() != 'else':
            self.__vm_writer.write_label(false_label)
            self.prev_token()

        else:  # there is else clause in this if statement
            self.next_token()  # '{'
            self.next_token()  # statements
            self.__vm_writer.write_goto(end_label)
            self.__vm_writer.write_label(false_label)
            self.compile_statements()
            self.__vm_writer.write_label(end_label)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # expression: term (op term)*
        # Your code goes here!
        self.compile_term()
        self.next_token()
        while self.current_token() in self.OP_LIST:
            op = self.current_token()
            self.next_token()
            self.compile_term()
            if op == '*':
                self.__vm_writer.write_call('Math.multiply', 2)
            elif op == '/':
                self.__vm_writer.write_call('Math.divide', 2)
            else:  # op is in OP_LIST but isn't '*' nor '/'
                op = CompilationEngine.ARITHMETIC[op]
                self.__vm_writer.write_arithmetic(op)
            self.next_token()

    def compile_subroutine_call(self, identifier_name: str):
        # subroutineCall: subroutineName '(' expressionList ')' | (className | varName)
        # '.' subroutineName '(' expressionList ')'
        self.__n_args = 0
        if self.current_token() == '(':
            subroutine_name = identifier_name
            function_name = f"{self.__class_name}.{subroutine_name}"
            self.__n_args += 1
            self.__vm_writer.write_push('pointer', 0)
            self.prev_token()
        elif self.current_token() == '.':
            self.next_token()  # subroutineName
            subroutine_name = self.current_token()
            identifier_type = self.__symbol_table.type_of(identifier_name)
            if identifier_type is None:  # identifier is a class_name
                class_name = identifier_name
                function_name = f"{class_name}.{subroutine_name}"
            else:  # identifier is the varName
                var_kind = self.__symbol_table.kind_of(identifier_name)
                var_ind = self.__symbol_table.index_of(identifier_name)
                self.__vm_writer.write_push(self.correct_var_kind(var_kind), var_ind)
                function_name = f"{identifier_type}.{subroutine_name}"
                self.__n_args += 1
        else:
            raise NameError
        self.next_token()  # '('
        self.compile_expression_list()
        self.__vm_writer.write_call(function_name, self.__n_args)

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
        if self.__tokenizer.token_type() == "INT_CONST":
            self.__vm_writer.write_int_const(int(self.current_token()))
        elif self.__tokenizer.token_type() == "STRING_CONST":
            self.__vm_writer.write_string_const(self.current_token())
        elif self.__tokenizer.token_type() == "KEYWORD":
            if self.current_token() == 'this':
                self.__vm_writer.write_push('pointer', 0)
            else:
                self.__vm_writer.write_int_const(0)  # null / false
                if self.current_token() == 'true':
                    self.__vm_writer.write_arithmetic('NOT')
            # if self.current_token() == 'true':
            #     self.__vm_writer.write_push('constant', 1)
            #     self.__vm_writer.write_arithmetic('NEG')
            # elif self.current_token() in ['null', 'false']:
            #     self.__vm_writer.write_push('constant', 0)

        # in case of function call or variable name
        elif self.__tokenizer.token_type() == "IDENTIFIER":
            var_kind = self.__symbol_table.kind_of(self.current_token())
            var_ind = self.__symbol_table.index_of(self.current_token())
            identifier_name = self.current_token()
            self.next_token()
            if self.current_token() == '[':  # we have an Array var, so we need to do some Array manipulations
                self.next_token()  # expression
                self.compile_expression()
                self.__vm_writer.write_push(self.correct_var_kind(var_kind), var_ind)
                self.__vm_writer.write_arithmetic('ADD')  # top stack value = RAM address of arr[expression]
                # top stack value = RAM address of arr[expression]
                # rebase 'that' to point at var+ind
                self.__vm_writer.write_pop('pointer', 1)
                self.__vm_writer.write_push('that', 0)
            elif self.current_token() in ['.', '(']:  # subroutineCall case
                self.compile_subroutine_call(identifier_name)
            else:  # varName case
                self.__vm_writer.write_push(self.correct_var_kind(var_kind), var_ind)
                self.prev_token()
        elif self.current_token() == '(':  # '(' expression ')' case
            self.next_token()  # expression
            self.compile_expression()
        elif self.current_token() in ('-', '~'):  # unaryOp term case
            symbol = self.current_token()
            if symbol == '-':
                sym_to_write = 'NEG'
            else:  # symbol == '~'
                sym_to_write = 'NOT'
            self.next_token()
            self.compile_term()
            self.__vm_writer.write_arithmetic(sym_to_write)

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # expressionList: (expression (',' expression)* )?
        # Your code goes here!
        self.next_token()
        if self.current_token() != ')':  # then there is an expression to compile
            self.compile_expression()
            self.__n_args += 1
            while self.is_symbol() and self.current_token() == ",":
                self.__n_args += 1
                self.next_token()  # expression
                self.compile_expression()

    def is_expected_token(self, expected_list: list[str]) -> Optional[bool]:
        """If the current token is different from all the string options we expect to get,
           an error is raised. else, return True.
           Note that is_expected_token function should be called ONLY if the next token has to
           be one of the expected_list of tokens. if it COULD be a token from this list, but not HAS TO, we
           should use other conditions."""
        for element in expected_list:
            if self.current_token() == element:
                return True
        return False

    def current_token(self) -> str:
        """Return the current token."""
        return self.__tokenizer.get_current_token()

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

    def identifier_type(self, name: str):
        return self.__symbol_table.type_of(name)
    
    def identifier_kind(self, name: str):
        return self.__symbol_table.kind_of(name)
    
    def identifier_index(self, name: str):
        return self.__symbol_table.index_of(name)
    
    def is_in_symbol_table(self, name: str):
        if name in self.__symbol_table.get_class_sym_table().class_sym_table.keys():
            return True
        elif name in self.__symbol_table.get_subr_sym_table().keys():
            return True
        return False
    
    def next_token(self):
        if self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()

    def prev_token(self):
        if self.__tokenizer.get_token_number() > 0:
            self.__tokenizer.previous()

    def arg_index(self):
        return self.__symbol_table.get_arg_ind()

    def lcl_index(self):
        return self.__symbol_table.get_lcl_ind()

    def field_index(self):
        return self.__symbol_table.get_field_ind()

    def static_index(self):
        return self.__symbol_table.get_static_ind()

    def correct_var_kind(self, var_kind):
        if var_kind == 'FIELD':
            var_kind = 'this'
        return var_kind
