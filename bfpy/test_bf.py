from bf import Interpreter


def test_add_cells():
    interpreter = Interpreter('++>+++<[->+<]')
    interpreter.run()
    assert interpreter.data == bytearray([0, 5])

