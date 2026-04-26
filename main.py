import os
import ast
import json
from llm_engine import generate_tests


class SoftwareTestingTool:
    def __init__(self, target_path):
        self.target_path = target_path
        self.excluded_dirs = {'.git', '__pycache__', 'node_modules', 'venv'}

    def get_source_code(self):
        extracted_data = []

        for root, dirs, files in os.walk(self.target_path):
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]

            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    extracted_data.append(self._parse_file(path))

        return extracted_data

    def _parse_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        nodes = []

        for node in ast.iter_child_nodes(tree):

            # Classes + methods
            if isinstance(node, ast.ClassDef):
                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef):
                        nodes.append({
                            "class": node.name,
                            "name": sub.name,
                            "code": ast.get_source_segment(source_code, sub)
                        })

            # Standalone functions
            elif isinstance(node, ast.FunctionDef):
                nodes.append({
                    "class": None,
                    "name": node.name,
                    "code": ast.get_source_segment(source_code, node)
                })

        return {"file": file_path, "content": nodes}


# ===================== SAVE TESTS =====================

def save_tests(function_name, tests):
    base = "Test_Folder"

    # Required structure (rubric compliant)
    structure = {
        "whitebox": ["statement", "condition", "block", "path"],
        "blackbox": ["bva", "ecp", "mutation"]
    }

    for main, subs in structure.items():
        for sub in subs:
            os.makedirs(f"{base}/{main}/{sub}", exist_ok=True)

    # Map test types to folders
    mapping = {
        "statement": "whitebox/statement",
        "condition": "whitebox/condition",
        "block": "whitebox/block",
        "path": "whitebox/path",
        "bva": "blackbox/bva",
        "ecp": "blackbox/ecp",
        "mutation": "blackbox/mutation"
    }

    # Save tests into correct folders
    for test_type, folder in mapping.items():
        file_path = f"{base}/{folder}/{function_name}_tests.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({test_type: tests.get(test_type, [])}, f, indent=4)


# ===================== MAIN EXECUTION =====================

if __name__ == "__main__":
    tool = SoftwareTestingTool("./")

    print("\n--- STARTING CODE ANALYSIS ---")

    results = tool.get_source_code()

    total_functions = 0

    for file in results:
        print(f"\nFile: {file['file']}")

        for item in file["content"]:
            total_functions += 1

            print(f"\nFunction: {item['name']} (Class: {item['class']})")

            # Generate tests using LLM engine (mock or real)
            tests = generate_tests(item["code"], item["name"])

            # Save structured outputs
            save_tests(item["name"], tests)

    print(f"\n✔ Analysis complete. Total functions processed: {total_functions}")
    print("✔ Test cases generated in Test_Folder/")
