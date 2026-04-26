import os
import ast
import json
from llm_engine import generate_tests


class SoftwareTestingTool:
    def __init__(self, target_path, context_file="context.json"):
        self.target_path = target_path
        self.context_data = self._load_context(context_file)
        self.excluded_dirs = {'.git', '__pycache__', 'node_modules', 'venv'}

    def _load_context(self, context_file):
        """Loads specification/context data if available."""
        if os.path.exists(context_file):
            with open(context_file, 'r', encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_source_code(self):
        """Recursively scans project and extracts Python code."""
        extracted_data = []

        for root, dirs, files in os.walk(self.target_path):
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]

            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    extracted_data.append(self._parse_file(path))

        return extracted_data

    def _parse_file(self, file_path):
        """Extract classes and functions using AST."""

        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        nodes = []

        for node in ast.iter_child_nodes(tree):

            # CLASS HANDLING
            if isinstance(node, ast.ClassDef):
                class_name = node.name

                for sub_node in node.body:
                    if isinstance(sub_node, ast.FunctionDef):
                        nodes.append({
                            "class": class_name,
                            "name": sub_node.name,
                            "type": "Method",
                            "code": ast.get_source_segment(source_code, sub_node)
                        })

            # FUNCTION HANDLING
            elif isinstance(node, ast.FunctionDef):
                nodes.append({
                    "class": None,
                    "name": node.name,
                    "type": "Function",
                    "code": ast.get_source_segment(source_code, node)
                })

        return {"file": file_path, "content": nodes}

    def export_results(self, data, output_file="analysis_output.json"):
        """Save extracted structure to JSON."""
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"\n[✔] Analysis saved to {output_file}")


# ================= MAIN EXECUTION =================

if __name__ == "__main__":
    tool = SoftwareTestingTool(target_path="./")

    print("\n--- Starting Recursive Code Analysis ---")
    results = tool.get_source_code()

    total_nodes = 0

    # Create test folder
    os.makedirs("Test_Folder", exist_ok=True)

    for file in results:
        print(f"\nFile: {file['file']}")

        for item in file["content"]:
            total_nodes += 1

            print(f"\nFunction: {item['name']} (Class: {item['class']})")

            # CALL LLM ENGINE
            tests = generate_tests(item["code"], item["name"])

            print("\n--- GENERATED TESTS ---")
            print("WHITEBOX:", tests["whitebox"])
            print("BLACKBOX:", tests["blackbox"])
            print("BVA:", tests["bva"])
            print("ECP:", tests["ecp"])

            # SAVE TESTS TO FILE
            safe_name = item["name"]
            file_path = f"Test_Folder/{safe_name}_tests.json"

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(tests, f, indent=4)

    print(f"\nTotal Extracted Nodes: {total_nodes}")

    # Save full analysis
    tool.export_results(results)
