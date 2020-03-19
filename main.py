ALL_opCodes = {"CLA":(0,0), "LAC":(1,1), "SAC":(2,1), "ADD":(3,1), "SUB":(4,1), "BRZ":(5,1), "BRN":(6,1), "BRP":(7,1), "INP":(8,1), "DSP":(9,1), "MUL":(10,1), "DIV":(11,1), "STP":(12,0)}

symbolTable = {}
opCodeTable = []
errorTable = []

with open('inputACode.txt','r') as aFile:
  assemblyFile = aFile.readlines()

def printSymbolTable():
  print("********* SYMBOL TABLE *********")
  print("\tSymbol\t Location")
  for symbol,location in symbolTable.items():
    print("  \t",symbol," \t",format(location, "08b"))
  print("")

def printOpCodeTable():
  print("********* OPCODE TABLE *********")
  print("\t Location\tOpCode")
  for o in opCodeTable:
    print("\t",format(o[0], "08b"),"\t",format(o[1], "04b"))
  print("")


def check_valid_variable(symbol,lineNumber):
    try:
        k = int(symbol[0])
        errorTable.append([lineNumber,"ERROR: Symbol's starting cannot be a number in " + symbol])
        return False
    except:
        pass
    if (symbol in ALL_opCodes):
        errorTable.append([lineNumber,"ERROR: opcode used as variable"])
        return False
    validchars = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    flag = 0
    for character in symbol:
        if character not in validchars:
            flag = 1
            errorTable.append([lineNumber,"ERROR: Invalid character " + character + " in symbol " + symbol])
    if flag == 1:
        return False
    return True

def isComment(line):
    if ('#' in line):
        return True
    else:
        return False
        
def isSymbol(line):
    if(':' in line):
        return True
    return False

def addSymbol(line, lc, lineNumber):
    symbol = line.split(':')[0]
    if (len(symbol) == 0):
        errorTable.append([lineNumber,"ERROR: No symbol found"])
        return
    if (symbol in ALL_opCodes):
        errorTable.append([lineNumber,"ERROR: Opcode used as label"])
        return
    if(symbol in symbolTable):
      if type(symbolTable[symbol]) != type(5):
        if(symbolTable[symbol][0] == -2):
          errorTable.append([lineNumber,"ERROR: Variable " + symbol + " used as Label"])
          return
      else:
        errorTable.append([lineNumber,"ERROR: Symbol " + symbol +"   already declared"])
        return
    if(check_valid_variable(symbol, lineNumber)==False):
        return
    symbolTable[symbol] = lc

def passONE(locationCounter):
  lineNumber = 0
  while lineNumber != len(assemblyFile):
    line = assemblyFile[lineNumber]
    if(isComment(line)):
        line = line.split('#')[0]
        line = line.strip()
        if(len(line) == 0):
            lineNumber += 1
            continue
    if(isSymbol(line)):
      addSymbol(line, locationCounter, lineNumber)
      line = line.split(':')[1]

    line = line.split()

    opCode = line[0]
    if (lineNumber == len(assemblyFile) - 1):
        if(opCode != 'STP'):
            errorTable.append([lineNumber,"ERROR: End statement is missing expected STP at the end of the statement"])
    if opCode in ALL_opCodes.keys():
      opCodeTable.append([locationCounter, ALL_opCodes[opCode][0]])
    else:
        errorTable.append([lineNumber,"ERROR: " + opCode + " opcode not recognized."])
    line = line[1:]
    
    if (opCode in ALL_opCodes):
        if ALL_opCodes[opCode][1] != len(line):
            errorTable.append([lineNumber,"ERROR: " + opCode + " expects " + str(ALL_opCodes[opCode][1]) + " number of arguments " + "but " + str(len(line)) + " given."])

    for var in line:
      if var not in symbolTable:
        if(check_valid_variable(var,lineNumber)==False):
            continue
        if ('BR' in opCode):
            symbolTable[var] = (-1,lineNumber)
        else:
            symbolTable[var] = (-2,lineNumber)
      else:
        if ('BR' in opCode and symbolTable[var][0] == -2):
            errorTable.append([lineNumber,"ERROR: Invalid jump location " + var + " Since it's already used as a variable."])
        if('BR' not in opCode and symbolTable[var][0] == -1):
            errorTable.append([lineNumber,"ERROR: Invalid use of " + var + ", it has already been used as a jump location."])

    lineNumber += 1
    locationCounter += 1
  return locationCounter


def handleVariables(lc):
  for symbol in symbolTable:
    if type(symbolTable[symbol]) == type((1,1)):
      if symbolTable[symbol][0] == -2:
        symbolTable[symbol] = lc
        lc += 1
      elif symbolTable[symbol][0] == -1:
        errorTable.append([symbolTable[symbol][1],"ERROR: Label " + symbol  + " used but not defined."])
  return lc

def passTWO(outFile):
  lineNumber = 0
  while lineNumber != len(assemblyFile):
    line = assemblyFile[lineNumber]
    if(isComment(line)):
        line = line.split('#')[0]
        line = line.strip()
        if(len(line) == 0):
            lineNumber += 1
            continue
    if(isSymbol(line)):
      line = line.split(':')[1]
    line = line.split()
    opCode = line[0]
    if opCode in ALL_opCodes.keys():
      outFile.write(format(ALL_opCodes[line[0]][0], "04b"))
    line = line[1:]
    if(len(line) == 0):
      outFile.write(format(0,"08b"))
    else:
      for var in line:
        outFile.write(format(symbolTable[var],"08b"))
    
    outFile.write("\n")
    lineNumber += 1


locationCounter = passONE(0)
handleVariables(locationCounter)
if(len(errorTable) == 0):
  with open("outputMCode.txt","w+") as outFile:
    passTWO(outFile)
  printSymbolTable()
  printOpCodeTable()
else:
    for i in errorTable:
        print (i[1],"at line number " + str(i[0]+1))
