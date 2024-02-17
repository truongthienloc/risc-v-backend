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
from diassembler_ import tmp_diassembler

def graphic (pc, instruction, blocking) :
    control(instruction[25:32], instruction[17:20])
    line_color= {
    'pc': pc,
    'instruction': tmp_diassembler(instruction),
    'blocking': blocking,
    'IF' : {},
    'REG': {},
    'EX' : {},
    'MEM': {},
    'WB' : {}
    }
    line_color['IF'] ={
        '1' : 'FFFF66' ,
        '2' : '00FF00' ,
        '10': 'FF0000' ,
        '7' : 'B37F4E' ,#= MUX (1,6)
        '8' : 'FF33FF' ,#= MUX (5,7) 
    }
    line_color['REG']= {
        '3'         :'FF0000',
        '4'         :'FF8000',
        '5'         :'7C00F7',
        '6'         :'FF66B3',
        '9'         :'00FF00',
        '11'        :'FFFF66',
        '12'        :'CC00CC',
        '13'        :'00FFFF',
        'CONTROL'   :'1',
        'WB'        :'1',
        'MEM'       :'1',
        'EX'        :'1',
        'wb'        :wb,
        'jump'      :jump,
        'slt'       :slt,
        'MemtoReg'  :mem_to_reg,
        'jal'       :jal,
        'branch'    :branch,
        'jalr'      :jalr,
        'pcsrc1'    :'1',
        'pcsrc2'    :'1',
    }
    line_color['EX']= {
        '14':'FFFF66',
        '15':'00FF00',
        '16':'FF8000',
        '17':'CC00CC',
        '18':'00FFFF',
        '19':'FF0000',
        '20':'FF9933',#= mux(18,31,32,33,34,45)
        '21':'99FFCC',#= mux (31,17,32,33,34,45)
        '22':'99FFCC',#= mux(20,16)
        '23':'00FFFF',#= mux(15,16)
        '24':'FF0000', 
        '25':'00FF00',
        '26':'FFFF00',
        '27':'FF0000',
        '28':'FF0000',
        'AuiOrLui':aui_or_lui,
        'ALUop':ALU_op   ,
        'ALUSrc':ALU_src ,
        'ALUControl': '1',
        'sign-bit':'1'   ,
        'WB': '1',
        'MEM':'1',
    }
    line_color['MEM'] ={
        '29':'FF0000',
        '30':'FF9933',
        '31':'00FF00',
        '32':'FF0000',
        '33':'00FFFF',
        '34':'FFFF66',
        '35':'',
        '36':'',
        'MemWrite': mem_write,
        'Unsigned': unsigned,
        'MemRead' : mem_read,
        'WB': '1'
    }
    if instruction[25:] == '0000011' : #LOAD
        line_color['MEM']['35'] = 'FF8000'
        line_color['MEM']['36'] = 'FF8000' 
    line_color['WB'] = {
        'RegWrite': reg_write,
        'Wb'  :     wb,
        'Slt' :     slt,
        'Jump':     jump,
        'MemtoReg': mem_to_reg,
        '37':'FFFF66',
        '38':'00FFFF',
        '39':'FF0000',
        '40':'',
        '41':'00FF00',
        '42':'', #= mux(40,41)
        '43':'', #= mux(37,42)
        '44':'', #= mux(39, 43)
        '45':'', #= mux(44, 38)
        '46':''
    }
    if instruction[25:] == '0000011' : #LOAD
        line_color['EX']['40'] = 'FF8000'
    line_color['WB']['42'] = mux(line_color['WB']['41'],line_color['WB']['40'], mem_to_reg)
    line_color['WB']['43'] = mux(line_color['WB']['42'],line_color['WB']['37'], jump)
    line_color['WB']['44'] = mux(line_color['WB']['43'],line_color['WB']['39'], slt)
    line_color['WB']['45'] = mux(line_color['WB']['44'],line_color['WB']['38'], wb)

    return line_color
