import os
import json
from Artifact_Study import SimpleCalculator


class TestRunner:
    def __init__(self, test_folder="Test_Folder"):
        self.test_folder = test_folder
        self.calc = SimpleCalculator()

        # metrics
        self.mutants_total = 0
        self.mutants_killed = 0
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
    # EXECUTE FUNCTION (FIXED ORDER)
    # -----------------------------
    def execute_function(self, func_name, inputs):
        func = getattr(self.calc, func_name, None)

        if not func:
            return None, f"Function {func_name} not found"

        # WHITEBOX CONDITION TRACKING (SAFE)
        if func_name == "divide":
            if len(inputs) > 1:
                if inputs[1] == 0:
                    self.conditions_hit.add("divide_by_zero")
                else:
                    self.conditions_hit.add("valid_division")

        if func_name == "calculate_discount":
            if inputs[1] < 0 or inputs[1] > 100:
                self.conditions_hit.add("invalid_discount")
            else:
                self.conditions_hit.add("valid_discount")

        try:
            return func(*inputs), None
        except Exception as e:
            return str(e), None

    # -----------------------------
    # SAFE TEST PARSER
    # -----------------------------
    def parse_test_case(self, test_case):

        if "(" not in test_case or ")" not in test_case:
            return None, None

        if "=" not in test_case:
            return None, None

        try:
            left = test_case.split("=")[0]
            expected = test_case.split("=")[-1].strip()

            args = left[left.find("(") + 1:left.find(")")]
            inputs = tuple(
                int(x.strip()) for x in args.split(",") if x.strip()
            )

            return inputs, expected

        except Exception:
            return None, None

    # -----------------------------
    # EVALUATION (FIXED)
    # -----------------------------
    def evaluate(self, result, expected):

        is_fail = str(result) != str(expected)

        return "FAIL" if is_fail else "PASS"

    # -----------------------------
    # RUN TESTS
    # -----------------------------
    def run_tests(self):
        print("\n--- TEST RUNNER STARTED ---\n")

        test_files = self.load_test_files()

        total = 0
        passed = 0
        failed = 0

        for filename, data in test_files:

            func_name = self.extract_function_name(filename)

            print(f"\nFile: {filename} → Function: {func_name}")

            for category, tests in data.items():

                print(f"\n  [{category}]")

                for test in tests:

                    if not isinstance(test, str):
                        print(f"   SKIPPED NON-STRING: {test}")
                        continue

                    inputs, expected = self.parse_test_case(test)

                    if inputs is None:
                        print(f"   SKIPPED INVALID: {test}")
                        continue

                    total += 1

                    # MUTATION TRACKING (FIXED)
                    if "mutation" in category.lower():
                        self.mutants_total += 1

                    result, error = self.execute_function(func_name, inputs)

                    if error:
                        print(f"   ERROR: {error}")
                        failed += 1
                        continue

                    status = self.evaluate(result, expected)

                    if status == "PASS":
                        passed += 1
                    else:
                        failed += 1

                        if "mutation" in category.lower():
                            self.mutants_killed += 1

                    print(f"   {status}: {test} | Got: {result}")

        # -----------------------------
        # FINAL REPORT
        # -----------------------------
        print("\n--- SUMMARY ---")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

        if total > 0:
            print(f"Success Rate: {round((passed / total) * 100, 2)}%")

        if self.mutants_total > 0:
            score = (self.mutants_killed / self.mutants_total) * 100
            print(f"Mutation Score: {round(score, 2)}%")

        print(f"Conditions Covered: {len(self.conditions_hit)}")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    runner = TestRunner()
    runner.run_tests()