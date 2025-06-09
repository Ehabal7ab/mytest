import ast
import sys
import json

class CommandInjectionDetector(ast.NodeVisitor):
    def __init__(self):
        self.vulnerabilities = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'system' and isinstance(node.func.value, ast.Name) and node.func.value.id == 'os':
                self.check_command_injection(node, 'os.system')
        self.generic_visit(node)

    def check_command_injection(self, node, function_name):
        if node.args:
            first_arg = node.args[0]
            if not isinstance(first_arg, (ast.Str, ast.Constant)):
                self.vulnerabilities.append({
                    'type': 'Command Injection',
                    'function': function_name,
                    'line': node.lineno,
                    'col': node.col_offset,
                    'desc': f'Potential injection using {function_name}'
                })

def analyze_file(file_path):
    with open(file_path, 'r') as f:
        code = f.read()
    tree = ast.parse(code)
    detector = CommandInjectionDetector()
    detector.visit(tree)
    return detector.vulnerabilities

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python sast.py <file>")
        sys.exit(1)

    vulns = analyze_file(sys.argv[1])
    if vulns:
        print(json.dumps(vulns, indent=2))
        with open("sast_results.json", "w") as out:
            json.dump(vulns, out, indent=2)
        sys.exit(1)
    else:
        print("No vulnerabilities found.")
        sys.exit(0)
