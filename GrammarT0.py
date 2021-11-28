from GElement import GType, Gelemnt
from MT import Mt


class GrammarFree:
    def __init__(self):
        self.nonterminals = set()
        self.terminals = set()
        self.productions = dict()
        self.start_nonterminal = None

        # For executing
        self.mt_start_state = None
        self.mt_final_states = set()
        self.mt_states = set()

    @classmethod
    def from_Mt(cls, mt: Mt):
        obj = cls()

        obj.mt_states = mt.states.copy()
        obj.mt_final_states = mt.final_states.copy()
        obj.mt_start_state = mt.start_state

        #######################################
        # nonterminals create
        temp_set = mt.alphabet.copy()
        temp_set.add('')
        first_symb_lst = list(temp_set - mt.alphabet_spec)
        second_symb_lst = list(mt.alphabet)

        for first in first_symb_lst:
            for second in second_symb_lst:
                nonterm = Gelemnt(GType.NonTerm_box, [first, second])
                obj.nonterminals.add(nonterm)

        for state in mt.states:
            nonterm = Gelemnt(GType.NonTerm_simpl, state)
            obj.nonterminals.add(nonterm)

        n_term_A1 = Gelemnt(GType.NonTerm_simpl, 'A1')
        n_term_A2 = Gelemnt(GType.NonTerm_simpl, 'A2')
        n_term_A3 = Gelemnt(GType.NonTerm_simpl, 'A3')
        n_term_epsilon = Gelemnt(GType.NonTerm_box, ['', 'B'])

        obj.nonterminals.update({n_term_A1,
                                 n_term_A2,
                                 n_term_A3})

        ##############################################################
        # terminals create
        obj.terminals = mt.alphabet - mt.alphabet_spec

        ##############################################################
        # start non terminal
        obj.start_nonterminal = n_term_A1

        ##############################################################
        # productions
        # start word
        obj.productions[n_term_A1] = [[n_term_A3, Gelemnt(GType.NonTerm_simpl, mt.start_state), n_term_A2]]

        obj.productions[n_term_A2] = [[n_term_epsilon, n_term_epsilon]]
        for symbol in mt.alphabet - mt.alphabet_spec:
            nonterm = Gelemnt(GType.NonTerm_box, [symbol, symbol])
            obj.productions[n_term_A2].append([nonterm, n_term_A2])

        # memory boxes
        obj.productions[n_term_A3] = [[n_term_A3, n_term_epsilon], ['']]

        # delta function elements
        keys = list(mt.delta.keys())
        for key in keys:
            for symbol in first_symb_lst:
                nterm_acting = Gelemnt(GType.NonTerm_box, [symbol, key[1]])
                nterm_end_act = Gelemnt(GType.NonTerm_box, [symbol, mt.delta[key][1]])
                nterm_beg_st = Gelemnt(GType.NonTerm_simpl, key[0])
                nterm_end_st = Gelemnt(GType.NonTerm_simpl, mt.delta[key][0])
                if mt.delta[key][2] == '<':
                    for neig_f in first_symb_lst:
                        for neig_s in second_symb_lst:
                            nterm_any = Gelemnt(GType.NonTerm_box, [neig_f, neig_s])
                            obj.productions[(nterm_any, nterm_beg_st, nterm_acting)] = \
                                [[nterm_end_st, nterm_any, nterm_end_act]]
                else:
                    obj.productions[(nterm_beg_st, nterm_acting)] = [[
                        nterm_end_act, nterm_end_st
                    ]]

        # final states & delete of trash
        for fin in mt.final_states:
            fin_nonterm = Gelemnt(GType.NonTerm_simpl, fin)
            obj.productions[fin_nonterm] = [['']]
            for first_sym in first_symb_lst:
                for second_sym in second_symb_lst:
                    box_nonterm = Gelemnt(GType.NonTerm_box, [first_sym, second_sym])

                    obj.productions[(box_nonterm, fin_nonterm)] = [[
                        fin_nonterm, first_sym, fin_nonterm
                    ]]
                    obj.productions[(fin_nonterm, box_nonterm)] = [[
                        fin_nonterm, first_sym, fin_nonterm
                    ]]

        return obj

    def to_text(self):
        res_str = '##start_nonTerminal##\n'
        res_str += self.start_nonterminal.data + '\n'

        res_str += '##Terminals##\n'
        term_lst = list(self.terminals)
        for term in term_lst:
            res_str += term + '\n'

        res_str += '##NonTerminals##\n'
        non_term_lst = list(self.nonterminals)
        for term in non_term_lst:
            res_str += str(term) + '\n'

        res_str += '##Productions##\n'
        for key, values in self.productions.items():
            key_str = ''
            if type(key) is Gelemnt:
                key_str = str(key)
            else:
                for item in key:
                    key_str += '-' + str(item)
                key_str = key_str[1:]

            for sub_lst in values:
                val_str = ''
                for val in sub_lst:
                    val_str += ',' + str(val)
                val_str = val_str[1:]
                res_str += key_str + ' -> ' + val_str + '\n'

        return res_str

    def run(self, word: int):

        file = open('log_grammar_run.txt', "w")
        file.write("#################### Create Word ####################\n")

        sentence = [self.start_nonterminal]
        self.logger(file, sentence, sentence[0], self.productions[sentence[0]][0])
        # Create word
        sentence = self.productions[sentence[0]][0]

        # TODO hardcode of 1111 alphabet: symbol_1 has to be = 1
        head = sentence[len(sentence) - 1]
        # symbol_1 = self.productions[head].index([c, head])
        sym_one = list(self.terminals)[0]
        symbol_1 = self.get_index_delta_term(self.productions[head],
                                             [Gelemnt(GType.NonTerm_box, [sym_one, sym_one]), head])

        for i in range(word):
            self.logger(file, sentence, sentence[len(sentence) - 1],
                        self.productions[sentence[len(sentence) - 1]][symbol_1])
            head = sentence.pop(len(sentence) - 1)
            sentence = sentence + self.productions[head][symbol_1]

        self.logger(file, sentence, sentence[len(sentence) - 1], self.productions[sentence[len(sentence) - 1]][0])

        head = sentence.pop(len(sentence) - 1)
        sentence = sentence + self.productions[head][0]

        file.write("#################### Create memory boxes ####################\n")
        # Create memory boxes
        for i in range(word * 3 + 5):
            self.logger(file, sentence, sentence[0], self.productions[sentence[0]][0])
            head = sentence.pop(0)
            sentence = self.productions[head][0] + sentence

        self.logger(file, sentence, sentence[0], self.productions[sentence[0]][1])
        head = sentence.pop(0)
        if not (self.productions[head][1] == ['']):
            print("POTENTIAL ERROR: epsilon expected")
            sentence = self.productions[head][1] + sentence

        file.write("#################### Mt imitation ####################\n")
        # Mt imitation
        curr_state_term = Gelemnt(GType.NonTerm_simpl, self.mt_start_state)
        keys = list(self.productions.keys())

        idx = sentence.index(curr_state_term)
        flag_stop = ((sentence[idx - 1], curr_state_term, sentence[idx + 1]) in keys) \
                    or ((curr_state_term, sentence[idx + 1]) in keys
                        and not (curr_state_term.data in self.mt_final_states))

        while (flag_stop):
            if (sentence[idx - 1], curr_state_term, sentence[idx + 1]) in keys:
                current_head = (sentence[idx - 1], curr_state_term, sentence[idx + 1])
                substitution = self.productions[(sentence[idx - 1], curr_state_term, sentence[idx + 1])][0]
                curr_state_term = substitution[0]
                idx_delete = idx - 1

            else:
                substitution = self.productions[(curr_state_term, sentence[idx + 1])][0]
                current_head = (curr_state_term, sentence[idx + 1])
                curr_state_term = substitution[1]
                idx_delete = idx

            self.logger(file, sentence, current_head, substitution)
            sentence = sentence[:idx_delete] + substitution + sentence[idx + 2:]

            idx = sentence.index(curr_state_term)
            flag_stop = ((sentence[idx - 1], curr_state_term, sentence[idx + 1]) in keys) \
                        or ((curr_state_term, sentence[idx + 1]) in keys
                            and not (curr_state_term.data in self.mt_final_states))

        file.write("###### Delete boxes Nonterminals (f[a, b]->faf, [a,b]f->faf) ######\n")
        # Delete boxes Nonterminals (f[a, b]->faf, [a,b]f->faf)
        idx_middle = idx
        while idx + 1 < len(sentence):
            substitution = self.productions[(sentence[idx], sentence[idx + 1])][0]
            self.logger(file, sentence, (sentence[idx], sentence[idx + 1]), substitution)

            if idx + 2 >= len(sentence):
                sentence = sentence[:idx] + substitution
            else:
                sentence = sentence[:idx] + substitution + sentence[idx + 2:]

            idx += 2

        idx = idx_middle
        while idx - 1 >= 0:
            substitution = self.productions[(sentence[idx - 1], sentence[idx])][0]
            self.logger(file, sentence, (sentence[idx - 1], sentence[idx]), substitution)

            if idx + 1 >= len(sentence):
                sentence = sentence[:idx - 1] + substitution
            else:
                sentence = sentence[:idx - 1] + substitution + sentence[idx + 1:]

            idx -= 1

        file.write("#################### Last deletion rule f->e ####################\n")
        for i in range(len(sentence)):
            if type(sentence[i]) is Gelemnt:
                self.logger(file, sentence, sentence[i], self.productions[sentence[i]][0])
                sentence[i] = self.productions[sentence[i]][0][0]

        file.write("#################### RESULT ####################\n")
        file.write(f"{''.join(sentence)}\n")
        file.close()

        return ''.join(sentence)

    def logger(self, file, sentence, key, product):
        # key
        key_str = self.key_to_str(key)

        # value
        val_str = self.product_to_str(product)

        # sentence
        sentence_str = ''
        for s in sentence:
            sentence_str += str(s) + '|'

        sentence_str = sentence_str[:len(sentence_str) - 1]

        file.write(f"{sentence_str}::    {key_str} -> {val_str}\n")

    @staticmethod
    def key_to_str(key):
        key_str = ''
        if type(key) is Gelemnt:
            key_str = str(key)
        else:
            for item in key:
                key_str += '_' + str(item)
            key_str = key_str[1:]
        return key_str

    @staticmethod
    def product_to_str(values):
        val_str = ''
        for val in values:
            val_str += ',' + str(val)
        val_str = val_str[1:]
        return val_str

    @staticmethod
    def get_index_delta_term(lst, element: list):
        index = -1
        for i in range(len(lst)):
            if len(lst[i]) == len(element):
                for j in range(len(lst[i])):
                    index = i
                    if lst[i][j].type != element[j].type:
                        index = -1
                        break

                    if element[j].type == GType.NonTerm_box:
                        if not (lst[i][j].data[0] == element[j].data[0]
                                and lst[i][j].data[1] == element[j].data[1]):
                            index = -1
                            break
                    else:
                        if not (lst[i][j].data == element[j].data):
                            index = -1
                            break
                if index != -1:
                    return index
        return index
