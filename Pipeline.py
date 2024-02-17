from convert import handle_intruction_memory
from convert import handle_register
from convert import handle_data_memory
from convert import dec 
from convert import Rd
from convert import Rs1
from convert import Rs2
from app import app, request, json

IF = {
    'pc+4'      : 0,
    'pc'        : 0,
    'intruction': ''
}
REG = {
    'wb'        : {
        'reg_write': '' , 
        'wb'       :'' , 
        'slt'      : '', 
        'jump'     : '', 
        'mem_to_reg': ''    
    },
    'mem'       : {
        'mem_write': '', 
        'unsigned' :'', 
        'mem_read' :''
    },
    'ex'        : {
        'AuiOrLui'  :'',
        'ALU_src'   :'', 
        'ALU_op'    :''
    },
    'pc+4'      : 0,
    'pc'        : 0,
    'read_data1': '',
    'read_data2': '',
    'imm_gen'   : '',
    'funct3_7'  : '',
    'write_reg' : '',
    'rs1'       : '',
    'rs2'       : '',
}
EX = {
    'wb'        : {
        'reg_write': '' , 
        'wb'       :'' , 
        'slt'      : '', 
        'jump'     : '', 
        'mem_to_reg': ''    
    },
    'mem'       : {
        'mem_write': '', 
        'unsigned' :'', 
        'mem_read' :''
    },
    'pc+4'      : 0,
    'beq'       : 0,
    'AuiOrLui'  : '',
    'slt'       : '',
    'ALU_result': '',
    'read_data2': '',
    'write_reg' : ''
}
WB = {
    'wb'        : {
        'reg_write': '' , 
        'wb'       :'' , 
        'slt'      : '', 
        'jump'     : '', 
        'mem_to_reg': ''    
    },
    'pc+4'      :0,
    'AuiOrLui'  :'',
    'slt'       :'',
    'data'      :'',
    'alu_result':'',
    'write_reg' : ''
}
# DONE SIGNAL
if_done  = 0
reg_done = 0
ex_done  = 0
mem_done = 0
wb_done  = 0

#INSTRUCTION MEMORY
pc=0
current_pc=0
instruction_memory={}


#REGISTER 
register={
'00000': '00000000000000000000000000000000',
'00001': '00000000000000000000000000000000',
'00010': '00000000000000000000000000000000',
'00011': '00000000000000000000000000000000',
'00100': '00000000000000000000000000000000',
'00101': '00000000000000000000000000000000',
'00110': '00000000000000000000000000000000',
'00111': '00000000000000000000000000000000',
'01000': '00000000000000000000000000000000',
'01001': '00000000000000000000000000000000',
'01010': '00000000000000000000000000000000',
'01011': '00000000000000000000000000000000',
'01100': '00000000000000000000000000000000',
'01101': '00000000000000000000000000000000',
'01110': '00000000000000000000000000000000',
'01111': '00000000000000000000000000000000',
'10000': '00000000000000000000000000000000',
'10001': '00000000000000000000000000000000',
'10010': '00000000000000000000000000000000',
'10011': '00000000000000000000000000000000',
'10100': '00000000000000000000000000000000',
'10101': '00000000000000000000000000000000',
'10110': '00000000000000000000000000000000',
'10111': '00000000000000000000000000000000',
'11000': '00000000000000000000000000000000',
'11001': '00000000000000000000000000000000',
'11010': '00000000000000000000000000000000',
'11011': '00000000000000000000000000000000',
'11100': '00000000000000000000000000000000',
'11101': '00000000000000000000000000000000',
'11110': '00000000000000000000000000000000',
'11111': '00000000000000000000000000000000'
}
read_register_1=''
read_register_2=''
write_register=''
write_data_r=0
read_data_1=0
read_data_2=0
rs1=0
rs2=0

#DATA_MEMORY
Data_memory ={}
write_data_d=''
read_data=''

#CONTROL
jalr = 0
branch ='000'
jal = 0
slt = 0 
mem_read = '000' 
mem_to_reg = 0
ALU_op = '00'
mem_write = '000'
ALU_src = 0
reg_write = 0
aui_or_lui = 0
unsigned = 0
wb = 0

#ALU
operation=''
zero=0
sign_bit=0
ALU_result=0

#BRANCH
pc_src_1=0
pc_src_2=0
jump=0

#ALL TIME DATA
regiter_all_time = []
data_memory_all_time = []
#STALL SIGNALS
blocking = 0
EX_stall = 0
MEM_stall= 0
nop_fwd  = 0
WB_stall = 0

def data_memory (address, mem_read, mem_write, write_data) :
    global read_data, Data_memory

    if mem_read[0] == '1' :
        if address not in Data_memory :
            Data_memory[address] = '00000000000000000000000000000000'
        if mem_read == '100' :
            read_data = Data_memory[address][-8:]
        if mem_read == '101' :
            read_data = Data_memory[address][-16:]
        if mem_read == '110' :
            read_data = Data_memory[address]
        
    if mem_write[0] == '1':
        if address not in Data_memory :
            Data_memory[address] = '00000000000000000000000000000000'
        if mem_write == '100' :
            string = Data_memory[address][8:] + write_data [-8:]
            Data_memory[address] = string
        if mem_write == '101' :
            string = Data_memory[address][16:] +  write_data [-16:] 
            Data_memory[address] = string
        if mem_write == '110' :
            Data_memory[address] = write_data
    

def data_gen (read_data, unsigned) :
    if unsigned == 0 and read_data != '' :
        read_data = read_data.rjust(32, read_data[0])
    if unsigned == 1 and read_data != '' :
        read_data = read_data.rjust(32, '0')
    return read_data

def ALU (operand_1 ,operand_2 ,operation) :
    global zero, sign_bit, ALU_result
    zero= 0
    sign_bit= 0
    #print('alu',operand_1 ,operand_2, operation)
    if operation == 'z' : 
        ALU_result = '0'
        return
    
    if operation[0] == '1' : #unsigned 
        operand_1 =dec ('0'+operand_1)
        operand_2 =dec ('0'+operand_2)
    else : #signed
        operand_1 =dec (operand_1)
        operand_2 =dec (operand_2)
    #print (operand_1, operand_2)

    if operand_1 <0 : sign_operand_1 =1
    else: sign_operand_1 =0

    if operation[1:] == '000': #and
        ALU_result = operand_1 & operand_2
    if operation[1:] == '001': #or
        ALU_result = operand_1 | operand_2
    if operation[1:] == '010':  #Xor
        ALU_result = operand_1 ^ operand_2
    if operation[1:] == '011': #add
        ALU_result = operand_1 + operand_2
    if operation[1:] == '100':  #sub
        ALU_result = operand_1 - operand_2
    
    operand_2 = operand_2 & 31
    if operation[1:] == '101': #Sll
        ALU_result = operand_1 << operand_2
    if operation[1:] == '110' :  #Slr
        ALU_result = operand_1 >> operand_2
    if operation[1:] == '111': #Sra
        if sign_operand_1 :
            ALU_result = dec (bin(operand_1 >> operand_2)[2:].rjust(32,'1'))
        else:
            ALU_result = dec (bin(operand_1 >> operand_2)[2:].rjust(32,'0'))
    if ALU_result == 0 : zero = 1
    if ALU_result < 0  :
        sign_bit=1
        ALU_result = (1<<32) + ALU_result
    ALU_result = bin (ALU_result)

    if ALU_result[0] == '-' : ALU_result= ALU_result[3:].rjust(32,'1')
    if ALU_result[0] == '0' : ALU_result= ALU_result[2:].rjust(32,'0')
    #print (ALU_result)

def mux (input1, input2, sel) :
    if sel ==0 :
        return input1
    if sel ==1 :
        return input2

def control (opcode, funct3) :
    global jalr, branch, jal, slt, mem_read, mem_to_reg, ALU_op, mem_write, ALU_src, reg_write, aui_or_lui, unsigned, wb, jump
    
    if opcode == '0110011'  : #R-type
        jal =0; jalr = 0;   branch = '000';     aui_or_lui = 0;     wb = 0
        mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
        ALU_src = 0;        reg_write = 1;      ALU_op = '10' 
        if funct3 == '010' or funct3 =='011': slt = 1  
        else: slt =0
    
    if opcode == '1100011'  : #BEQ
        jal =0;         jalr = 0;       aui_or_lui = 0;     wb = 0      
        mem_to_reg =0;  unsigned = 0;   mem_read = '000';   mem_write = '000'
        ALU_src = 0;        reg_write = 0;      ALU_op = '01' 
        slt = 0

        if funct3== '000' :
            branch= '1000' #BEQ
        if funct3== '001' :
            branch= '1010'  #BNE
        if funct3== '100' :
            branch= '1100' #BLT
        if funct3== '101' :
            branch= '1110' #BGE
        if funct3== '110' :
            branch= '1101' #BLTU
        if funct3== '111' : 
            branch= '1111' #BGEU
    
    if opcode == '0000011' : #LOAD
        jal =0;     jalr = 0;               branch = '000';         aui_or_lui = 0
        wb = 0;     mem_to_reg =1;          unsigned = funct3[0];   mem_read ='1'+ funct3[1:]
        mem_write = '000';   ALU_src = 1;   reg_write = 1;          ALU_op = '00' ; slt =0
    
    if  opcode == '0100011': #STORE
        jal =0;     jalr = 0;        branch = '000';         aui_or_lui = 0
        wb = 0;     mem_to_reg =0;   unsigned = funct3[0];   mem_read = '000'
        mem_write = '1'+ funct3[1:];      ALU_src = 1;   reg_write = 0;       ALU_op = '00' ; slt=0
    
    if opcode == '0010011' : #I-FORMAT
        jal =0;             jalr = 0;   branch = '000';     aui_or_lui = 0;     wb = 0
        mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
        ALU_src = 1;        reg_write = 1;      ALU_op = '11' 
        if funct3 == '010' or funct3 =='011': slt = 1
        else: slt =0

    if opcode == '1100111' :   #JALR
        jal =0;             jalr = 1;           branch = '000';     aui_or_lui = 0;     wb = 0
        mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
        ALU_src = 1;        reg_write = 1;      ALU_op = '00' ; slt =0
    
    if opcode == '1101111' :   #JAL
        jal =1;             jalr = 0;           branch = '000';     aui_or_lui = 0;     wb = 0
        mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
        ALU_src = 0;        reg_write = 1;      ALU_op = 'z' ;      slt= 0
    
    if opcode == '0110111' : #LUI   
        jal = 0;             jalr = 0;           branch = '000';     aui_or_lui = 1;     wb = 1
        mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
        ALU_src = 0;        reg_write = 1;      ALU_op = 'z' ;      slt= 0
        
    if opcode == '0010111' : #AUIPC
        jal = 0;             jalr = 0;           branch = '000';     aui_or_lui = 0;     wb = 1
        mem_to_reg =0;      unsigned = 0;       mem_read = '000';   mem_write = '000'
        ALU_src = 0;        reg_write = 1;      ALU_op = 'z' ; slt=0

    if jal==1 or jalr ==1: jump=1
    else: jump =0

def imm_gen (instruction) :
        imm=''
        if instruction [-7:] == '0110011' : #R-type
            return '0'
        if instruction [-7:] == '0010011' or instruction [-7:] == '0000011' or instruction[-7:] == '1100111' :  #I-TYPE
            imm= instruction[0:12]
            #if instruction[-15:-12] == '011' : return imm.rjust(32, '0')
        
        if instruction[-7:] =='0100011' :#S-TYPE
            imm= instruction[0:7]+instruction[20:25] 
    
        if instruction[-7:] =='1100011' : #B-TYPE
            imm= instruction[0]+instruction[24]+instruction[1:7]+ instruction[20:24]
    
        if instruction[-7:] =='1101111' :#J-TYPE
            imm= instruction[0] + instruction[12:20] +instruction[11] + instruction[1:11]
        
        if instruction[-7:] == '0110111' or instruction[-7:] == '0010111': #U-TYPE
            imm= instruction[:20]
        
        if instruction[-7:] == '0110111' or instruction[:7] == '0010111': #LUI AUIPC
            return imm.rjust(32, '0')
        else:
            return imm.rjust(32, imm[0])

def alu_control (alu_op, funct3, funct7):
    global operation
    if alu_op == '00' : #   LOAD and STORE and JALR
        operation = '0011'
    if alu_op == '01' : #BRANCH
        if funct3 == '000' or funct3 == '001' or funct3 == '100' or funct3 == '101' :
            operation = '0100'
        if funct3 == '110' or funct3 == '111' :
            operation = '1100'
    
    if alu_op == '10' : #R-TYPE 
        if funct3 == '000' :
            if funct7 =='0' :
                operation = '0011'
            if funct7 == '1':
                operation = '0100'

        if funct3 == '001' : operation= '0101'
        if funct3 == '010' : operation= '0100'
        if funct3 == '011' : operation= '1100'
        if funct3 == '100' : operation= '0010'
        if funct3 == '101' :
            if funct7 == '0' :
                operation = '0110'
            if funct7 == '1' :
                operation = '0111'
        if funct3 == '110' : operation= '0001'
        if funct3 == '111' : operation= '0000'
    
    if alu_op == '11' : #I-TYPE
        if funct3 == '000' : operation= '0011'  #ADDI
        if funct3 == '001' : operation= '0101'  #SLLI
        if funct3 == '010' : operation= '0100'  #SLTI
        if funct3 == '011' : operation= '1100'  #SLTIU
        if funct3 == '100' : operation= '0010'  #XORI
        if funct3 == '101' : #SRLI OR SRAI
            if funct7 == '0' :
                operation= '0110'
            if funct7 == '1' :
                operation= '0111'
        if funct3 == '110' : operation= '0001'  #ORI
        if funct3 == '111' : operation= '0000'  #ANDI
    if alu_op == 'z': operation = 'z'

tw_reg=[]
buffer=[]
buffer1=[]

def branch_control (jal, jalr, Branch, wb, jump, slt, MemtoReg,
                    pc4, AuiOrLui, Slt, ALU_result, data,
                    rs1, rs2, rd1, rd2,w_reg) :
    global pc_src_1, pc_src_2, tw_reg, buffer1, buffer2, buffer
    vrs1= rd1
    vrs2= rd2
    # print('vrs1', vrs1,'vrs2',vrs2)
    if len (buffer) == 3:
        buffer = buffer[1:]
    if len (buffer1) == 3:
        buffer1 = buffer1[1:]

    buffer1.append([jal, jalr, Branch, wb, jump, slt, MemtoReg])
    if len(buffer1) >1:
        buffer.append(mux( mux( mux(mux(ALU_result, data, buffer1[1][6]), pc4, buffer1[1][4]),Slt, buffer1[1][5]), AuiOrLui, buffer1[1][3]))
    else:
        buffer.append(mux( mux( mux(mux(ALU_result, data, MemtoReg), pc4, jump),Slt, slt), AuiOrLui, wb))
    tw_reg.append(w_reg)
    # print('buff1',buffer1)
    # print('buff2',buffer2)
    # print('buffer',buffer)
    # print('twr',tw_reg)
    # print( rs2 == tw_reg[len(tw_reg)-1] or rs2==tw_reg[len(tw_reg)-2])
    # print('rs1',rs1,'rs2', rs2)
    # print (rs2==tw_reg[len(tw_reg)-2])
    # print('signal',jal, jalr, Branch, wb, jump, slt, MemtoReg, 'pc4', pc4)
    # print('data',pc4, AuiOrLui, Slt, ALU_result, data)

    if jal == 1: 
        pc_src_1 = 1
        pc_src_2 = 0
        return
    if jalr == 1 :
        pc_src_1 = 0
        pc_src_2 = 1
        return
    if Branch == '000' :
        pc_src_1= 0
        pc_src_2= 0
        return
    if rs1 == tw_reg[len(tw_reg)-1] or rs2 == tw_reg[len(tw_reg)-1] or rs1==tw_reg[len(tw_reg)-2] or rs2==tw_reg[len(tw_reg)-2]:
        if rs1==tw_reg[len(tw_reg)-2]:
            vrs1= buffer[1]
        if rs2==tw_reg[len(tw_reg)-2]:
            vrs2= buffer[1]
        # print (vrs1, vrs2, rs2, tw_reg[len(tw_reg)-2])
        # print ((ALU_result, data, MemtoReg), pc4, jump,Slt, slt, AuiOrLui, wb)
        # print(buffer)
        if rs1==tw_reg[len(tw_reg)-1]:
            vrs1= buffer[2]
        if rs2==tw_reg[len(tw_reg)-1]:
            vrs2= buffer[2]
    #print (vrs1.rjust(32,'0'), vrs2.rjust(32,'0'))     
    # print('tvrs1', vrs1,'vrs2',vrs2)
    vrs1= dec(vrs1)
    vrs2= dec(vrs2)
    
    
    if Branch[0] == '1' :
        if Branch == '1000' : #beq
            if vrs1==vrs2 :
                pc_src_1 = 1
                pc_src_2 = 0
            else :
                pc_src_1 = 0
                pc_src_2 = 0
        if Branch == '1010' : #bne
            if vrs1!=vrs2 :
                pc_src_1 = 1
                pc_src_2 = 0
            else:
                pc_src_1 = 0
                pc_src_2 = 0
        if Branch == '1100' : #blt
            if vrs1 < vrs2:
                pc_src_1 = 1
                pc_src_2 = 0
            else :
                pc_src_1 = 0
                pc_src_2 = 0 
        if Branch == '1110' : #bge
            if vrs1>=vrs2 :
                pc_src_1 = 1
                pc_src_2 = 0
            else :
                pc_src_1 = 0
                pc_src_2 = 0

        if Branch == '1101' : #BLTU
            if abs (vrs1) < abs (vrs2):
                pc_src_1 = 1
                pc_src_2 = 0
            else :
                pc_src_1 = 0
                pc_src_2 = 0 
        if Branch == '1111' : #BGEU
            if abs (vrs1) >= abs (vrs2):
                pc_src_1 = 1
                pc_src_2 = 0
            else :
                pc_src_1 = 0
                pc_src_2 = 0 
    #print('buffer',buffer)
    #print ('branch',Branch,vrs1, vrs2,'pcs',pc_src_1,pc_src_2)
#print (instruction_memory)
pcs1=pcjalr=0
gra = []
from graphic import graphic
from diassembler_ import tmp_diassembler
def ins_fetch ():
    global pc, if_done, current_pc, gra
    if pc == (len(instruction_memory))*4:
        if_done = 1
        return
    # print (pc,tmp_diassembler(instruction_memory[bin(pc)[2:]]))
    # print ('===>x1',dec(register['00001'])) #'x14',dec(register['01110']), 'x17',dec (register['10001']),'x31',dec (register['11111']))#,'x10',register['01010'])
    # print ('===>x09',dec(register['01001']), 'x27',dec(register['11011']),'x07',dec(register['00111']), 'x21',dec(register['10101']))#,'x10',register['01010'])
    # print('wb',write_data_r)
    gra.append(graphic(pc, instruction_memory [bin(pc)[2:]], blocking))
    if blocking ==0:
        instruction= instruction_memory [bin(pc)[2:]]
        IF ['pc']              = pc
        IF ['pc+4']            = pc+4
        IF ['intruction']      = instruction
        current_pc = pc

def reg ():
    global reg_done, blocking, EX_stall, REG, nop_fwd, current_pc, pc, pcs1, pcjalr, rs1, rs2
    if if_done == 1:
        reg_done = 1
        return
    
    control(IF['intruction'][25:32], IF['intruction'][17:20])
    
    read_register_1    = Rs1 (IF['intruction'])
    read_register_2    = Rs2 (IF['intruction'])
    write_register     = Rd (IF['intruction'])
    blocking = hazard_detection (read_register_1, read_register_2, REG['write_reg'], REG ['mem']['mem_read'])
    read_data_1=''
    read_data_2=''
    if read_register_1 != '-2' :
        read_data_1        =register[read_register_1]
    if read_register_2 != '-3' :
        read_data_2        =register[read_register_2]
    branch_control(jal, jalr, branch, wb, jump, slt, mem_to_reg, EX['pc+4'], EX['AuiOrLui'], EX['slt'], EX['ALU_result'],WB['data'], read_register_1 ,read_register_2, read_data_1, read_data_2, REG['write_reg'])
    pcjalr= IF['pc']+dec(imm_gen(IF['intruction']))
    pcs1= IF['pc']+2*dec(imm_gen(IF['intruction']))
    pc = mux(mux(pc+4, pcs1, pc_src_1),pcjalr,pc_src_2)
    if blocking == 0:
        REG ['wb']         ={'reg_write':reg_write , 'wb':wb , 'slt': slt, 'jump': jump, 'mem_to_reg': mem_to_reg}
        REG ['mem']        ={'mem_write': mem_write, 'unsigned':unsigned, 'mem_read':mem_read}
        REG ['ex']         ={'AuiOrLui': aui_or_lui, 'ALU_src': ALU_src, 'ALU_op':ALU_op}
        REG ['pc+4']       =IF['pc+4']
        REG ['pc']         =IF['pc']
        REG ['read_data1'] =read_data_1
        REG ['read_data2'] =read_data_2
        REG ['imm_gen']    =imm_gen(IF['intruction'])
        REG ['funct3_7']   ={'funct3': IF['intruction'][17:20],'funct7': IF['intruction'][1]}
        REG ['write_reg']  =write_register
        REG ['rs1']        =read_register_1
        REG ['rs2']        =read_register_2
        rs1 = REG ['rs1']
        rs2 = REG ['rs2']
        # print ('REG',REG ['rs1'], REG ['rs2'])
    if blocking == 1:
        pc = current_pc
        EX_stall = 1
        REG = {
        'wb'        : {
            'reg_write': '' , 
            'wb'       : '' , 
            'slt'      : '', 
            'jump'     : '', 
            'mem_to_reg':''    
        },
        'mem'       : {
            'mem_write': '', 
            'unsigned' : '', 
            'mem_read' : ''
        },
        'ex'        : {
            'ALU_src'   :'', 
            'AuiOrLui'  :'',
            'ALU_op'    :''
        },
        'pc+4'      : 0,
        'pc'        : 0,
        'read_data1': '',
        'read_data2': '',
        'imm_gen'   : '',
        'funct3_7'  : '',
        'write_reg' : write_register,
        'rs1'       : '',
        'rs2'       : '',
        }
def ex ():
    global ex_done, MEM_stall, EX_stall

    if reg_done == 1:
        #print('exd')
        ex_done = 1
        return
    if EX_stall == 1:
        EX_stall =0
        #print('stall')
        MEM_stall =1
        return
    #print ('FREG',REG ['rs1'], REG ['rs2'])
 

    fwd1, fwd2, flag_x0 = forwarding()
    alu_control(REG['ex']['ALU_op'], REG['funct3_7']['funct3'], REG['funct3_7']['funct7'])
    #print('ex')
    temp_wdr= write_data_r
    # if flag_x0 == 1:
    #     EX['ALU_result']= REG['read_data1']= EX['slt']= EX['AuiOrLui']= EX['pc+4'] ='0'
    # if flag_x0 == 11:
    #     temp_wdr= 0
    operator_1 = mux_6 (EX['ALU_result'], REG['read_data1'], EX['slt'], EX['AuiOrLui'], EX['pc+4'], temp_wdr , fwd1)
    operator_2 = mux (mux_6 (REG['read_data2'], EX['ALU_result'], EX['slt'], EX['AuiOrLui'], EX['pc+4'], temp_wdr ,fwd2 ), REG['imm_gen'], REG['ex']['ALU_src'])
    # print (REG['read_data1'], EX['slt'], EX['AuiOrLui'], EX['pc+4'], temp_wdr , fwd1)
    # print(operator_1, operator_2,'s')
    # print('rd', Rd (IF['intruction']))
    # print ('rs1',Rs1(IF['intruction']),'rs2', Rs2(IF['intruction']))
    if REG['rs1'] =='00000' or REG['rs2']=='00000':
        if REG['rs1'] =='00000': operator_1 = '0'
        if REG['rs2'] =='00000': operator_2 = '0'
    # print (REG['rs1'], REG['rs2'])
    ALU(str(operator_1), str(operator_2), operation)
    # print('RD',Rd (IF['intruction']))
    # print('op',operator_1, operator_2,ALU_result,operation)
    # print('op1-','0',EX['ALU_result'], '1',REG['read_data1'], '2',EX['slt'], '3',EX['AuiOrLui'], '4',EX['pc+4'], '5',temp_wdr , fwd1)
    # print('op2-',REG['read_data2'], EX['ALU_result'], EX['slt'], EX['AuiOrLui'], EX['pc+4'], temp_wdr ,fwd2 , REG['imm_gen'], REG['ex']['ALU_src'])
    # print(mux (mux_6 (REG['read_data2'], EX['ALU_result'], EX['slt'], EX['AuiOrLui'], EX['pc+4'], temp_wdr ,fwd2 ), REG['imm_gen'], REG['ex']['ALU_src']))
    tmp1=''
    tmp2=''
    if (dec(REG['imm_gen'])<<12)+REG['pc'] > 0:
        tmp1= bin((dec(REG['imm_gen'])<<12)+REG['pc'])[2:].rjust(32, '0')
    else:
        tmp1= bin((dec(REG['imm_gen'])<<12)+REG['pc'])[3:].rjust(32, '0')
    if (dec(REG['imm_gen'])<<12) > 0:
        tmp2= bin((dec(REG['imm_gen'])<<12))[2:].rjust(32, '0')
    else:
        tmp2= bin((dec(REG['imm_gen'])<<12))[3:].rjust(32, '0')
    EX['AuiOrLui'] = mux (tmp1 ,tmp2, REG['ex']['AuiOrLui'])
    EX['pc+4'] = bin (REG['pc+4'])[2:].rjust(32, '0')
    EX['slt']      = mux ('00000000000000000000000000000000','00000000000000000000000000000001', sign_bit)
    EX['read_data2'] = mux_6 (REG['read_data2'], EX['ALU_result'], EX['slt'], EX['AuiOrLui'], EX['pc+4'], write_data_r ,fwd2 )
    EX['write_reg']= REG ['write_reg']
    EX['ALU_result'] = ALU_result
    EX['wb']  = REG['wb']
    EX['mem'] = REG['mem']
    # if Rd (IF['intruction']) =='00000':
    #     EX['AuiOrLui'] = '0'
    #     EX['pc+4'] = '0'
    #     EX['slt']      = '0'
    #     EX['write_reg']= '0'
    #     EX['ALU_result'] = '0'
    #     #print('********0*******')

def mem ():
    global mem_done, WB_stall, MEM_stall
    if ex_done == 1:
        mem_done = 1
        return
    if MEM_stall == 1:
        MEM_stall =0
        WB_stall = 1
        return
    WB['wb']         = EX['wb']
    WB['pc+4']       = EX['pc+4']
    WB['AuiOrLui']   = EX['AuiOrLui']
    data_memory(EX['ALU_result'], EX['mem']['mem_read'], EX['mem']['mem_write'], EX['read_data2'])
    #print(EX['ALU_result'], EX['mem']['mem_read'], EX['mem']['mem_write'], EX['read_data2'])
    WB['data']       = data_gen (read_data, EX['mem']['unsigned']) 
    WB['alu_result'] = EX['ALU_result']
    WB['slt']        = EX['slt']
    WB['write_reg']  = EX['write_reg']
    # print('WbinMem',WB['write_reg'],WB['slt'],WB['alu_result'], WB['data'],WB['AuiOrLui'],WB['pc+4'],WB['wb'])
    # if WB['write_reg'] == '00000':
    #     WB['pc+4']       = '0'
    #     WB['AuiOrLui']   = '0'
    #     WB['data']       = '0'
    #     WB['alu_result'] = '0'
    #     WB['slt']        = '0'
write_data_r = ''
pre_wb_rd =''
def write_back():
    global wb_done, pre_wb_rd, write_data_r, WB_stall
    if mem_done == 1:
        wb_done = 1
        return 
    if WB_stall == 1:
        WB_stall =0
        return
    write_data_r = mux( mux( mux(mux(WB['alu_result'],WB['data'], WB['wb']['mem_to_reg']), WB['pc+4'], WB['wb']['jump']),WB['slt'], WB['wb']['slt']), WB['AuiOrLui'],WB['wb']['wb'])
    # print('wb',WB['alu_result'],WB['data'], WB['wb']['mem_to_reg'], WB['pc+4'], WB['wb']['jump'],WB['slt'], WB['wb']['slt'], WB['AuiOrLui'],WB['wb']['wb'])
    if WB['wb']['reg_write']== 1 :
        register[WB['write_reg']] = write_data_r
        # print ('rd',dec('0'+WB['write_reg']), write_data_r, 'ALU', WB['alu_result'])
        if WB['write_reg'] == '00000' :
            register[WB['write_reg']] = '00000000000000000000000000000000'
    pre_wb_rd = WB['write_reg']
    
def mux_6 (data_0, data_1, data_2, data_3, data_4, data_5, sel):
    if sel == 0:
        return data_0
    if sel == 1:
        return data_1
    if sel == 2:
        return data_2
    if sel == 3:
        return data_3 
    if sel == 4:
        return data_4
    if sel == 5:
        return data_5 

def forwarding ():
    global nop_fwd, rs1, rs2
    fwd2=0; fwd1= 1; flag_x0= 0
    if EX['wb']['wb']==0 and EX['wb']['slt']==0 and EX['wb']['jump']==0 and EX['wb']['mem_to_reg']==0 and EX['ALU_result']!='':
        fwd1 = 0 ; fwd2 =1 #ALU_result
    if EX['wb']['wb']==1 and EX['wb']['slt']==0 and EX['wb']['jump']==0 and EX['wb']['mem_to_reg']==0 and EX['AuiOrLui']!=''  :
        fwd1 = 3 ; fwd2 =3 #AUIorLUI
    if EX['wb']['wb']==0 and EX['wb']['slt']==1 and EX['wb']['jump']==0 and EX['wb']['mem_to_reg']==0 and EX['slt']!=''       :
        fwd1 = 2 ; fwd2 =2 #SLT
    if EX['wb']['wb']==0 and EX['wb']['slt']==0 and EX['wb']['jump']==1 and EX['wb']['mem_to_reg']==0 and EX['pc+4']!=''      :
        fwd1 = 4 ; fwd2 =4 #pc+4
    # rs1= Rs1 (IF['intruction'])
    # rs2= Rs2 (IF['intruction'])
    # print('fd1',fwd1 , fwd2)
    # read_register_1= Rs1 (IF['intruction'])
    # read_register_2= Rs2 (IF['intruction'])
    ex_rd = EX['write_reg']
    wb_rd = pre_wb_rd
    # print('rd', ex_rd, 'rs1', Rs1 (IF['intruction']), 'rs2', Rs2 (IF['intruction']))
    if ex_rd== '00000':
        flag_x0 = 1
    if wb_rd == '00000':
        flag_x0 = 11
    #print (WB['write_reg'], pre_wb_rd, pc)
    if rs1 == ex_rd or rs2==ex_rd :
        if rs1 == ex_rd and rs2 != ex_rd:
            fwd2=0
        if rs1 != ex_rd and rs2 == ex_rd:
            fwd1 =1
    else: fwd2=0; fwd1= 1
    # print('fd2',fwd1 , fwd2)
    if (rs1 == wb_rd or rs2== wb_rd) and wb_rd != ex_rd :
        if rs1 == wb_rd and rs2 != wb_rd:
            fwd1 =5
        if rs1 != wb_rd and rs2 == wb_rd:
            fwd2 =5
    if WB_stall == 1:
        fwd1 = 5 ; fwd2 =5
        if rs1 == wb_rd and rs2 != wb_rd:
            fwd2=0
        if rs1 != wb_rd and rs2 == wb_rd:
            fwd1 =1 
    return fwd1, fwd2, flag_x0

def hazard_detection (rs1, rs2, rd, mem_read) :
    blocking = 0
    if mem_read !='' :
        if mem_read[0] == '1'  and (rs1== rd or rs2==rd) :
            blocking= 1
    return blocking

from assembler import assembler
#from diassembler import tmp_diassembler
@app.route('/pipeline', methods = ['POST'])
def pipeline ():
    global IF, REG, EX, WB
    global if_done, reg_done, ex_done, mem_done, wb_done 
    global pc, current_pc, instruction_memory
    global register, read_register_1, read_register_2, write_register, write_data_r, read_data_1, read_data_2, rs1, rs2
    global Data_memory, write_data_d, read_data
    global jalr, branch, jal, slt, mem_read, mem_to_reg, ALU_op, mem_write, ALU_src, reg_write, aui_or_lui, unsigned, wb
    global operation, zero, sign_bit, ALU_result
    global pc_src_1, pc_src_2, jump
    global blocking, EX_stall, MEM_stall, nop_fwd, WB_stall 
    global tw_reg, buffer, buffer1, pcs1, pcjalr
    IF = {
    'pc+4'      : 0,
    'pc'        : 0,
    'intruction': ''
    }
    REG = {
        'wb'        : {
            'reg_write': '' , 
            'wb'       :'' , 
            'slt'      : '', 
            'jump'     : '', 
            'mem_to_reg': ''    
        },
        'mem'       : {
            'mem_write': '', 
            'unsigned' :'', 
            'mem_read' :''
        },
        'ex'        : {
            'AuiOrLui'  :'',
            'ALU_src'   :'', 
            'ALU_op'    :''
        },
        'pc+4'      : 0,
        'pc'        : 0,
        'read_data1': '',
        'read_data2': '',
        'imm_gen'   : '',
        'funct3_7'  : '',
        'write_reg' : '',
        'rs1'       : '',
        'rs2'       : '',
    }
    EX = {
        'wb'        : {
            'reg_write': '' , 
            'wb'       :'' , 
            'slt'      : '', 
            'jump'     : '', 
            'mem_to_reg': ''    
        },
        'mem'       : {
            'mem_write': '', 
            'unsigned' :'', 
            'mem_read' :''
        },
        'pc+4'      : 0,
        'beq'       : 0,
        'AuiOrLui'  : '',
        'slt'       : '',
        'ALU_result': '',
        'read_data2': '',
        'write_reg' : ''
    }
    WB = {
        'wb'        : {
            'reg_write': '' , 
            'wb'       :'' , 
            'slt'      : '', 
            'jump'     : '', 
            'mem_to_reg': ''    
        },
        'pc+4'      :0,
        'AuiOrLui'  :'',
        'slt'       :'',
        'data'      :'',
        'alu_result':'',
        'write_reg' : ''
    }
    # DONE SIGNAL
    if_done  = 0
    reg_done = 0
    ex_done  = 0
    mem_done = 0
    wb_done  = 0

    #INSTRUCTION MEMORY
    pc=0
    current_pc=0
    instruction_memory={}


    #REGISTER 
    register={
    '00000': '00000000000000000000000000000000',
    '00001': '00000000000000000000000000000000',
    '00010': '00000000000000000000000000000000',
    '00011': '00000000000000000000000000000000',
    '00100': '00000000000000000000000000000000',
    '00101': '00000000000000000000000000000000',
    '00110': '00000000000000000000000000000000',
    '00111': '00000000000000000000000000000000',
    '01000': '00000000000000000000000000000000',
    '01001': '00000000000000000000000000000000',
    '01010': '00000000000000000000000000000000',
    '01011': '00000000000000000000000000000000',
    '01100': '00000000000000000000000000000000',
    '01101': '00000000000000000000000000000000',
    '01110': '00000000000000000000000000000000',
    '01111': '00000000000000000000000000000000',
    '10000': '00000000000000000000000000000000',
    '10001': '00000000000000000000000000000000',
    '10010': '00000000000000000000000000000000',
    '10011': '00000000000000000000000000000000',
    '10100': '00000000000000000000000000000000',
    '10101': '00000000000000000000000000000000',
    '10110': '00000000000000000000000000000000',
    '10111': '00000000000000000000000000000000',
    '11000': '00000000000000000000000000000000',
    '11001': '00000000000000000000000000000000',
    '11010': '00000000000000000000000000000000',
    '11011': '00000000000000000000000000000000',
    '11100': '00000000000000000000000000000000',
    '11101': '00000000000000000000000000000000',
    '11110': '00000000000000000000000000000000',
    '11111': '00000000000000000000000000000000'
    }
    read_register_1=''
    read_register_2=''
    write_register=''
    write_data_r=0
    read_data_1=0
    read_data_2=0
    rs1=0
    rs2=0

    #DATA_MEMORY
    Data_memory ={}
    write_data_d=''
    read_data=''

    #CONTROL
    jalr = 0
    branch ='000'
    jal = 0
    slt = 0 
    mem_read = '000' 
    mem_to_reg = 0
    ALU_op = '00'
    mem_write = '000'
    ALU_src = 0
    reg_write = 0
    aui_or_lui = 0
    unsigned = 0
    wb = 0

    #ALU
    operation=''
    zero=0
    sign_bit=0
    ALU_result=0

    #BRANCH
    pc_src_1=0
    pc_src_2=0
    jump=0

    #ALL TIME DATA
    regiter_all_time = []
    data_memory_all_time = []
    #STALL SIGNALS
    blocking = 0
    EX_stall = 0
    MEM_stall= 0
    nop_fwd  = 0
    WB_stall = 0

    tw_reg=[]
    buffer=[]
    buffer1=[]
    pcs1=0
    pcjalr=0

    s = json.loads(request.data)['code']
    fi = assembler(s)
    pc = 0
    for i in fi :
        instruction_memory[bin(pc)[2:]] = i
        pc+=4

    pc=0
    ins_fetch()

    reg()
    ins_fetch()

    ex()
    reg()
    ins_fetch()

    mem()
    ex()
    reg()
    ins_fetch()
    write_back()
    data_memory_all_time.append (handle_data_memory(Data_memory))
    regiter_all_time.append (handle_register(register))
    mem()
    ex()
    reg()
    ins_fetch()
    while (wb_done==0) :
        write_back()
        # if pc == 72:
        #     d+=1
        # if d== 5:
        #     break
        data_memory_all_time.append (handle_data_memory(Data_memory))
        regiter_all_time.append (handle_register(register))
        mem()
        ex()
        reg()
        ins_fetch()
    instruction_memory= handle_intruction_memory(instruction_memory)
    return gra
    # print (handle_register(register))
    # return {'Register': regiter_all_time,'Data_memory': data_memory_all_time, 'Intruction_memory': instruction_memory}

# ALU()
#pipeline("Code_editor.txt")
# register= handle_register(register)
# print(register)
# Data_memory= handle_data_memory(Data_memory)
# print(Data_memory)
# # print(Data_memory)

# # for i in register:
# #     print(i, register[i])
# for i in Data_memory:
#     print(i)






