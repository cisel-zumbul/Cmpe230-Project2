f = open('file2', 'r')
map = {'HALT': "1", 'LOAD': "2", 'STORE': "3", 'ADD': "4", 'SUB': "5", 'INC': "6", 'DEC': "7", 'XOR': "8", 'AND': "9",
       'OR': 'A', 'NOT': 'B', 'SHL': 'C', 'SHR': 'D', 'NOP': 'E', 'PUSH': 'F', 'POP': "10", 'CMP': "11", 'JMP': "12",
       'JZ': "13", 'JE': "13", 'JNZ': "14", 'JNE': "14", 'JC': "15", 'JNC': "16", 'JA': "17", 'JAE': "18", 'JB': "19",
       'JBE': '1A', 'READ': '1B', 'PRINT': '1C'}
registersaddr = {'PC': "0", 'A': "1", 'B': "2", 'C': "3", 'D': "4", 'E': "5", 'S': "6"}

def getkey(val):  #mapin tersini yazmamak için bunu yazdım valueyu yazınca keyi veriyo ama hiç gerekmeyebilir
   for key, value in map.items():
      if val == value:
         return key

register= {'0000': ' ', '0001':' ','0002':' ','0003':' ','0004':' ','0005':' ','0006':' '}
asci={'0041':45,'0042':47,'0043':49,'0044':51,'0045':53}
memory=[None]*65536

memory[45]='00'
memory[46]='41'
memory[47]='00'
memory[48]='42'
memory[49]='00'
memory[50]='43'
memory[51]='00'
memory[52]='44'
memory[53]='00'
memory[54]='45'


def getdatafrommemo(address):
    toint = int(address, 10)
    val1 = memory[toint]
    val2 = memory[toint + 1]
    data = val1 + val2
    return data

SF=False
ZF=False
CF=False


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

    if(opcode=='1'):  #Halt
        print("Halts the cpu")
    elif(opcode=='2'): #Load

        if(addr=='00'):  #LOAD 'A', LOAD 0004
           # print('girdim1')
            register['0001']=operand

        if(addr=='01'):  #LOAD C
           # print('girdim2')
            val=register[operand]
            register['0001']=val

        if(addr=='10'):  #LOAD [B]
            val=register[operand]
            register['0001']=getdatafrommemo(val)

        if(addr=='11'):
            register['0001']=getdatafrommemo(operand)

    print(register.items())




