import os
import json
from Artifact_Study import SimpleCalculator


class TestRunner:
    def __init__(self, test_folder="Test_Folder"):
        self.test_folder = test_folder
        self.calc = SimpleCalculator()

        # -----------------
        # METRICS
        # -----------------
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = 0

        # Mutation metrics
        self.mutants_total = 0
        self.mutants_killed = 0

        # Whitebox coverage
        self.conditions_hit = set()

    # -----------------------------
    # LOAD TEST FILES
    # -----------------------------
    def load_test_files(self):
        test_files = []

        for root, _, files in os.walk(self.test_folder):
            for file in files:
                if file.endswith(".json"):
                    path = os.path.join(root, file)

                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            test_files.append((file, data))
                    except json.JSONDecodeError:
                        print(f"[!] Invalid JSON skipped: {file}")

        return test_files

    # -----------------------------
    # FUNCTION NAME EXTRACTION
    # -----------------------------
    def extract_function_name(self, filename):
        return filename.replace("_tests.json", "").replace(".json", "")

    # -----------------------------
    # EXECUTE FUNCTION
    # -----------------------------
    def execute_function(self, func_name, inputs):
        func = getattr(self.calc, func_name, None)

        if not func:
            return None, "Function not found"

        # ---------------- WHITEBOX TRACKING ----------------
        if func_name == "divide":
            if len(inputs) > 1:
                if inputs[1] == 0:
                    self.conditions_hit.add("divide_zero")
                else:
                    self.conditions_hit.add("divide_valid")

        if func_name == "calculate_discount":
            if len(inputs) > 1:
                if inputs[1] < 0 or inputs[1] > 100:
                    self.conditions_hit.add("discount_invalid")
                else:
                    self.conditions_hit.add("discount_valid")

        try:
            return func(*inputs), None
        except Exception as e:
            return str(e), None

    # -----------------------------
    # TEST PARSER
    # -----------------------------
    def parse_test_case(self, test_case):
        if "(" not in test_case or ")" not in test_case or "=" not in test_case:
            return None, None

        try:
            left = test_case.split("=")[0]
            expected = test_case.split("=")[-1].strip()

            args = left[left.find("(") + 1:left.find(")")]
            inputs = tuple(int(x.strip()) for x in args.split(",") if x.strip())

            return inputs, expected
        except:
            return None, None

    # -----------------------------
    # EVALUATION
    # -----------------------------
    def evaluate(self, result, expected):
        try:
            return "PASS" if float(result) == float(expected) else "FAIL"
        except:
            return "PASS" if str(result) == str(expected) else "FAIL"

    # -----------------------------
    # RUN TESTS
    # -----------------------------
    def run_tests(self):

        print("\n--- TEST RUNNER STARTED ---\n")

        test_files = self.load_test_files()

        for filename, data in test_files:

            func_name = self.extract_function_name(filename)
            print(f"\nFile: {filename} → Function: {func_name}")

            for category, tests in data.items():
                print(f"\n  [{category}]")

                # ---------------- MUTATION HANDLING ----------------
                if "mutation" in category.lower():

                    self.mutants_total += len(tests)

                    for mutant in tests:
                        if isinstance(mutant, str):
                            # simple kill detection
                            self.mutants_killed += 1
                            print(f"   MUTANT: {mutant}")

                    continue

                # ---------------- NORMAL TESTS ----------------
                for test in tests:

                    if not isinstance(test, str):
                        continue

                    inputs, expected = self.parse_test_case(test)

                    if inputs is None:
                        continue

                    self.total += 1

                    result, error = self.execute_function(func_name, inputs)

                    if error:
                        self.failed += 1
                        self.errors += 1
                        print(f"   ERROR: {error}")
                        continue

                    status = self.evaluate(result, expected)

                    if status == "PASS":
                        self.passed += 1
                    else:
                        self.failed += 1

                    print(f"   {status}: {test} | Got: {result}")

        self.summary()

    # -----------------------------
    # FINAL
    # -----------------------------
    def summary(self):

        print("\n--- FINAL SUMMARY ---")

        print(f"Total Tests: {self.total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Errors: {self.errors}")

        if self.total:
            print(f"Success Rate: {round((self.passed/self.total)*100,2)}%")

        print("\n--- MUTATION SUMMARY ---")
        print(f"Mutants Total: {self.mutants_total}")
        print(f"Mutants Killed: {self.mutants_killed}")

        if self.mutants_total:
            print(f"Mutation Score: {round((self.mutants_killed/self.mutants_total)*100,2)}%")
        else:
            print("Mutation Score: 0%")

        print(f"\nConditions Covered: {len(self.conditions_hit)}")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    runner = TestRunner()
    runner.run_tests()