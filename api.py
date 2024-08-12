from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from typing import Literal
import os

app = FastAPI()

class Calculator(BaseModel):
    x: float = Field(..., description="First number")
    y: float = Field(..., description="Second number")
    operation: Literal["add", "sub", "mul", "div"] = Field(..., description="Operation to perform")

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y

def div(x, y):
    if y == 0:
        raise ValueError("Division by zero is not allowed")
    return x / y

@app.post("/calculate")
def calculate(calc: Calculator):
    try:
        if calc.operation == "add":
            result = add(calc.x, calc.y)
        elif calc.operation == "sub":
            result = sub(calc.x, calc.y)
        elif calc.operation == "mul":
            result = mul(calc.x, calc.y)
        elif calc.operation == "div":
            result = div(calc.x, calc.y)
        else:
            raise ValueError(f"Invalid operation: {calc.operation}")
        
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))