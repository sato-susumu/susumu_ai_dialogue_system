from susumu_ai_dialogue_system.infrastructure.limited_fifo import LimitedFIFO


def test_fifo_overflow():
    fifo = LimitedFIFO(3)
    fifo.put(1)
    fifo.put(2)
    fifo.put(3)
    fifo.put(4)
    assert fifo.get() == 2
    assert fifo.get() == 3
    assert fifo.get() == 4
    assert fifo.get() is None


def test_empty():
    fifo = LimitedFIFO(3)
    assert fifo.is_empty()
    fifo.put(1)
    assert not fifo.is_empty()
