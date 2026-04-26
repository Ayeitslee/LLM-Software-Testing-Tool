import os
import json
from Artifact_Study import SimpleCalculator


class TestRunner:
    def __init__(self, test_folder="Test_Folder"):
        self.test_folder = test_folder
        self.calc = SimpleCalculator()

    def load_test_files(self):
        """Recursively load all JSON test files from Test_Folder"""
        test_files = []

        for root, _, files in os.walk(self.test_folder):
            for file in files:
                if file.endswith(".json"):
                    path = os.path.join(root, file)

                    with open(path, "r", encoding="utf-8") as f:
                        try:
                            data = json.load(f)
                            test_files.append((file, data))
                        except json.JSONDecodeError:
                            print(f"[!] Skipping invalid JSON: {file}")

        return test_files

    def extract_function_name(self, filename):
        """Infer function name from file"""
        return filename.replace("_tests.json", "").replace(".json", "")

    def execute_function(self, func_name, inputs):
        """Call function dynamically from SimpleCalculator"""
        func = getattr(self.calc, func_name, None)

        if not func:
            return None, f"Function {func_name} not found"

        try:
            result = func(*inputs)
            return result, None
        except Exception as e:
            return str(e), None

    def parse_test_case(self, test_case):
        """
        Converts test case string like:
        add(2,3)=5
        into:
        inputs = (2,3)
        expected = 5
        """

        if "=" not in test_case:
            return None, None

        left, expected = test_case.split("=")
        expected = expected.strip()

        try:
            args = left[left.find("(") + 1:left.find(")")]
            inputs = tuple(eval(arg.strip()) for arg in args.split(",") if arg.strip() != "")
            return inputs, expected
        except Exception:
            return None, None

    def run_tests(self):
        print("\n--- TEST RUNNER STARTED ---\n")

        test_files = self.load_test_files()

        total = 0
        passed = 0
        failed = 0

        for filename, data in test_files:

            func_name = self.extract_function_name(filename)

            print(f"\n📄 File: {filename} → Function: {func_name}")

            for category, tests in data.items():

                print(f"\n  [{category.upper()}]")

                for test in tests:
                    total += 1

                    # Only process string-style tests
                    if isinstance(test, str) and "=" in test:
                        inputs, expected = self.parse_test_case(test)

                        if inputs is None:
                            print(f"   ⚠ Skipped invalid test: {test}")
                            continue

                        result, error = self.execute_function(func_name, inputs)

                        if error:
                            print(f" ERROR: {error}")
                            failed += 1
                            continue

                        if str(result) == expected:
                            print(f"   ✔ PASS: {test}")
                            passed += 1
                        else:
                            print(f" FAIL: {test} | Got: {result}")
                            failed += 1

                    else:
                        print(f"   ⚠ Unsupported test format: {test}")

        print("\n--- SUMMARY ---")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {round((passed/total)*100, 2) if total else 0}%\n")


if __name__ == "__main__":
    runner = TestRunner()
    runner.run_tests()
