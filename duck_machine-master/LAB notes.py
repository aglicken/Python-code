OBJECT CODE ---> Memory ---> CPU(control unit ---> ALU) ---> Back to mem
           step 0      step 1                step 2      step 3
            
Create control unit --> ALU and how to acess memory



Fetch: The first step is to read a machine instruction.
Instructions are in memory. Register r15 is treated as the program counter,
so we need to get the value from r15, and use that value to address memory
(Memory.get(address)).
Decode: Once we have the instruction word, we need to decode
its bit fields into the meaningful parts of an instruction.
This is the decode logic you developed in the prior project.
It should produce an Instruction object with several fields.
Execute: This step can be broken down further:


