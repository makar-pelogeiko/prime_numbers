from MT import Mt

def Mt_from_file(path: str)->Mt:
    try:
        file = open(path, "r")
        text_mt = file.read()
        file.close()
    except:
        print("can not open and read file")

    mt = None
    try:
        mt = Mt.from_text(text_mt)
    except:
        print("not a mt syntax in file")
        mt = None
    return mt