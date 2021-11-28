from MtTools import Mt_from_file
from MT import Mt

def is_prime_number(path_to_mt_config:str, word:int) -> bool:
    mt = Mt_from_file(path_to_mt_config)
    if word < 0:
        word = -1 * word

    word_lst = ['1'] * word
    mt.set_word(word_lst)
    return mt.run()

if __name__ == "__main__":
    for i in range(0, 25):
        res = is_prime_number("Results\\Mt_config.txt", i)
        print(f"input: {i}, result: {res}")
    print("end of code")
