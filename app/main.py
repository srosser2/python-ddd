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

class Batch:
    def __init__(self, reference, sku, quantity) -> None:
        self.reference = reference
        self.sku = sku
        self.quantity = quantity

    def allocate_order(self, quantity):
        if self.quantity < quantity:
            raise Exception("Insufficient quantity")
        self.quantity -= quantity
        return Order('Ref', [{ 'sku': self.sku, 'quantity': quantity }])
