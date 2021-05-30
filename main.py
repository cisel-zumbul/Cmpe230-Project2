import re

f = open('file', 'r')
map = {'HALT': "1", 'LOAD': "2", 'STORE': "3", 'ADD': "4", 'SUB': "5", 'INC': "6", 'DEC': "7", 'XOR': "8", 'AND': "9",
       'OR': 'A', 'NOT': 'B', 'SHL': 'C', 'SHR': 'D', 'NOP': 'E', 'PUSH': 'F', 'POP': "10", 'CMP': "11", 'JMP': "12",
       'JZ': "13", 'JE': "13", 'JNZ': "14", 'JNE': "14", 'JC': "15", 'JNC': "16", 'JA': "17", 'JAE': "18", 'JB': "19",
       'JBE': '1A', 'READ': '1B', 'PRINT': '1C'}
registers = {'PC': "0", 'A': "1", 'B': "2", 'C': "3", 'D': "4", 'E': "5", 'S': "6"}
labels = {}

linecount = 0
for line in f:  # labelları mape ekledim
    if line =="\n":
        continue
    islabel = re.search(':', line)
    if islabel:
        pos = line.find(':')
        val = 3 * (linecount)
        labels[line[:pos]] = hex(val)[2:]
    else:
        linecount=linecount+1


f.close()
f = open('file', 'r')

for lines in f:
    
    lines=lines.strip()
    opcode = "-1"
    addrmode = "-1"
    operand = "-1"
    word = lines.split(" ")
    for token in word:
        labelmi = re.search('\:', token)
        if labelmi:  # loop: gibi bi satırsa geçiyoz
            continue
        delete = re.search('\n', token)
        if delete:  # mal olduğu için sonuna newline eklemiş onları sildim
            pos = token.find('\n')
            token = token[:pos]
        if token in map:  # mapteyse load store vs demektir
            opcode = map[token]
            continue
        if token in labels:  # labelsa
            addrmode = "0"
            operand = labels[token]
            continue
        if token in registers:  # registerlardan biriyse
            addrmode = "1"
            operand = registers[token]
            continue
        tirnak = re.search('\'', token)
        if tirnak:  # tırnak içindeyse
            addrmode = "0"
            token = token[1:2]
            asci = format(ord(token), "x")
            operand = asci
            continue
        bracket = re.search('\[', token)
        if bracket:  # parantez içindeyse
            if len(token) is 3:  # [B] gibi
                token = token[1:2]
                val = registers[token]
                addrmode = "2"
                operand = val
                continue
            else:  # [1234] gibi
                closeb = token.find('\]')
                memo = token[1:closeb]
                addrmode = "3"
                operand = memo
                continue
        # hiçbiri değilse normal sayıdır  load 0004
        addrmode = "0"
        operand = token

    if opcode == "1" or opcode=="E":
        addrmode = "0"
        operand = "0"

   # print(opcode, addrmode, operand)

    if opcode == "-1":
        continue

    opcode1 = int(opcode, 16)
    addrmode1 = int(addrmode, 16)
    operand1 = int(operand, 16)

    bopcode = format(opcode1, '06b')
    baddrmode = format(addrmode1, '02b')
    boperand = format(operand1, '016b')
    bin = '0b' + bopcode + baddrmode + boperand
    ibin = int(bin[2:], 2);
    instr = format(ibin, '06x')
    print(instr)
