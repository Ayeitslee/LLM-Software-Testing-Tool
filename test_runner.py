import os
import json
from Artifact_Study import SimpleCalculator


class TestRunner:
    def __init__(self, test_folder="Test_Folder"):
        self.test_folder = test_folder
        self.calc = SimpleCalculator()

        # Metrics
        self.mutants_total = 0
        self.mutants_killed = 0
        self.conditions_hit = set()

        # Results
        self.total = 0
        self.passed = 0
        self.failed = 0

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
            return None, f"Function {func_name} not found"

        # Whitebox tracking (light simulation)
        if func_name == "divide":
            self.conditions_hit.add("divide_branch")

        if func_name == "calculate_discount":
            self.conditions_hit.add("discount_branch")

        try:
            return func(*inputs), None
        except Exception as e:
            return str(e), None

    # -----------------------------
    # SAFE TEST PARSER
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

        except Exception:
            return None, None

    # -----------------------------
    # EVALUATION (FIXED TYPE HANDLING)
    # -----------------------------
    def evaluate(self, result, expected):

        try:
            # numeric-safe comparison
            if isinstance(result, float):
                result = round(result, 2)

            return "PASS" if str(result) == str(expected) else "FAIL"
        except:
            return "FAIL"

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

                for test in tests:

                    if not isinstance(test, str):
                        print(f"   INVALID TEST FORMAT: {test}")
                        continue

                    inputs, expected = self.parse_test_case(test)

                    if inputs is None:
                        print(f"   INVALID PARSE: {test}")
                        continue

                    self.total += 1

                    # Mutation tracking
                    if "mutation" in category.lower():
                        self.mutants_total += 1

                    result, error = self.execute_function(func_name, inputs)

                    if error:
                        print(f"   ERROR: {error}")
                        self.failed += 1
                        continue

                    status = self.evaluate(result, expected)

                    if status == "PASS":
                        self.passed += 1
                    else:
                        self.failed += 1

                        if "mutation" in category.lower():
                            self.mutants_killed += 1

                    print(f"   {status}: {test} | Got: {result}")

        self.generate_report()

    # -----------------------------
    # FINAL REPORT (NEW FEATURE)
    # -----------------------------
    def generate_report(self):

        mutation_score = 0
        if self.mutants_total > 0:
            mutation_score = (self.mutants_killed / self.mutants_total) * 100

        report = {
            "total_tests": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "success_rate": round((self.passed / self.total) * 100, 2) if self.total else 0,
            "mutation_total": self.mutants_total,
            "mutants_killed": self.mutants_killed,
            "mutation_score": round(mutation_score, 2),
            "conditions_covered": len(self.conditions_hit)
        }

        print("\n--- FINAL SUMMARY ---")
        print(json.dumps(report, indent=4))

        # Save report file
        with open("report.json", "w") as f:
            json.dump(report, f, indent=4)

        print("\n✔ Report saved to report.json")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    runner = TestRunner()
    runner.run_tests()
