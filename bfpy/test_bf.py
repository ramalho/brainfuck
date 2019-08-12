import pytest

from bf import Interpreter

@pytest.mark.parametrize('src, pc, expected', [
    ('[]', 0, 1),
    ('[+]', 0, 2),
    ('[[]]', 0, 3),
    ('[[]]', 1, 2),
    ('[-[-[-]-]-]', 0, 10),
    ('[-[-[-]-]-]', 2, 8),
    ('[-[-]-[-]-]', 0, 10),
    ('[-[-]-[-]-]', 2, 4),
])
def test_index_loop_end(src, pc, expected):
    interpreter = Interpreter(src, pc=pc)
    result = interpreter.index_loop_end()
    assert result == expected


@pytest.mark.parametrize('src, pc', [
    ('[', 0),
    ('[+', 0),
    ('[[]', 0),
])
def test_index_loop_end_exception(src, pc):
    with pytest.raises(LookupError) as excinfo:
        interpreter = Interpreter(src, pc=pc)
        _ = interpreter.index_loop_end()
    assert "No matching ']'" in str(excinfo.value)


@pytest.mark.parametrize('src, end_pc', [
    ('[]', 2),
    ('[>>>]', 5),
    ('[>[>]>]', 7),
])
def test_jump_forward(src, end_pc):
    interpreter = Interpreter(src)
    interpreter.step()
    assert interpreter.pc == end_pc

@pytest.mark.parametrize('src, steps, end_pc', [
    ('+[-]', 0, 0),
    ('+[-]', 1, 1),
    ('+[-]', 2, 2),
    ('+[-]', 3, 3),
    ('+[-]', 4, 1),
    ('+[-]', 5, 4),
])
def test_jump_back(src, steps, end_pc):
    interpreter = Interpreter(src)
    for _ in range (steps):
        interpreter.step()
    assert interpreter.pc == end_pc

def test_add_cells():
    interpreter = Interpreter('++>+++<[->+<]')
    interpreter.run()
    assert interpreter.data.startswith(bytearray([0, 5]))
