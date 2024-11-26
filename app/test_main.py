import pytest
from app.main import OrderLine, Batch, allocate, OutOfStock
from datetime import datetime, timedelta


def test_batch_quantity_decreases_on_order_allocation():
    batch = Batch('ref', 'SMALL-TABLE', 20, eta=None)
    order_line = OrderLine("ref", 'SMALL-TABLE', 2)
    batch.allocate(order_line)
    assert batch.get_available_quantity == 18

def test_doesnt_decrease_if_insufficient_quantity():
    batch = Batch('ref', 'RED-CHAIR', 10, eta=None)
    order_line = OrderLine("ref", 'RED-CHAIR', 12)
    batch.allocate(order_line)
    assert batch.get_available_quantity == 10

def test_doesnt_decrease_if_with_incorrect_sku():
    batch = Batch('ref', 'SMALL-TABLE', 2, eta=None)
    order_line = OrderLine("ref", 'RED-CHAIR', 1)
    batch.allocate(order_line)
    assert batch.get_available_quantity == 2

def test_cant_allocate_same_line_multiple_times():
    batch = Batch('ref', 'BLUE-VASE', 10, eta=None)
    order_line = OrderLine("ref", 'BLUE-VASE', 2)
    batch.allocate(order_line)
    batch.allocate(order_line)
    assert batch.get_available_quantity == 8

def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, timedelta(days=1))
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.get_available_quantity == 90
    assert shipment_batch.get_available_quantity == 100

def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=None)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=timedelta(days=1))
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=timedelta(days=2))
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.get_available_quantity == 90
    assert medium.get_available_quantity == 100
    assert latest.get_available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=timedelta(days=1))
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference

# def test_raises_out_of_stock_exception_if_cannot_allocate():
#     batch = Batch("batch1", "SMALL-FORK", 10, eta=timedelta(days=1))
#     allocate(OrderLine("order1", "SMALL-FORK", 10), [batch])

#     with pytest.raises(OutOfStock):
#         allocate(OrderLine("order2", "SMALL-FORK", 1), [batch])