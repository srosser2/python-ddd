from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class OrderLine:
    sku: str
    quantity: int

@dataclass
class Order:
    order_reference: str
    order_lines: list[OrderLine]

class Batch:
    def __init__(self, reference: str, sku: str, quantity: int, eta: Optional[date] = None) -> None:
        self.reference = reference
        self.sku = sku
        self.quantity = quantity
        self.eta = eta
        self._purchased_quantity = quantity
        self._allocations = set()

    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.sku == order_line.sku and self.quantity >= order_line.quantity

    def allocate(self, order_line: OrderLine) -> None:
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    @property
    def get_allocated_quantity(self) -> int:
        return sum(order_line.quantity for order_line in self._allocations)
    
    @property
    def get_available_quantity(self) -> int:
        return self.quantity - self.get_allocated_quantity
