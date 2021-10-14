from typing import Dict

import recall


def demo_recall(entry: Dict[str, list]) -> Dict[str, list]:
    result = dict()
    for key, values in entry.items():
        result[key] = [val + "123" for val in values]

    return result


def init():
    recall.register_recall("demo", demo_recall)
