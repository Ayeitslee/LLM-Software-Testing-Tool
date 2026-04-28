class SimpleCalculator:
    """
    A simple calculator to test the LLM Testing Tool.
    Supports basic math and a percentage-based discount logic.
    """

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, numerator, denominator):
        if denominator == 0:
            raise ZeroDivisionError("Division by zero")
        return numerator / denominator

    def calculate_discount(self, price, discount_percent):
        # Boundary Value Analysis (BVA)

        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Invalid discount percentage")

        if price <= 0:
            return 0.0

        return price * (discount_percent / 100)


# ==============================
# Demo / Execution Block
# ==============================
if __name__ == "__main__":
    calc = SimpleCalculator()

    print("\n====================")
    print("Testing SimpleCalculator")
    print("====================\n")

    # Basic arithmetic operations
    print("Add:", calc.add(2, 3))
    print("Subtract:", calc.subtract(10, 4))
    print("Multiply:", calc.multiply(3, 5))
    print("Divide:", calc.divide(20, 4))

    # Exception handling for division by zero
    try:
        print("Divide by zero:", calc.divide(10, 0))
    except ZeroDivisionError as e:
        print("Divide by zero:", e)

    # Discount logic tests
    print("Discount (valid):", calc.calculate_discount(100, 20))
    print("Discount (edge case 0%):", calc.calculate_discount(100, 0))