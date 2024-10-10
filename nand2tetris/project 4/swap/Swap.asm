// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

    // set min = arr[0]
    @R14
    A=M
    D=M
    @min
    M=D
    // set max = arr[0]
    @max
    M=D
    // i = 1
    @i
    M=1
    // set minaddress = R14
    @R14 
    D=M
    @minaddress 
    M=D
    // set maxaddress = R14
    @maxaddress 
    M=D 

(LOOP)
    // if i >= R15 goto STOP
    @R15 
    D=M 
    @i 
    D=D-M
    @SWAP
    D;JLE
    // else
    @R14
    D=M
    @i
    A=D+M
    D=M
    @min
    D=D-M
    @CHANGEMIN
    D;JLT
    @R14
    D=M
    @i
    A=D+M
    D=M
    @max
    D=D-M 
    @CHANGEMAX
    D;JGT
    // i = i + 1
    @i
    M=M+1

(CHANGEMIN)
    @R14
    D=M
    @i
    A=D+M
    D=A
    @minaddress
    M=D
    @R14 
    D=M 
    @i 
    A=D+M
    D=M
    @min
    M=D
    @i 
    M=M+1
    @LOOP
    0;JMP

(CHANGEMAX)
    @R14
    D=M
    @i
    A=D+M
    D=A
    @maxaddress
    M=D
    @R14 
    D=M 
    @i 
    A=D+M
    D=M
    @max
    M=D
    @i 
    M=M+1
    @LOOP
    0;JMP

(SWAP)
    @max
    D=M 
    @minaddress
    A=M 
    M=D 
    @min 
    D=M 
    @maxaddress
    A=M 
    M=D
    @END 
    0;JMP

(END)
    @END
    0;JMP
