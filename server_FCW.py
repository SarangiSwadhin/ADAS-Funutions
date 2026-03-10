from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from math import inf
from typing import Literal

app = FastAPI(title="Forward collision warning", version="1.0.0")

# ---------- Public Schemas (Input/Output Contracts) ----------
class FCWInput(BaseModel):
    distance_m: float = Field(gt=0, description="Distance to lead object (meters)")
    rel_speed_mps: float = Field(description="Closing speed (m/s); + means approaching")
    host_speed_mps: float = Field(ge=0, description="Ego vehicle speed (m/s)")

class FCWOutput(BaseModel):
    ttc_s: float | None  # None when not approaching
    threat_level: Literal["safe", "warning", "critical"]
    advice: Literal["none", "prepare_to_brake", "brake_now"]

# ---------- Public Endpoint ----------
@app.post("/v1/fcw/assess", response_model=FCWOutput)
def assess_fcw(inp: FCWInput) -> FCWOutput:
    """
    Assess forward collision risk from gap distance and relative speed.
    rel_speed_mps > 0 means we are closing the gap.
    """
    _validate(inp)  # policy/range guardrails

    ttc = _compute_ttc(inp.distance_m, inp.rel_speed_mps)
    threat, advice = _assess_threat(ttc, inp.host_speed_mps)

    return FCWOutput(
        ttc_s=None if ttc == inf else round(ttc, 3),
        threat_level=threat,
        advice=advice
    )

# ---------- Hidden Internals (Black-Box Logic) ----------
def _validate(inp: FCWInput) -> None:
    """
    Extra sanity/policy checks beyond schema validation.
    Raise HTTP 400 for client mistakes (clean error surface).
    """
    if inp.distance_m > 1000:
        raise HTTPException(status_code=400, detail="distance_m too large for FCW context")
    if abs(inp.rel_speed_mps) > 120:
        raise HTTPException(status_code=400, detail="rel_speed_mps out of expected bounds")
    if inp.host_speed_mps > 90:  # ~324 km/h
        raise HTTPException(status_code=400, detail="host_speed_mps out of expected bounds")

def _compute_ttc(distance_m: float, closing_mps: float) -> float:
    """
    TTC (Time-To-Collision) in seconds.
    TTC = distance / closing_speed when approaching (closing_mps > 0).
    If not approaching (closing_mps <= 0), return infinity (no collision).
    """
    return distance_m / closing_mps if closing_mps > 0 else inf

def _assess_threat(ttc_s: float, host_speed_mps: float) -> tuple[str, str]:
    """
    Map TTC to discrete threat levels and driver advice.
      - critical if TTC < 1.0 s
      - warning  if 1.0 <= TTC < 3.0 s
      - safe     otherwise (or not approaching)
    """
    if ttc_s == inf:
        return "safe", "none"

    critical_thr = 1.0  # seconds
    warning_thr = 3.0   # seconds

    if ttc_s < critical_thr:
        return "critical", "brake_now"
    elif ttc_s < warning_thr:
        return "warning", "prepare_to_brake"
    else:
        return "safe", "none"