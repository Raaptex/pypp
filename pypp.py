# Py++ by Raaptex

import os
import sys
import getopt
import shutil

# ------ Instructions

class FunctionExecution:
    
    def __init__(self, instruction) -> None:
        self.instruction = instruction
        
    def get_indent(self):
        return 0
        
    def get_code(self):
        return self.instruction + ";"
    
    @staticmethod
    def is_it(instruction):
        return instruction[-1] == ")" and \
            instruction.split("(")[0] != ""
            
class VariableModification:
    
    def __init__(self, instruction) -> None:
        self.instruction = instruction
       
    def get_indent(self):
        return 0   
        
    def get_code(self):
        if "++" not in self.instruction and "--" not in self.instruction:
            return self.instruction + ";"
        elif "++" in self.instruction:
            return self.instruction.split("++")[0] + "+=1" + ";"
        elif "--" in self.instruction:
            return self.instruction.split("--")[0] + "-=1" + ";"
    
    @staticmethod
    def is_it(instruction):
        return len(instruction.split("=")) == 2 or "++" not in instruction or "--" not in instruction
    
class IfStatement:
    
    def __init__(self, instruction) -> None:
        self.instruction = instruction
    
    def get_indent(self):
        return 1
        
    def get_code(self):
        return "{next_line}if " + self.instruction.split("(")[1].split(")")[0] + ":\n"
    
    @staticmethod
    def is_it(instruction):
        return instruction.split("(")[0].replace(" ", "") == "if"
 
class ElseStatement:
    
    def __init__(self, instruction) -> None:
        self.instruction = instruction
    
    def get_indent(self):
        return 1
        
    def get_code(self):
        return "{next_line}else:\n"
    
    @staticmethod
    def is_it(instruction):
        return instruction.replace(" ", "") == "else"
    
class CloseIndent:
    
    def __init__(self, instruction) -> None:
        self.instruction = instruction
    
    def get_indent(self):
        return self.instruction.count('}') * -1
        
    def get_code(self):
        return "\n"
    
    @staticmethod
    def is_it(instruction):
        return "}" in instruction.replace(" ", "")
    
class DefFunction:
    
    def __init__(self, instruction) -> None:
        self.instruction = instruction
    
    def get_indent(self):
        return 1
        
    def get_code(self):
        return "{next_line}" + self.instruction + ":\n"
    
    @staticmethod
    def is_it(instruction):
        return instruction.split(" ")[0] == "def"
       
class ForLoop:
    
    def __init__(self, instruction) -> None:
        self.instruction = instruction
    
    def get_indent(self):
        return 1
        
    def get_code(self):
        return "{next_line}for " + "(".join(self.instruction.split("(")[1:])[:-2] + ":\n"
    
    @staticmethod
    def is_it(instruction):
        return instruction.split("(")[0].replace(" ", "") == "for"

class WhileLoop:
    
    def __init__(self, instruction) -> None:
        self.instruction = instruction
    
    def get_indent(self):
        return 1
        
    def get_code(self):
        return "{next_line}while " + self.instruction.split("(")[1].split(")")[0] + ":\n"
    
    @staticmethod
    def is_it(instruction):
        return instruction.split("(")[0].replace(" ", "") == "while"

# ------ Code

class ExecutionInfos:
    
    def __init__(self) -> None:
        self.main_file = None
        self.out_file = None
        self.to_bin = False
        self.run_after = False

class ArgvHandle:
    def __init__(self) -> None:
        self.argv = sys.argv[1:]
        self.exec_infos = ExecutionInfos()
        
        try:
            opts, args = getopt.getopt(self.argv, "m:o:br")
        except Exception as e:
            print(e)
            exit()
            
        for opt, arg in opts:
            if opt in ["-m"]:
                self.exec_infos.main_file = arg
            if opt in ["-o"]:
                self.exec_infos.out_file = arg
            if opt in ["-b"]:
                self.exec_infos.to_bin = True
            if opt in ["-r"]:
                self.exec_infos.run_after = True

class Compiler:
    
    def __init__(self, exec_infos : ExecutionInfos) -> None:
        self.exec_infos = exec_infos
        self.code = open(self.exec_infos.main_file, "r").read()
        splited_instructions = self.code.split(";")
        self.splited_instructions = []
        for i in splited_instructions:
            self.splited_instructions += i.split("{")
        self.compiled = ""
        self.indent_level = 0
        
    def _compile(self):
        ins_i = 0
        for instruction in self.splited_instructions:
            instruction = self.__remove_indent(instruction.replace("\n", ""))
            instruction = self.__split_close_indents(instruction)
            for ins in instruction:
                if ins != "":
                    ins_i += 1
                    instruction_type = self.__get_intruction_type(ins)
                    self.compiled += " " * self.indent_level + instruction_type.get_code().replace("{next_line}", "\n" + " " * self.indent_level)
                    self.indent_level += instruction_type.get_indent()
                
        with open(self.exec_infos.out_file + ".py", "w") as out:
            out.write(self.compiled)
            
        if self.exec_infos.to_bin:
            os.system("pyinstaller -F --clean --distpath ./ --log-level CRITICAL " + self.exec_infos.out_file + ".py")
            shutil.rmtree('./build/')
            os.remove(self.exec_infos.out_file + ".spec")
            if self.exec_infos.run_after:
                os.system("cls & " + self.exec_infos.out_file + ".exe")
        else:
            if self.exec_infos.run_after:
                os.system("cls & python " + self.exec_infos.out_file + ".py")
                
    def __get_intruction_type(self, instruction):
        if DefFunction.is_it(instruction):
            return DefFunction(instruction)
        if IfStatement.is_it(instruction):
            return IfStatement(instruction)
        if ElseStatement.is_it(instruction):
            return ElseStatement(instruction)
        if CloseIndent.is_it(instruction):
            return CloseIndent(instruction)
        if ForLoop.is_it(instruction):
            return ForLoop(instruction)
        if WhileLoop.is_it(instruction):
            return WhileLoop(instruction)
        if FunctionExecution.is_it(instruction):
            return FunctionExecution(instruction)
        if VariableModification.is_it(instruction):
            return VariableModification(instruction)
            
    def __remove_indent(self, instruction):
        removed = ""
        text = False
        for l in instruction:
            if l != " ":
                removed += l
                text = True
            elif text:
                removed += l
        return removed
    
    def __split_close_indents(self, instruction):
        if not "}" in instruction:
            return [instruction]
        else:
            ends, ins, text = "", "", False
            i = instruction.split("}")
            for _ in range(len(i)):
                if i[_] == "" and not text: ends+="}"
                elif i[_] != "": text=True; ins+=i[_]
            return ends, ins
                
                    
            
if __name__ == "__main__":
    Compiler(
        ArgvHandle().exec_infos
    )._compile()