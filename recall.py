recall_table = dict()


def register_recall(recall_name, recall):
    recall_table[recall_name] = recall


def get_recall(recall_name):
    return recall_table[recall_name]


def is_registered(recall_name):
    return recall_table.__contains__(recall_name)


