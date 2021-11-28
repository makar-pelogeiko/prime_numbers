from MtTools import Mt_from_file
from MT import Mt
from GrammarT0 import GrammarFree
from prime_number_by_MT import is_prime_number


def grammar_creation(path_to_mt_config: str, word: int) -> str:
    mt = Mt_from_file(path_to_mt_config)
    if word < 0:
        word = -1 * word

    gr_to = GrammarFree.from_Mt(mt)

    grammar_str = gr_to.to_text()
    f = open("grammar.txt", "w")
    f.write(grammar_str)
    f.close()

    result = gr_to.run(word)
    return result


if __name__ == "__main__":
    for i in range(0, 25):
        res = is_prime_number("Mt_config.txt", i)
        print(f"input: {i}, result: {res}")
        if res:
            gram_str = grammar_creation("Mt_config.txt", i)
            print(f"result of Grammar works: '{gram_str}'")

    print("End of code")
