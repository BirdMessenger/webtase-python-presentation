# Python Speed-Up Options for Scientific Computing

This project is a modular, interactive presentation built with Reveal.js and FastAPI. It benchmarks standard Python performance against vectorized NumPy code and compiled Numba routines, visualizing hardware-level bottlenecks like the Global Interpreter Lock (GIL) and memory management.

## Project Architecture

- **Backend:** FastAPI (serves the frontend and runs the benchmark logic).
- **Frontend:** Reveal.js (the slide engine) with Tailwind CSS for styling.
- **Templating:** Jinja2 (allows for modular slide management).

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/BirdMessenger/webtase-python-presentation.git
cd webtase-python-presentatio
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Compile the C++ Benchmark
Before starting the server, ensure the C++ backend is compiled:
```bash
g++ comparisons/edist.cpp -o comparisons/edist
```

### 5. Running the Presentation
Start the FastAPI server:
```python
uvicorn backend:app --reload
```

Once running, open your browser and navigate to:
http://127.0.0.1:8000/

## Contributing

To add a new slide:
1. Create a new .html file in templates/slides/.
2. Include the new file in templates/index.html using the {% include %} directive.
3. Restart the server and refresh your browser.
