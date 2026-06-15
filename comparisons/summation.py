# # Pre-initialize matrix globally to measure ONLY loop execution time
# print("Initializing 10,000 x 10,000 Python matrix (this may take a moment)...")
# MATRIX_SIZE = 10000
# print("Matrix ready!")

# @app.get("/benchmark/pythonsum")
# def benchmark_python():

#     start_time = time.perf_counter()
#     python_matrix = [[1.0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
#     total = 0
#     for row in python_matrix:
#         for val in row:
#             total += val

#     end_time = time.perf_counter()
#     duration = end_time - start_time
#     return {"duration": f"{duration:.3f}s"}


# @app.get("/benchmark/cppsum")
# def benchmark_cpp():
#     try:
#         result = subprocess.run(
#             ["./matrix_sum"], capture_output=True, text=True, check=True
#         )
#         duration_str = result.stdout.strip()  # Contains the "X.XXs" string
#         return {"duration": duration_str}
#     except Exception as e:
#         return {"duration": "Error executing C++ binary"}