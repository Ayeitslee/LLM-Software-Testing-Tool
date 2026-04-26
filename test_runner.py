import os
import json
from Artifact_Study import SimpleCalculator


class TestRunner:
    def __init__(self, test_folder="Test_Folder"):
        self.test_folder = test_folder
        self.calc = SimpleCalculator()

    def load_test_files(self):
        """Load all JSON test files recursively from Test_Folder"""
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
                        print(f"[!] Skipping invalid JSON: {file}")

        return test_files

    def extract_function_name(self, filename):
        """Infer function name from filename"""
        return filename.replace("_tests.json", "").replace(".json", "")

    def execute_function(self, func_name, inputs):
        """Dynamically call function from SimpleCalculator"""
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
        Convert:
        add(2,3)=5
        into:
        inputs=(2,3), expected=5
        """

        if "=" not in test_case:
            return None, None

        left, expected = test_case.split("=")
        expected = expected.strip()

        try:
            args = left[left.find("(") + 1:left.find(")")]
            inputs = tuple(
                eval(arg.strip())
                for arg in args.split(",")
                if arg.strip() != ""
            )
            return inputs, expected
        except Exception:
            return None, None

    def evaluate(self, result, expected):
        """Return PASS or FAIL"""
        if str(result) == str(expected):
            return "PASS"
        return "FAIL"

    def save_report(self, report, filename="test_report.json"):
        """Save final report"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        print(f"\n[✔] Report saved to {filename}")

    def run_tests(self):
        print("\n--- TEST RUNNER STARTED ---\n")

        test_files = self.load_test_files()

        report = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "tests": []
        }

        for filename, data in test_files:

            func_name = self.extract_function_name(filename)

            print(f"\nFile: {filename} → Function: {func_name}")

            for category, tests in data.items():

                print(f"\n  [{category}]")

                for test in tests:
                    report["total"] += 1

                    if isinstance(test, str) and "=" in test:

                        inputs, expected = self.parse_test_case(test)

                        if inputs is None:
                            print(f"   SKIPPED: {test}")
                            continue

                        result, error = self.execute_function(func_name, inputs)

                        if error:
                            status = "FAIL"
                            print(f"   ERROR: {error}")
                            report["failed"] += 1
                        else:
                            status = self.evaluate(result, expected)

                            if status == "PASS":
                                report["passed"] += 1
                            else:
                                report["failed"] += 1

                            print(f"   {status}: {test} | Got: {result}")

                        report["tests"].append({
                            "function": func_name,
                            "test": test,
                            "expected": expected,
                            "actual": result,
                            "status": status
                        })

                    else:
                        print(f"   SKIPPED INVALID FORMAT: {test}")

        # Summary
        print("\n--- SUMMARY ---")
        print(f"Total Tests: {report['total']}")
        print(f"Passed: {report['passed']}")
        print(f"Failed: {report['failed']}")

        if report["total"] > 0:
            rate = (report["passed"] / report["total"]) * 100
            print(f"Success Rate: {round(rate, 2)}%")

        # Save report
        self.save_report(report)


if __name__ == "__main__":
    runner = TestRunner()
    runner.run_tests()
