from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ----------- MODELOS -----------

class InputBiseccion(BaseModel):
    a: float
    b: float
    tol: float
    max_iter: int

class InputSecante(BaseModel):
    x0: float
    x1: float
    tol: float
    max_iter: int

# ----------- FUNCION -----------

def f(x):
    return x**3 - x - 2

# ----------- ENDPOINT INICIO (opcional pero recomendado) -----------

@app.get("/")
def inicio():
    return {"mensaje": "API de métodos numéricos funcionando correctamente"}

# ----------- METODO DE BISECCION -----------

@app.post("/biseccion")
def biseccion(data: InputBiseccion):
    a, b = data.a, data.b
    tol, max_iter = data.tol, data.max_iter

    iteraciones = []

    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        iteraciones.append({
            "iter": i + 1,
            "a": a,
            "b": b,
            "c": c,
            "f(c)": fc
        })

        if abs(fc) < tol:
            return {
                "metodo": "Biseccion",
                "datos_entrada": {
                    "a": a,
                    "b": b,
                    "tolerancia": tol,
                    "max_iter": max_iter
                },
                "resultado": c,
                "iteraciones": iteraciones,
                "mensaje": "Raíz encontrada mediante el método de bisección"
            }

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    return {
        "metodo": "Biseccion",
        "datos_entrada": {
            "a": data.a,
            "b": data.b,
            "tolerancia": tol,
            "max_iter": max_iter
        },
        "resultado": c,
        "iteraciones": iteraciones,
        "mensaje": "Máximo de iteraciones alcanzado"
    }

# ----------- METODO DE LA SECANTE -----------

@app.post("/secante")
def secante(data: InputSecante):
    x0, x1 = data.x0, data.x1
    tol, max_iter = data.tol, data.max_iter

    iteraciones = []

    for i in range(max_iter):
        if f(x1) - f(x0) == 0:
            return {
                "metodo": "Secante",
                "datos_entrada": {
                    "x0": data.x0,
                    "x1": data.x1,
                    "tolerancia": tol,
                    "max_iter": max_iter
                },
                "resultado": None,
                "iteraciones": iteraciones,
                "mensaje": "Error: división por cero"
            }

        x2 = x1 - (f(x1) * (x1 - x0)) / (f(x1) - f(x0))

        iteraciones.append({
            "iter": i + 1,
            "x": x2
        })

        if abs(x2 - x1) < tol:
            return {
                "metodo": "Secante",
                "datos_entrada": {
                    "x0": data.x0,
                    "x1": data.x1,
                    "tolerancia": tol,
                    "max_iter": max_iter
                },
                "resultado": x2,
                "iteraciones": iteraciones,
                "mensaje": "Raíz encontrada mediante el método de la secante"
            }

        x0, x1 = x1, x2

    return {
        "metodo": "Secante",
        "datos_entrada": {
            "x0": data.x0,
            "x1": data.x1,
            "tolerancia": tol,
            "max_iter": max_iter
        },
        "resultado": x2,
        "iteraciones": iteraciones,
        "mensaje": "Máximo de iteraciones alcanzado"
    }
