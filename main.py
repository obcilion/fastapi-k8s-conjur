from fastapi import FastAPI
from contextlib import asynccontextmanager
import psutil

# Super simple service so we have something to do.

@asynccontextmanager
async def lifespan(_: FastAPI):
    print("Starting server")
    yield
    print("Stopping server")

app = FastAPI(lifespan=lifespan)

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}"

@app.get("/healthz")
async def healthz():
    return "OK"

@app.get("/")
async def root():
    # get information about the environment we're running on

    logical_cpus = psutil.cpu_count(logical=True)
    physical_cpus = psutil.cpu_count(logical=False)
    mem = psutil.virtual_memory()
    io = psutil.disk_io_counters()

    return {
        "logical_cpus": logical_cpus,
        "physical_cpus": physical_cpus,
        "mem": {
            "total": format_bytes(mem.total),
            "available": format_bytes(mem.available),
            "used": format_bytes(mem.used),
            "free": format_bytes(mem.free),
            "percent": mem.percent,
        },
        "io": {
            "read_count": io.read_count,
            "write_count": io.write_count,
            "read_bytes": format_bytes(io.read_bytes),
            "write_bytes": format_bytes(io.write_bytes),
        },
    }
