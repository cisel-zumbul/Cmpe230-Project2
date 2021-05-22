f = open('file2', 'r')
map = {'HALT': "1", 'LOAD': "2", 'STORE': "3", 'ADD': "4", 'SUB': "5", 'INC': "6", 'DEC': "7", 'XOR': "8", 'AND': "9",
       'OR': 'A', 'NOT': 'B', 'SHL': 'C', 'SHR': 'D', 'NOP': 'E', 'PUSH': 'F', 'POP': "10", 'CMP': "11", 'JMP': "12",
       'JZ': "13", 'JE': "13", 'JNZ': "14", 'JNE': "14", 'JC': "15", 'JNC': "16", 'JA': "17", 'JAE': "18", 'JB': "19",
       'JBE': '1A', 'READ': '1B', 'PRINT': '1C'}
registers = {'PC': "0", 'A': "1", 'B': "2", 'C': "3", 'D': "4", 'E': "5", 'S': "6"}

def getkey(val):  #mapin tersini yazmamak için bunu yazdım valueyu yazınca keyi veriyo ama hiç gerekmeyebilir
   for key, value in map.items():
      if val == value:
         return key

for word in f:
    pos = word.find('\n') #sondaki boşlukları siliyoz
    word = word[:pos]
    firsttwo = word[:2]  # opcode için
    operand = word[-4:]
    tobinary="{0:06b}".format(int(firsttwo, 16)) #binarye cevirdim
    o = tobinary[:-2]     #bastan son iki digite kadar
    o2= int(o,2)
    o3=hex(o2)
    opcode=o3[2:]
    addr= tobinary[-2:]        #son iki digit
    print(opcode,addr,operand)
