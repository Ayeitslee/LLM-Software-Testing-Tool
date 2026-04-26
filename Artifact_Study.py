class SimpleCalculator:
    """
    Simple calculator for testing framework
    """

    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

    def divide(self, numerator, denominator):
        if denominator == 0:
            return "error"
        return numerator / denominator

    def calculate_discount(self, price, discount_percent):
        if discount_percent < 0 or discount_percent > 100:
            return "error"

        if price <= 0:
            return 0.0

        return price * (discount_percent / 100)