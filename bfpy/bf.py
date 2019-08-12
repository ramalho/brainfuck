#!/usr/bin/env python3

import sys

MEMORY_LEN = 30_000

HELLO = (
    '++++++++++[>+++++++>++++++++++>+++<<<-]>++.>+.+++++++..+++.>++.'
    '<<+++++++++++++++.>.+++.------.--------.>+.'
)


class Interpreter:

    actions = {
        symbol: name
        for symbol, name in [
            ('>', 'inc_ptr'),
            ('<', 'dec_ptr'),
            ('+', 'inc'),
            ('-', 'dec'),
            ('.', 'output'),
            (',', 'input'),
            ('[', 'conditional_jump'),
            (']', 'jump_back'),
        ]
    }

    def __init__(self, source_code, *, pc=0, ptr=0, visible=False):
        if visible:
            self.code = self.compact(source_code)
        else:
            self.code = source_code
        self.pc = pc  # program counter (a.k.a. instruction pointer)
        self.data = bytearray(MEMORY_LEN)
        self.ptr = ptr  # data pointer
        self.visible = visible
        self.loops = []

    def inc_ptr(self):
        self.ptr += 1
        assert self.ptr < len(self.data), f'ptr={self.ptr}'

    def dec_ptr(self):
        self.ptr -= 1
        assert self.ptr >= 0, f'ptr={self.ptr}'

    def inc(self):
        if self.data[self.ptr] < 255:
            self.data[self.ptr] += 1
        else:
            self.data[self.ptr] = 0

    def dec(self):
        if self.data[self.ptr] > 0:
            self.data[self.ptr] -= 1
        else:
            self.data[self.ptr] = 255

    def output(self):
        char = chr(self.data[self.ptr])
        if self.visible:
            print(repr(char))
        else:
            print(char, end='')

    def input(self):
        self.data[self.ptr] = ord(sys.stdin.read(1))

    def index_loop_end(self):
        '''find index of matching ]''' 
        level = 0
        start = self.pc + 1
        for offset, instruction in enumerate(self.code[start:]):
            if instruction == ']':
                if level == 0:
                    return start + offset
                else:
                    level -= 1
            elif instruction == '[':
                level += 1
        raise LookupError("No matching ']'")

    def conditional_jump(self):
        '''jump past end of loop if current cell == zero'''
        loop_end = self.index_loop_end()
        self.loops.append((self.pc, loop_end))
        if self.data[self.ptr] == 0:
            self.pc = loop_end + 1
            self.loops.pop()
        else:
            self.pc += 1

    def jump_back(self):
        self.pc, _ = self.loops[-1]


    def compact(self, code):
        return ''.join(c for c in code if c in Interpreter.actions)

    def show_state(self):
        for i, v in enumerate(reversed(self.data)):
            if v > 0:
                break
        data_len = len(self.data) - i
        octets = ' '.join('%02x' % octet for octet in self.data[:data_len])
        print(self.code, '│', octets)
        left_pad = ' ' * self.pc
        middle_pad = ' ' * (len(self.code) - self.pc)
        right_pad = '   ' * self.ptr
        print(left_pad + '↑' + middle_pad + '│' + right_pad + ' ↑↑')
        print()

    def step(self):
        instruction = self.code[self.pc]

        action_name = Interpreter.actions.get(instruction, '')

        if action_name:
            getattr(self, action_name)()

        if 'jump' not in action_name:
            self.pc += 1

        if action_name and self.visible:
            self.show_state()

    def run(self):
        if self.visible:
            self.show_state()
        while self.pc != len(self.code):
            self.step()


def read(file_name):
    try:
        with open(file_name) as fp:
            return fp.read()
    except OSError as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    if '-v' in sys.argv:
        visible = True
        sys.argv.remove('-v')
    else:
        visible = False

    if len(sys.argv) == 2:
        source_code = read(sys.argv[1])

    else:
        source_code = HELLO

    Interpreter(source_code, visible=visible).run()
