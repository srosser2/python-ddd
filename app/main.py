from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int

@dataclass
class Order:
    order_reference: str
    order_lines: list[OrderLine]

class Batch:
    def __init__(self, reference: str, sku: str, quantity: int, eta: Optional[date]) -> None:
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

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

class OutOfStock(Exception):
    pass

def allocate(line, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference

    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
