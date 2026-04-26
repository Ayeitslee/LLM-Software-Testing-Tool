import os
import ast
import json


class SoftwareTestingTool:
    def __init__(self, target_path, context_file="context.json"):
        self.target_path = target_path
        self.context_data = self._load_context(context_file)
        self.excluded_dirs = {'.git', '__pycache__', 'node_modules', 'venv'}

    def _load_context(self, context_file):
        """Loads the detailed specifications from context.json."""
        if os.path.exists(context_file):
            with open(context_file, 'r', encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_source_code(self):
        """Recursively finds and parses code from the artifact under study."""
        extracted_data = []

        for root, dirs, files in os.walk(self.target_path):
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]

            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    extracted_data.append(self._parse_file(path))

        return extracted_data

    def _parse_file(self, file_path):
        """Extracts functions/classes for LLM analysis."""

        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
            tree = ast.parse(source_code)

        nodes = []

        # Extract classes and methods
        for node in ast.walk(tree):

            # Handle classes
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

            # Handle standalone functions (outside class)
            elif isinstance(node, ast.FunctionDef):
                # Avoid duplicate methods inside classes
                if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                    nodes.append({
                        "class": None,
                        "name": node.name,
                        "type": "Function",
                        "code": ast.get_source_segment(source_code, node)
                    })

        return {"file": file_path, "content": nodes}

    def generate_test_prompt(self, code_snippet, requirement):
        """Creates LLM prompt for test generation."""

        prompt = f"""
You are a software testing expert.

Analyze the following code:
{code_snippet}

Based on this requirement:
{requirement}

Generate a complete test suite including:

1. Whitebox Testing:
   - Statement Coverage
   - Condition Coverage

2. Blackbox Testing:
   - Equivalence Class Partitioning (ECP)
   - Boundary Value Analysis (BVA)

Return structured test cases with inputs and expected outputs.
"""
        return prompt


if __name__ == "__main__":
    tool = SoftwareTestingTool(target_path="./")

    print("\n--- Starting Recursive Code Analysis ---")
    results = tool.get_source_code()

    total_nodes = 0

    for file in results:
        print(f"\nFile: {file['file']}")

        for item in file["content"]:
            total_nodes += 1
            print(f"  - {item['type']}: {item['name']} (Class: {item['class']})")

    print(f"\nTotal Extracted Nodes: {total_nodes}")
