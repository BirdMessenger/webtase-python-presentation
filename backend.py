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
    
    return {"python": t_py, "numpy": t_np, "numba": t_nb, "size": size, "ratio": t_py/t_np}

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


def mandelbrot_np(c, max_iter):
    output = np.zeros(c.shape, dtype=int)
    z = np.zeros_like(c)
    mask = np.ones(c.shape, dtype=bool)

    for i in range(max_iter):
        z[mask] = z[mask]**2 + c[mask]
        escaped = np.abs(z) > 2.0
        
        # Update output for newly escaped pixels
        new_escaped = escaped & mask
        output[new_escaped] = i
        mask[new_escaped] = False 
        
    output[mask] = max_iter
    return output


@njit(fastmath=True)
def mandelbrot_nb(c, max_iter):
    rows, cols = c.shape
    output = np.zeros(c.shape, dtype=np.int32)
    
    for i in range(rows):
        for j in range(cols):
            z = 0.0j
            c_val = c[i, j]
            for k in range(max_iter):
                z = z*z + c_val
                # Early stop! This is what makes Numba so much faster here.
                if z.real**2 + z.imag**2 > 4.0: 
                    output[i, j] = k
                    break
            else:
                output[i, j] = max_iter
                
    return output


@app.get("/benchmark/heateq")
def benchmark_mandelbrot(size: int = 1500, max_iter: int = 200):
    # Setup the complex plane grid
    y, x = np.ogrid[-1.4:1.4:size*1j, -2.0:0.8:size*1j]
    c = x + y*1j

    # NumPy
    t0 = time.time()
    mandelbrot_np(c, max_iter)
    t_np = time.time() - t0

    # Numba
    mandelbrot_nb(c[:10, :10], max_iter) # Warm-up compilation
    
    t0 = time.time()
    mandelbrot_nb(c, max_iter)
    t_nb = time.time() - t0

    return {"numpy": t_np, "numba": t_nb, "size": size, "max_iter": max_iter, "ratio": t_np/t_nb}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)