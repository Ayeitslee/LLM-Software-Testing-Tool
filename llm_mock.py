def generate_tests(prompt):
    """
    Mock LLM generator for test cases.
    Simulates AI output without needing any API.
    """

    if "divide" in prompt:
        return """
WHITEBOX TESTS:
- divide(10, 2) → 5
- divide(10, 0) → "Error: Division by zero"

BLACKBOX TESTS:
- Valid inputs (10, 2)
- Edge case (0 denominator)

BVA:
- numerator = 0, denominator = 1
- denominator = 0
"""

    elif "add" in prompt:
        return """
WHITEBOX TESTS:
- add(2, 3) → 5
- add(-1, 1) → 0

BLACKBOX TESTS:
- Positive numbers
- Negative numbers

BVA:
- 0, 1, -1 values
"""

    elif "calculate_discount" in prompt:
        return """
WHITEBOX TESTS:
- price=100, discount=10 → 10
- price=100, discount=0 → 0

BLACKBOX TESTS:
- discount = 0
- discount = 100
- invalid discount = -1 → Error

BVA:
- 0%, 100%, -1%, 101%
"""

    return """
WHITEBOX TESTS:
- Generic test case 1
- Generic test case 2

BLACKBOX TESTS:
- Input validation
- Output verification

BVA:
- Boundary checks applied
"""
