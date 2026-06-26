from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
import re

class CargoIntakeSchema(BaseModel):
    cargo_description: str = Field(..., description="The description of items being transported.")
    weight_lbs: float = Field(..., description="Total cargo weight in pounds.")
    usdot_number: str = Field(..., description="7-digit USDOT number formatting (e.g., DOT-1234567 or USDOT1234567).")
    pickup_date: date = Field(..., description="The planned execution window date (YYYY-MM-DD).")
    origin_city: str = Field(..., description="City and State of origin.")
    destination_city: str = Field(..., description="City and State of delivery.")

    @field_validator('weight_lbs')
    @classmethod
    def validate_weight_limits(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Cargo weight must be greater than 0 lbs.")
        if value > 45000:
            raise ValueError("Overweight violation: Standard semi-truck payloads cannot exceed 45,000 lbs.")
        return value

    @field_validator('usdot_number')
    @classmethod
    def validate_usdot_format(cls, value: str) -> str:
        # Standard cleaning to handle messy text extraction variations
        cleaned = "".join(value.split()).upper()
        # Enforces variations of DOT1234567 or USDOT1234567 (7 digits digits strictly required)
        pattern = r"^(USDOT|DOT)?\d{7}$"
        if not re.match(pattern, cleaned):
            raise ValueError("Invalid USDOT standard: Must contain exactly 7 numeric tracking digits.")
        return cleaned

    @field_validator('pickup_date')
    @classmethod
    def validate_future_horizon(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("Scheduling violation: Pickup timelines cannot reside in past horizons[cite: 21, 29].")
        return value