"""      # Duck Machine
Cis 211 project 8
Author: Anne Glickenhaus
Duck Machine model DM2018S CPU.
A central processing unit (CPU) which contains registers, an
interface to memory, and sequential logic for executing assembly code
that may have loops and conditional branches. Uses bit field manipulation
and ALU written in the previous project.
"""

from instr_format import Instruction, OpCode, CondFlag, decode
from register import Register, ZeroRegister
from alu import ALU
from mvc import MVCEvent, MVCListenable
from memory import MemoryMappedIO

import logging


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class CPUStep(MVCEvent):
    """CPU is beginning step with PC at a given address"""

    def __init__(self, subject: "CPU", pc_addr: int,
                 instr_word: int, instr: Instruction) -> None:
        self.subject = subject
        self.pc_addr = pc_addr
        self.instr_word = instr_word
        self.instr = instr


class CPU(MVCListenable):
    ''' CPU class subclassing MVCListenable. Contains 16 registers, the first
    one being a Zero register and the last register (number 15) is the
    program counter. Has CondFlag with current condition. Halted set
    initially to False. Does not contain the memory but does have a connection
    to memory object(MemoryMappedIO).
    '''
    def __init__(self, memory: MemoryMappedIO):
        super().__init__()
        self.memory = memory
        self.registers = [ZeroRegister(), Register(), Register(), Register(), Register(),
                          Register(), Register(), Register(), Register(), Register(),
                          Register(), Register(), Register(), Register(),
                          Register(), Register()] # List of register
        self.c_flag = CondFlag.ALWAYS # conditional flags type CondFlag
        self.halted = False
        self.pro_counter = self.registers[15] #reg 15
        self.alu = ALU()

    def step(self):
        ''' Fetch - Retrieve instruction from register 15. Decode - using decode function,
        decode instruction from register 15. Notify all of the memory address in reg 15,
        the retrieved instruction and the decoded instruction. Execute - Compare
        coditional flags by anding together current flag and previous flag, if they
        return a non 0 CondFlag execute. Otherwise increase the program counter by 1
        '''
        new_instruction = self.memory.get(self.pro_counter.get())  # Fetch
        decoded_instruction = decode(new_instruction)     # Decode  Instruction object

        self.notify_all(CPUStep(self, self.pro_counter.get(), new_instruction, decoded_instruction))

        predicate = self.c_flag & decoded_instruction.cond

        if predicate:               #execute instruction
            reg1_i = decoded_instruction.reg_src1
            reg2_i = decoded_instruction.reg_src2

            regtarg = decoded_instruction.reg_target

            value1 = self.registers[reg1_i].get()
            value2 = self.registers[reg2_i].get()
            value2 = decoded_instruction.offset + value2 #offset

            self.pro_counter.put(self.pro_counter.get() + 1) #program count + 1

            result_tup = self.alu.exec(decoded_instruction.op, value1, value2)
            result = result_tup[0]
            self.c_flag = result_tup[1]

            if decoded_instruction.op == OpCode.HALT:
                self.halted = True
            elif decoded_instruction.op == OpCode.LOAD:
                self.registers[regtarg].put(self.memory.get(result))

            elif decoded_instruction.op == OpCode.STORE:
                self.memory.put(result, self.registers[regtarg].get())

            else:
                self.registers[regtarg].put(result)

        else:
            self.pro_counter.put(self.pro_counter.get() + 1)


    def run(self, from_addr=0, single_step=False) -> None:
        ''' A loop that calls the step method. Always starts program
        execution at address 0 and stores it in register 15 before starting
        execution. CPU is set to run until it executes the HALT instruction.
        '''
        self.pro_counter.put(from_addr)
        step_counter = 0
        while not self.halted:
            if single_step:
                input("Step {}; press enter".format(step_count))
            self.step()
            step_counter += 1