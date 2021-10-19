recall_table = dict()


def register_recall(recall_name, recall):
    recall_table[recall_name] = recall


def get_recall(recall_name):
    return recall_table[recall_name]


def is_registered(recall_name):
    return recall_table.__contains__(recall_name)


def is_preprocess_registered():
    return recall_table.__contains__("preprocess")


def get_preprocess_recall():
    if is_preprocess_registered():
        return recall_table["preprocess"], True
    else:
        return None, False


def register_preprocess(recall):
    recall_table["preprocess"] = recall