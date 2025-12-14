from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import karatsuba_vs_divide
import matplotlib.pyplot as plt
import io, base64

app = FastAPI()

# Allow frontend (localhost:3000) to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Numbers(BaseModel):
    num1: str
    num2: str

@app.post("/calculate/")
def calculate(data: Numbers):
    x = int(data.num1)
    y = int(data.num2)

    divide_res, divide_calls, divide_time = karatsuba_vs_divide.divide_and_conquer(x, y)
    kara_res, kara_calls, kara_time = karatsuba_vs_divide.karatsuba(x, y)

    return {
        "divide": {"result": divide_res, "calls": divide_calls, "time": divide_time},
        "karatsuba": {"result": kara_res, "calls": kara_calls, "time": kara_time},
    }

@app.get("/graph/{graph_type}")
def graph(graph_type: str, num1: str, num2: str):
    x = int(num1)
    y = int(num2)

    _, divide_calls, divide_time = karatsuba_vs_divide.divide_and_conquer(x, y)
    _, kara_calls, kara_time = karatsuba_vs_divide.karatsuba(x, y)

    labels = ["Divide", "Karatsuba"]

    plt.figure()

    if graph_type == "execution_time":
        plt.bar(labels, [divide_time, kara_time])
        plt.title("Execution Time (s)")
    elif graph_type == "recursive_calls":
        plt.bar(labels, [divide_calls, kara_calls])
        plt.title("Recursive Calls")
    elif graph_type == "speedup":
        plt.bar(["Speedup"], [divide_time / kara_time if kara_time > 0 else 0])
        plt.title("Speedup Factor")
    elif graph_type == "combined":
        fig, axs = plt.subplots(1, 3, figsize=(12, 4))
        axs[0].bar(labels, [divide_time, kara_time])
        axs[0].set_title("Execution Time")
        axs[1].bar(labels, [divide_calls, kara_calls])
        axs[1].set_title("Recursive Calls")
        axs[2].bar(["Speedup"], [divide_time / kara_time if kara_time > 0 else 0])
        axs[2].set_title("Speedup")
        plt.tight_layout()
    else:
        return {"error": "Invalid graph type"}

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")

    return {"image": f"data:image/png;base64,{img_base64}"}
