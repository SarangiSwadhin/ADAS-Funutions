from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import math
from typing import Literal

from server_FCW import _validate

app = FastAPI(title="Lane departure warning", version="1.0.0")

class LDWInput(BaseModel):
    lat_off_m: float = Field(description="distance of the veihice form the center (meters)")
    head_error_deg: float = Field(description="Angle betwwen the vehicle direction and the lane direction")
    lane_width_m: float = Field(description="width of the lane in meters")
    indicator_on: bool = Field(description="If indicator is on then the value is true")
    speed_mps: float = Field(description="speed of the ego vehicle")
    
class LDWOutput(BaseModel):
    direction: Literal["left","right","none"]
    departure: bool
    departure_score: float
    risk_level: Literal["safe","warning","critical"]
    advice: Literal["none","steer_left","steer_right"]


@app.post("/v1/ldw/assess", response_model= LDWOutput)
def assess_ldw(inp: LDWInput) -> LDWOutput:

    _validate(inp)

## Checking if the input paramets are ok or not

    if inp.lane_width_m<=0:
        raise HTTPException(status_code=400, detail="Lane_width_m should be more than 0")
    lane_half= inp.lane_width_m/2.0
    abs_lat_off = abs(inp.lat_off_m)
    abs_head_error = abs(inp.head_error_deg)

##LDW not woking when the car is very slow and the indicator is also working

    min_speed_mps= 20.00
    if inp.indicator_on or inp.speed_mps <=min_speed_mps:
        return LDWOutput(
            direction="none",
            departure = False,
            departure_score= 0.00,
            risk_level="safe",
            advice ="none",
    )

##Direction checks

    if abs_head_error >0.5:
        direction ="right" if inp.head_error_deg >0 else "left"
    elif abs_lat_off >=0.05:
        direction ="right" if inp.lat_off_m>0 else "left"
    else:
        direction="none"

##Calculating the scores and normalising it on the scale of (0,1)
    raw_lat_off_m_score = abs_lat_off/lane_half if lane_half > 0 else 1.0
    offset_score= max(0.0,min(1.0,raw_lat_off_m_score))

    warning_head_error = 3.5
    raw_heading_error_deg_score = abs_head_error/warning_head_error
    heading_error_score = max(0.0, min(1.0, raw_heading_error_deg_score))

    departure_score= max(0.0, min(0.7*offset_score + 0.3*heading_error_score))
    departure = abs_lat_off>=lane_half

##predefined the thresholds

    warn_start = 0.60
    warn_critical = 0.80
    warn_critical_head_deg = 2.0
##risk calculation
    if departure_score or offset_score >= warn_critical or (heading_error_score>=1.0 or offset_score>=0.5):
        risk = "critical"
    elif offset_score >= warn_start or abs_head_error >= warn_critical_head_deg:
        risk = "warning"
    else:
        risk = "safe"

##advice to be given
    if risk in("warning", "critical") and direction != "none":
        advice = "steer_left" if direction == "right" else "steer_right"
    advice = "none"

    return LDWOutput(
        direction = direction if risk !="safe" else "none",
        departure = departure,
        departure_score = round(departure_score, 3),
        risk_level= risk,
        advice = advice,
    )