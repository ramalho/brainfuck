
import sys
 
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


    def __init__(self, source_code):
        self.code = source_code.encode('ASCII')
        self.data = bytearray(1)  # one cell, zero-filled
        self.ptr = 0  # data pointer
        self.pc = 0  # program counter (a.k.a. instruction pointer)

    def inc_ptr(self):
        self.ptr += 1

    def dec_ptr(self):
        self.ptr -= 1

    def inc(self):
        if self.ptr == len(self.data):
            self.data.extend([0])
        if self.data[self.ptr] < 255:
            self.data[self.ptr] += 1
        else:
            self.data[self.ptr] = 0

    def dec(self):
        if self.ptr == len(self.data):
            self.data.extend([0])
        if self.data[self.ptr] > 0:
            self.data[self.ptr] -= 1
        else:
            self.data[self.ptr] = 255

    def output(self):
        sys.stdout.write(chr(self.data[self.ptr]))

    def input(self):
        if self.ptr == len(self.data):
            self.data.extend([0])
        self.data[self.ptr] = ord(sys.stdin.read(1))

    def conditional_jump(self):
        if self.data[self.ptr] == 0:
            self.pc = self.code.index(b']', self.pc)
            print(f'new pc: {self.pc}')
        else:
            print()

    def jump_back(self):
        self.pc = self.code.rindex(b'[', 0, self.pc) - 1


    def show_state(self):
        octets = ' '.join('%02x' % octet for octet in self.data)
        print(self.code.decode('ASCII'), '│', octets)
        left_pad = ' ' * self.pc
        middle_pad = ' ' * (len(self.code) - self.pc)
        right_pad = '   ' * self.ptr
        print(left_pad + '↑' + middle_pad + '│' + right_pad + ' ↑↑')
        print()


    def step(self, verbose=False):
        instruction = self.code[self.pc]

        action_name = Interpreter.actions[instruction]

        if action_name:
            getattr(self, action_name)()

        self.pc += 1

        if verbose:
            self.show_state()

    def run(self):
        self.show_state()
        while self.pc != len(self.code):
            self.step(True)
