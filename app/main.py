def add_numbers(a: int, b: int) -> int:
    """Function to add two numbers."""
    return a + b

class Product:
    def __init__(self, sku):
        self.sku = sku

class Order:
    def __init__(self, order_reference, order_lines):
        self.order_reference = order_reference
        self.order_lines = order_lines
