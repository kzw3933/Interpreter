import sys

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: generate_ast <output directory>")
        sys.stderr.write("\n")
        sys.stderr.flush()
        sys.exit(64)
    output_dir = sys.argv[1]
    define_ast(output_dir, "expr", [
        "Binary: left, operator, right",
        "Grouping: expression",
        "Literal: value",
        "Unary: operator, right"
    ])


def define_ast(output_dir, base_name, types):
    path = output_dir + "/" + base_name + ".py"
    with open(path, "w") as f:
        define_visitor(f, base_name, types)
        f.write("\n")
        for type in types:
            class_name = type.split(":")[0].strip()
            field_list = type.split(":")[1].strip()
            define_type(f, base_name, class_name, field_list)
            f.write("\n")

def define_visitor(file_handler, base_name, types):
    file_handler.write("class Visitor:")
    file_handler.write("\n")
    for type in types:
        type_name = type.split(":")[0].strip()
        file_handler.write(f"    def visit_{type_name.lower()}_{base_name}(self, {base_name}):")
        file_handler.write("\n")
        file_handler.write("        raise NotImplementedError")
        file_handler.write("\n")
        file_handler.write("\n")
    

def define_type(file_handler, base_name, class_name, field_list):
    file_handler.write(f"class {class_name}:")
    file_handler.write("\n")
    file_handler.write(f"    def __init__(self, {field_list}):")
    file_handler.write("\n")
    fields = field_list.split(", ")
    for field in fields:
        file_handler.write(f"        self.{field} = {field}")
        file_handler.write("\n")
    file_handler.write("\n")
    file_handler.write(f"    def accept(self, visitor):")
    file_handler.write("\n")
    file_handler.write(f"        return visitor.visit_{class_name.lower()}_{base_name}(self)")
    file_handler.write("\n")
    

if __name__ == "__main__":
    main()

