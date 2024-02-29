import sys
from typing import List, Optional

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: generate_ast <output directory>\n")
        sys.exit(64)
    output_dir = sys.argv[1]
    define_ast(output_dir, "Expr", [
        "Assign: Token name, Expr value",
        "Binary: Expr left, Token operator, Expr right",
        "Call: Expr callee, Token paren, List[Expr] arguments",
        "Grouping: Expr expression",
        "Literal: object value",
        "Logical: Expr left, Token operator, Expr right",
        "Unary: Token operator, Expr right",
        "Variable: Token name"
    ])
    define_ast(output_dir, "Stmt", [
        "Block: List[Stmt] statements",
        "Expression: Expr expression",
        "Print: Expr expression",
        "If: Expr condition, Stmt then_branch, Stmt else_branch",
        "While: Expr condition, Stmt body",
        "Function: Token name, List[Token] params, List[Stmt] body",
        "Var: Token name, Expr initializer",
        "Return: Token keyword, Expr value",
    ], "Expr")

def define_ast(output_dir: str, base_name: str, types: List[str], dependency: Optional[str]=None):
    path = f"{output_dir}/{base_name.lower()}.py"
    with open(path, "w") as f:
        f.write("from abc import ABC, abstractmethod\n")
        f.write("from typing import List\n")
        f.write("from lox.token import Token\n")
        if dependency is not None:
            f.write(f"from {output_dir.split('/')[-1]}.{dependency.lower()} import {dependency}\n")
        f.write("\n")
        define_base_class(f, base_name)
        f.write("\n")
        for type in types:
            class_name, field_list = map(str.strip, type.split(":"))
            define_type(f, base_name, class_name, field_list)
            f.write("\n")
        f.write("\n")
        define_visitor(f, base_name, types)
        

def define_base_class(fp, base_name: str):
    fp.write(f"class {base_name}(ABC):\n")
    fp.write("    @abstractmethod\n")
    fp.write(f"    def accept(self, visitor):\n")
    fp.write("        pass\n\n")

def define_visitor(fp, base_name: str, types: List[str]):
    fp.write("class Visitor(ABC):\n")
    for type in types:
        type_name = type.split(":")[0].strip()
        fp.write("    @abstractmethod\n")
        fp.write(f"    def visit_{type_name.lower()}_{base_name.lower()}(self, {base_name.lower()}: {type_name}):\n")
        fp.write("        pass\n\n")
    

def define_type(fp, base_name: str, class_name: str, field_list: str):
    fp.write(f"class {class_name}({base_name}):\n")
    params = ", ".join([f"{field.split(' ')[1]}: {field.split(' ')[0]}" for field in field_list.split(", ")])
    fp.write(f"    def __init__(self, {params}):\n")
    for field in field_list.split(", "):
        type, name = field.split(" ")
        fp.write(f"        self.{name}: {type} = {name}\n")
    fp.write(f"\n    def accept(self, visitor):\n")
    fp.write(f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n")
    

if __name__ == "__main__":
    main()

