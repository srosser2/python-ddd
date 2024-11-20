import pytest
from app.main import add_numbers, Batch

def test_add_numbers():
    """Test case for add_numbers function."""
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0

def test_raises_exeption_if_insufficient_quantity():
    with pytest.raises(Exception):
        table_batch = Batch('ref', 'SMALL-TABLE', 1)
        table_batch.allocate_order(2)

def test_batch_quantity_decreases_on_order_allocation():
    table_batch = Batch('ref', 'SMALL-TABLE', 2)
    table_batch.allocate_order(2)
    assert table_batch.quantity == 0