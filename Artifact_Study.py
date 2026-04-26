class SimpleCalculator:
    """
    A simple calculator to test the LLM Testing Tool.
    Supports basic math and a percentage-based discount logic.
    """
    
    def add(self, a, b):
        return a + b

    def divide(self, numerator, denominator):
        if denominator == 0:
            return "Error: Division by zero"
        return numerator / denominator

    def calculate_discount(self, price, discount_percent):
        # Good for BVA (0, 100, and negative numbers)
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Invalid discount percentage")
        
        if price <= 0:
            return 0.0
            
        return price * (discount_percent / 100)
