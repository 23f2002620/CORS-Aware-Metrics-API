import os
import time
import uuid
from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware

# Assigned allowed CORS origin
ALLOWED_ORIGIN = "https://dash-l6xt5u.example.com"

# Set your logged-in email via environment variable `EMAIL` or update default below
EMAIL = "23f2002620@ds.study.iitm.ac.in"

app = FastAPI(title="Descriptive Statistics API")

# 1. CORS Middleware - Restrict to allowed origin only
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# 2. Outer HTTP Middleware - Attach X-Request-ID and X-Process-Time to EVERY response
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.perf_counter()
    request_id = str(uuid.uuid4())
    
    response = await call_next(request)
    
    process_time = time.perf_counter() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response

# Fallback OPTIONS handler for disallowed preflights
@app.options("/stats")
async def options_stats():
    return Response(status_code=200)

# GET /stats endpoint
@app.get("/stats")
async def get_stats(values: str = Query(..., description="Comma-separated integers")):
    if not values or not values.strip():
        raise HTTPException(status_code=400, detail="The 'values' query parameter cannot be empty.")

    # Split comma-separated string and filter empty values
    raw_items = [v.strip() for v in values.split(",") if v.strip()]
    if not raw_items:
        raise HTTPException(status_code=400, detail="No numbers provided.")

    # Parse integers (or float fallback if needed)
    nums = []
    for item in raw_items:
        try:
            nums.append(int(item))
        except ValueError:
            try:
                nums.append(float(item))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid integer/number: '{item}'")

    count = len(nums)
    total_sum = sum(nums)
    min_val = min(nums)
    max_val = max(nums)
    mean_val = float(total_sum) / count

    return {
        "email": EMAIL,
        "count": count,
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "mean": mean_val
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)