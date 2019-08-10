#!/usr/bin/env python3

import sys

MEMORY_LEN = 30_000

HELLO = ('++++++++++[>+++++++>++++++++++>+++<<<-]>++.>+.+++++++..+++.>++.'
         '<<+++++++++++++++.>.+++.------.--------.>+.')

class Interpreter:

    actions = {ord(symbol): name for symbol, name in 
                [('>', 'inc_ptr'),
                 ('<', 'dec_ptr'),
                 ('+', 'inc'),
                 ('-', 'dec'),
                 ('.', 'output'),
                 (',', 'input'),
                 ('[', 'conditional_jump'),
                 (']', 'jump_back'),
                ]}


    def __init__(self, source_code, *, visible=False):
        self.code = source_code.encode('ASCII')
        self.data = bytearray(MEMORY_LEN)
        self.ptr = 0  # data pointer
        self.pc = 0  # program counter (a.k.a. instruction pointer)
        self.visible = visible

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

    def conditional_jump(self):
        if self.data[self.ptr] == 0:
            self.pc = self.code.index(b']', self.pc)

    def jump_back(self):
        self.pc = self.code.rindex(b'[', 0, self.pc) - 1


    def show_state(self):
        for i, v in enumerate(reversed(self.data)):
            if v > 0: break
        data_len = len(self.data) - i
        source = self.code.decode('ASCII').strip()
        octets = ' '.join('%02x' % octet for octet in self.data[:data_len])
        print(source, '│', octets)
        left_pad = ' ' * self.pc
        middle_pad = ' ' * (len(source) - self.pc)
        right_pad = '   ' * self.ptr
        print(left_pad + '↑' + middle_pad + '│' + right_pad + ' ↑↑')
        print()


    def step(self):
        instruction = self.code[self.pc]

        action_name = Interpreter.actions.get(instruction)

        if action_name:
            getattr(self, action_name)()

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
