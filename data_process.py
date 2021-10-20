from typing import Dict

import recall

steps = {"初始访问": "战略阶段--1001",
         "技术信息收集": "战略阶段--1002",
         "执行": "战略阶段--1003",
         "权限提升": "战略阶段--1004",
         "横向移动": "战略阶段--1005",
         "凭据访问": "战略阶段--1006"}


def demo_recall(entry: Dict[str, list]) -> Dict[str, list]:
    result = dict()
    for key, values in entry.items():
        result[key] = [val + "123" for val in values]

    return result


def link_steps(entry: Dict[str, list]) -> Dict[str, list]:
    result = entry.copy()
    for key, values in entry.items():
        if key == "zljd_mc":
            result["zljd_id"] = [steps[v] for v in values]
    return result


def ld_data_clean(entry: Dict[str, list]) -> Dict[str, list]:
    if "ld_mc" in entry.keys() and len(entry["ld_mc"]) != 0:
        return entry
    else:
        return dict()


def gjmb_data_clean(entry: Dict[str, list]) -> Dict[str, list]:
    if "gjmb_mc" in entry.keys() and len(entry["gjmb_mc"]) != 0:
        return entry
    else:
        return dict()


def pre_process(data: Dict[str, list], **kwargs) -> Dict[str, list]:
    for _, v in kwargs.items():
        if kwargs.__contains__("prefix") and kwargs["prefix"] != "":
            data["output_prefix"] = v

    return data


def relation_recall(entry: Dict[str, list]) -> Dict[str, list]:
    if entry[":START_ID"] != "" and entry[":END_ID"] != "":
        return entry
    return dict()


def init():
    recall.register_preprocess(pre_process)
    recall.register_recall("demo", demo_recall)
    recall.register_recall("link_steps", link_steps)
    recall.register_recall("relation_recall", relation_recall)
