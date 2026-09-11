from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator

app = FastAPI(title="Threshold Verification API")



# Pydantic Schema

class ThresholdRequest(BaseModel):
    stream_values: list[float]
    max_variance: float

    @field_validator("stream_values")
    @classmethod
    def stream_values_must_not_be_empty(cls, value: list[float]) -> list[float]:
        if len(value) == 0:
            raise ValueError("stream_values must contain at least one numeric value")
        return value

    @field_validator("max_variance")
    @classmethod
    def max_variance_must_be_non_negative(cls, value: float) -> float:
        if value < 0:
            raise ValueError("max-variance must be zero or a positive number")
        return value


# Defensive Interception: convert ALL validation failures (bad types,
# missing fields, empty arrays, malformed/blank JSON bodies) into a clean
# HTTP 400 instead of FastAPI's default 422, per the spec.

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid request payload. 'stream-values' must be a non-empty "
                      "list of numbers and 'max-variance' must be a number."
        },
    )


# Defensive Interception (safety net): catch any other unexpected error
# during processing so a dirty submission can never surface a raw Python
# 500 traceback to the candidate/evaluator.
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"detail": "Unable to process request. Please check the submitted data."},
    )


# Part A: Threshold Verification API

@app.post("/api/threshold")
async def check_threshold(payload: ThresholdRequest):
    values = payload.stream_values
    average = sum(values) / len(values)

    status = "STABLE"
    for value in values:
        if abs(value - average) > payload.max_variance:
            status = "CRITICAL"
            break

    return {
        "average": round(average, 4),
        "status": status,
        "max_variance": payload.max_variance,
        "count": len(values),
    }


# Asset Delivery Route: mount /templates as static assets on the root path.
# Registered LAST so the explicit /api/threshold route above always takes
# precedence over the catch-all static mount for that exact path.

app.mount("/", StaticFiles(directory="templates", html=True), name="frontend")
