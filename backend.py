from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import numpy as np
from numba import njit
import time
import subprocess
import random
import os
import math

app = FastAPI()
app.mount("/logos", StaticFiles(directory="logos"), name="logos")

# Initialize the Jinja2 template engine
templates = Jinja2Templates(directory="templates")

# Existing CORS middleware setup...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_presentation(request: Request):
    # Fixed: Explicitly defining the arguments prevents the version conflict
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"request": request}
    )


@njit
def numba_log(arr):
    s = 0.0
    for i in range(arr.size):
        arr[i] = math.log1p(arr[i])
    return arr

@njit
def numba_montecarlo(n):
    inside = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1.0:
            inside += 1
    return inside

@app.get("/benchmark/sum")
def benchmark_sum(size: int = 10_000_000):
    data_arr = np.ones(size)
    data_list = data_arr.tolist()
    
    t0 = time.time()
    [math.log1p(v) for v in data_list]
    t_py = time.time() - t0
    
    t0 = time.time()
    np.log1p(data_arr)
    t_np = time.time() - t0
    
    numba_log(data_arr) # warm-up
    t0 = time.time()
    numba_log(data_arr)
    t_nb = time.time() - t0
    
    return {"python": t_py, "numpy": t_np, "numba": t_nb, "size": size}

@app.get("/benchmark/montecarlo")
def benchmark_montecarlo(n: int = 1_000_000):
    t0 = time.time()
    inside = sum(1 for _ in range(n) if random.random()**2 + random.random()**2 <= 1.0)
    t_py = time.time() - t0
    
    t0 = time.time()
    pts = np.random.rand(n, 2)
    inside_np = np.sum(pts[:, 0]**2 + pts[:, 1]**2 <= 1.0)
    t_np = time.time() - t0
    
    numba_montecarlo(10) # warm-up
    t0 = time.time()
    numba_montecarlo(n)
    t_nb = time.time() - t0
    
    return {"python": t_py, "numpy": t_np, "numba": t_nb, "n": n}


@app.get("/benchmark/edist")
def benchmark_edist(size: int = 2000):
    durations = {}
    
    try:
        start_time = time.perf_counter()
        subprocess.run(
            ["python", "comparisons/edist.py", str(size)], 
            capture_output=True, text=True, check=True, timeout=15 
        )
        py_elapsed = time.perf_counter() - start_time
    except Exception as e:
        print(f"Python failed: {e}")
        py_elapsed = 0
    durations['py'] = py_elapsed
    
    try:
        executable = "comparisons/edist.exe" if os.name == 'nt' else "./comparisons/edist"
        start_time = time.perf_counter()
        subprocess.run(
            [executable, str(size)], 
            capture_output=True, text=True, check=True, timeout=15
        )
        cpp_elapsed = time.perf_counter() - start_time
    except Exception as e:
        print(f"C++ failed: {e}")
        cpp_elapsed = 0
    durations['cpp'] = cpp_elapsed

    try:
        ratio = py_elapsed / cpp_elapsed if cpp_elapsed > 0 else 0
    except Exception:
        ratio = 0
    durations['ratio'] = ratio

    return durations


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)