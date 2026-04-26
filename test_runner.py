from Artifact_Study import SimpleCalculator

def run_tests():
    calc = SimpleCalculator()

    test_cases = [
        # format: (function, inputs, expected_output)
        (calc.add, (2, 3), 5),
        (calc.add, (-1, 1), 0),

        (calc.divide, (10, 2), 5),
        (calc.divide, (10, 0), "error"),

        (calc.calculate_discount, (100, 10), 90),
    ]

    print("\n--- TEST RUNNER OUTPUT ---\n")

    for func, inputs, expected in test_cases:
        try:
            result = func(*inputs)

            if result == expected:
                print(f"{func.__name__}{inputs} → PASS ✔")
            else:
                print(f"{func.__name__}{inputs} → FAIL ❌ (expected {expected}, got {result})")

        except Exception as e:
            print(f"{func.__name__}{inputs} → ERROR ❌ ({e})")


if __name__ == "__main__":
    run_tests()
