# Form Helper: 根据配置文件约束的分表工具

## 使用场景：

需要将单一的K-V数据源分散输入到多个目标文件中。K-V数据源可以是json消息，数据库，excel表格。（日常实验室搬砖场景）

## 系统设计：

本工具是一个基于配置文件约束的可拓展前后端分离工具。通过简单编写配置文件并搭配合适的前端（如web，app），即可进行自动化工作，代替繁重机械的人力实验室搬砖工作。

##### 配置文件格式：

配置文件采用json的方式进行编写和解析，以下是一个参考配置文件：

```json
{
  "ID": {
    "filePath": "./dataset/entity/",
    "fileName": "被攻击组织",
    "fileType": "csv",
    "fields": {"id": "id:ID",
               "country": "国籍",
               "industry": "行业",
               "name": "名称",
               "description": "描述",
               "type": "类别",
               "location": "所在地",
               "function": "职能"},
    "recall": "demo"
  }

}
```

每个输出文件由一个json项表示：

1. ID：全局唯一即可
2. filePath：文件的输出路径，建议使用相对路径
3. fileName：文件名，无需跟后缀
4. fileType：输出类型（目前仅支持csv）
5. fields：输出的key与K-V源的key的映射，例如`id`为K-V源的一个key，`id:ID`为输出文件的一个key（即excel表格的表头）。
6. recall：该输出文件需要进行数据处理的回调函数的标识，如果不需要可忽略或直接置空。

##### 回调函数：

在一些场景下，输入的数据需要进行一定的处理再输出到指定文件中（例如输入的数据为20210102，输出需为2021-01-02）。用户可以编写data_process.py，自定义数据处理回调函数。以下为一个回调函数demo：

```python
def demo_recall(entry: Dict[str, list]) -> Dict[str, list]:
    result = dict()
    for key, values in entry.items():
      	# 该回调会为每一个数据项后加字符串123
        result[key] = [val + "123" for val in values]

    return result
  
def init():
    recall.register_recall("demo", demo_recall)
```

**请注意：**由于python是动态类型，所以只能在回调函数的签名上进行约束，请务必保证回调函数的签名为`def your_demo(entry: Dict[str, list]) -> Dict[str, list]:`

回调函数的输入entry为待处理的输出数据项，key对应该输出文件的key。value是一个列表项，里面为待处理的一批数据。

##### 数据预处理：

支持对输入的数据进行预处理（因为数据进入回调后即无法改变回调绑定的配置文件之外的数据）。recall提供注册预处理函数的api：`recall.register_preprocess(your_pre_process)`。回调函数在data_precess.py中编写。

```python
def pre_process(data: Dict[str, list], **kwargs) -> Dict[str, list]:
    for _, v in kwargs.items():
        if kwargs.__contains__("prefix") and kwargs["prefix"] != "":
            data["output_prefix"] = v

    return data
```

（为了实现按路由分别输出不同的目录，在预处理函数中耦合一段逻辑，这样不甚合理，期待后人修改）

## Quick Start：

配置环境：python 3.8

准备工作：请自行准备适合的虚拟环境

安装依赖：`pip install -r requirements.txt`

启动：`python3 main.py` 或 `python3 main.py your_ip your_port`(自定义ip port)

```bash
INFO:   Started server process [32883]

INFO:   Waiting for application startup.

INFO:   Application startup complete.

INFO:   Uvicorn running on **http://127.0.0.1:9090** (Press CTRL+C to quit)
```

终端输出如上信息即启动成功。


