import os
import ast
import json

class SoftwareTestingTool:
    def __init__(self, target_path, context_file="Context.json"):
        self.target_path = target_path
        self.context_data = self._load_context(context_file)
        self.excluded_dirs = {'.git', '__pycache__', 'node_modules', 'venv'}

    def _load_context(self, context_file):
        """Loads the detailed specifications from Context.json."""
        if os.path.exists(context_file):
            with open(context_file, 'r') as f:
                return json.load(f)
        return {}

    def get_source_code(self):
        """Recursively finds and parses code from the artifact under study."""
        extracted_data = []
        for root, dirs, files in os.walk(self.target_path):
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            for file in files:
                if file.endswith(".py"): # Supporting Python as the single language
                    path = os.path.join(root, file)
                    extracted_data.append(self._parse_file(path))
        return extracted_data

    def _parse_file(self, file_path):
        """Extracts functions/classes for LLM analysis."""
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        nodes = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                nodes.append({
                    "name": node.name,
                    "type": type(node).__name__,
                    "code": ast.get_source_segment(open(file_path).read(), node)
                })
        return {"file": file_path, "content": nodes}

    def generate_test_prompt(self, code_snippet, requirement):
        """Drafts the prompt for the LLM to generate Whitebox/Blackbox tests."""
        prompt = f"""
        Analyze this code: {code_snippet}
        Based on this requirement: {requirement}
        
        Generate a Test Suite in /Test_Folder including:
        1. Whitebox: Statement and Condition coverage.
        2. Blackbox: BVA and ECP cases.
        """
        return prompt

if __name__ == "__main__":
    # Initialize the tool
    tool = SoftwareTestingTool(target_path="./")
    print("--- Starting Recursive Code Analysis ---")
    results = tool.get_source_code()
    print(f"Successfully mapped {len(results)} files for testing.")
