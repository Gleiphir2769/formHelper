import sys

import uvicorn
from fastapi import FastAPI, Request

import aof
import data_process
import writer

app = FastAPI()
form_writer = writer.formWriter("config.json")


@app.post("/send_data/{name}")
async def handle_data(request: Request, name: str):
    data_json = await request.json()
    result = form_writer.write_data(data_json, prefix=name)
    return {"result": result}


@app.post("/send_data")
async def handle_data(request: Request):
    data_json = await request.json()
    result = form_writer.write_data(data_json)
    return {"result": result}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 3:
        port = 9090
    else:
        port = int(sys.argv[2])
    if len(sys.argv) < 2:
        server_address = "0.0.0.0"
    else:
        server_address = (sys.argv[1], port)

    data_process.init()
    aof.start()
    form_writer.start()

    uvicorn.run(app, host=server_address, port=port)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
