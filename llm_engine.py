def generate_tests(code_snippet, function_name):
    """
    Mock LLM that simulates AI test case generation.
    Produces Whitebox, Blackbox, BVA, ECP tests.
    """

    # ---------------- ADD FUNCTION ----------------
    if function_name == "add":
        return {
            "whitebox": [
                "Test add(2, 3) → 5",
                "Test add(-1, 1) → 0"
            ],
            "blackbox": [
                "Valid integers",
                "Negative + positive input"
            ],
            "bva": [
                "add(0, 0)",
                "add(999999, 1)"
            ],
            "ecp": [
                "Positive integers class",
                "Negative integers class"
            ]
        }

    # ---------------- DIVIDE FUNCTION ----------------
    elif function_name == "divide":
        return {
            "whitebox": [
                "Test divide(10, 2) → 5",
                "Test divide(10, 0) → Error"
            ],
            "blackbox": [
                "Normal division",
                "Division by zero handling"
            ],
            "bva": [
                "denominator = 1",
                "denominator = 0",
                "denominator = -1"
            ],
            "ecp": [
                "Valid numbers",
                "Invalid (zero denominator)"
            ]
        }

    # ---------------- DISCOUNT FUNCTION ----------------
    elif function_name == "calculate_discount":
        return {
            "whitebox": [
                "price=100, discount=10 → 10",
                "price=100, discount=0 → 0"
            ],
            "blackbox": [
                "Valid discount range (0–100)",
                "Invalid discount (>100 or <0)"
            ],
            "bva": [
                "0%, 1%, 100%",
                "-1%, 101%"
            ],
            "ecp": [
                "Valid range class",
                "Invalid range class"
            ]
        }

    # ---------------- DEFAULT ----------------
    return {
        "whitebox": ["Generic test case 1"],
        "blackbox": ["Generic input/output validation"],
        "bva": ["Boundary values test"],
        "ecp": ["Equivalence class test"]
    }
