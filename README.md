# TwoPassAssembler

## Overview

This is a two-pass assembler written using PYTHON 3. It takes assembly language as input
in a file named  **inputACode.txt** and generates corresponding machine code in a file named
**outputMCode.txt**. Symbol table and Opcode table are generated and displayed in the
terminal. Errors in assembly code, if any, will be reported in the terminal. Until all errors are
resolved, the program will not generate machine code or symbol/opcode table.

## OpCodes Used:

![OpCodes Used](https://github.com/adwitsingh/TwoPassAssembler/blob/master/OpcodeGuide.png)

## Types of Instructions:

Type 0: Instructions containing no argument.

Type 1: Instruction containing one argument.

## Syntax Used and Assumptions:

1. Syntax for the comment is, # for single line comments.

2. There should be no space between label and “:”.

3. For opCode with no operands like CLA, 8 “0”s will be added after opCode.

## Sample Input/Output:

### Sample Input-

```assembly
	CLA
	LAC	A
	SUB	B
	BRN	L1
	DSP	A
	CLA
	BRZ	L2
L1: DSP
	CLA
	BRZ	L2
L2: STP
```

### Sample Output -

```
000000000000
000100001011
010000001100
011000000111
100100001011
000000000000
010100001010
100100001100
000000000000
010100001010
110000000000
```



## Execution Process:

1. Put assembly language code in a file named inputACode.txt in the same directory as
    the python file.

2. Run from terminal using :

  ```bash
  $ python3 main.py
  ```

3. Output machine code is stored in OutputMCode.txt

  

## Errors Reported:

  1) If the starting of the symbol is a number.
  2) If Invalid characters detected in a symbol
  3) If no symbol is found before a ‘:’
  4) If a variable is used as a label
  5) If symbol is redeclared.
  6) If the end statement is missing
  7) If invalid opcode is used
  8) If invalid number of arguments to the opcode are given
  9) If an invalid jump location is given
  10) If an invalid use of variable is made
  11) If a symbol is used but not defined
  12) If opCode used as label
  13) If opCode used as variable

## Code Flow:

### PASS 1

1. Symbol table and opCode table are initialised.
2. Assembly program is processed line by line.
3. Program reads instruction and extracts label, opcode, operands and comments.
4. Program compares number of valid operands.
5. opCodes and labels are stored with their location.

### PASS 2

1. Variables are assigned addresses
2. Data tables constructed in pass one are used to create the final machine code as a
.txt file.
