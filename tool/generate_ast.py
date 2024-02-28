import sys

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: generate_ast <output directory>\n")
        sys.exit(64)
    output_dir = sys.argv[1]
    define_ast(output_dir, "expr", [
        "Binary: left, operator, right",
        "Grouping: expression",
        "Literal: value",
        "Unary: operator, right"
    ])


def define_ast(output_dir, base_name, types):
    path = f"{output_dir}/{base_name}.py"
    with open(path, "w") as f:
        f.write("from abc import ABC, abstractmethod\n\n")
        define_visitor(f, base_name, types)
        f.write("\n")
        for type in types:
            class_name, field_list = map(str.strip, type.split(":"))
            define_type(f, base_name, class_name, field_list)
            f.write("\n")

def define_visitor(file_handler, base_name, types):
    file_handler.write("class Visitor(ABC):\n")
    for type in types:
        type_name = type.split(":")[0].strip()
        file_handler.write("    @abstractmethod\n")
        file_handler.write(f"    def visit_{type_name.lower()}_{base_name}(self, {base_name}):\n")
        file_handler.write("        pass\n\n")
    

def define_type(file_handler, base_name, class_name, field_list):
    file_handler.write(f"class {class_name}:\n")
    file_handler.write(f"    def __init__(self, {field_list}):\n")
    for field in field_list.split(", "):
        file_handler.write(f"        self.{field} = {field}\n")
    file_handler.write(f"\n    def accept(self, visitor):\n")
    file_handler.write(f"        return visitor.visit_{class_name.lower()}_{base_name}(self)\n")
    

if __name__ == "__main__":
    main()

