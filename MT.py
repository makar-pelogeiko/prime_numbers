from DoubleLinkedList import DLinkedList as dList


class Mt:
    """
    :raise Exception("BAD DELTA ELEMENT")
    """
    def __init__(self):
        self.alphabet = set()
        self.alphabet_spec = set()
        self.memory_step = {'>', '<', '.'}
        self.states = set()
        self.start_state = None
        self.final_states = set()
        self.delta = dict()  # Dict[Tuple[state, symbol], Tuple[state, symbol, step]]

        # For working of MT
        self.is_passed = None
        self.is_started = False
        self.tape = dList(def_value='B')

    @classmethod
    def from_text(cls, text: str):
        """
        :raise Exception("BAD DELTA ELEMENT")
        """
        obj = cls()
        lines = text.splitlines()
        flag = 'alphabet'

        for line in lines:

            if flag == 'alphabet':
                if line == '####':
                    flag = 'spec_alphabet'
                    continue
                obj.alphabet.add(line)
                continue

            if flag == 'spec_alphabet':
                if line == '####':
                    flag = 'states'
                    continue
                obj.alphabet_spec.add(line)
                continue

            if flag == 'states':
                if line == '####':
                    flag = 'start_state'
                    continue
                obj.states.add(line)
                continue

            if flag == 'start_state':
                if line == '####':
                    flag = 'final_states'
                    continue
                obj.start_state = line
                continue

            if flag == 'final_states':
                if line == '####':
                    flag = 'delta'
                    continue
                obj.final_states.add(line)
                continue

            if flag == 'delta':
                if line == '####':
                    flag = 'stop'
                    continue
                delta_ln = line.split(' ')

                if not (delta_ln[0] in obj.states and delta_ln[1] in obj.alphabet and
                        delta_ln[2] in obj.states and delta_ln[3] in obj.alphabet and
                        delta_ln[4] in obj.memory_step):
                    print("Bad delta")
                    raise Exception("BAD DELTA ELEMENT")

                obj.delta[(delta_ln[0], delta_ln[1])] = (delta_ln[2], delta_ln[3], delta_ln[4])
                continue
        return obj

    def set_word(self, word):
        self.tape = dList(def_value='B')
        if len(word) == 0:
            return
        self.tape.data = word.pop(0)

        for symbol in word:
            self.tape.right_step()
            self.tape.data = symbol

        self.tape.get_to_left_end()
        return

    def run(self) -> bool:
        if not self.check_for_correct():
            print("<NOT CORRECT init stop running>")
            return False

        curr_state = self.start_state
        delta_keys = set(self.delta.keys())
        curr_symbol = self.tape.data

        self.is_started = True

        file = open('log_mt_run.txt', "w")

        while (curr_state, curr_symbol) in delta_keys:
            next_step = self.delta[(curr_state, curr_symbol)]
            file.write(f"{self.tape} - ({curr_state} {curr_symbol}): {next_step}\n")
            curr_state = next_step[0]
            step = next_step[2]

            self.tape.data = next_step[1]
            if step == '>':
                self.tape.right_step()
            elif step == '<':
                self.tape.left_step()

            curr_symbol = self.tape.data

        if curr_state in self.final_states:
            self.is_passed = True
            file.close()
            return True
        else:
            self.is_passed = False
            file.close()
            return False

    def check_for_correct(self) -> bool:
        # TODO check if all values are correct
        if self.start_state is None:
            print("No start state")
            return False

        if self.states is None:
            print("No states")
            return False

        if not (self.start_state in self.states):
            print("start_state not in states")
            return False

        if self.final_states is None:
            print("No final states obj")
            return False

        if not (self.final_states.issubset(self.states)):
            print("final_states not in states")
            return False

        return True
