from app.main import OrderLine, Batch

def test_batch_quantity_decreases_on_order_allocation():
    batch = Batch('ref', 'SMALL-TABLE', 20)
    order_line = OrderLine('SMALL-TABLE', 2)
    batch.allocate(order_line)
    assert batch.get_available_quantity == 18

def test_doesnt_decrease_if_insufficient_quantity():
    batch = Batch('ref', 'RED-CHAIR', 10)
    order_line = OrderLine('RED-CHAIR', 12)
    batch.allocate(order_line)
    assert batch.get_available_quantity == 10

def test_doesnt_decrease_if_with_incorrect_sku():
    batch = Batch('ref', 'SMALL-TABLE', 2)
    order_line = OrderLine('RED-CHAIR', 1)
    batch.allocate(order_line)
    assert batch.get_available_quantity == 2

def test_cant_allocate_same_line_multiple_times():
    batch = Batch('ref', 'BLUE-VASE', 10)
    order_line = OrderLine('BLUE-VASE', 2)
    batch.allocate(order_line)
    batch.allocate(order_line)
    assert batch.get_available_quantity == 8
