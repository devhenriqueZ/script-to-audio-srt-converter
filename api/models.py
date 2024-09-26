from pydantic import BaseModel, UUID4, validator
from typing import Literal

class TTSRequest(BaseModel):
    task_uuid: UUID4
    title: str
    body: str
    language: str
    gender: Literal["Male", "Female"]
    rate: str
    volume: float

    @validator('rate')
    def validate_rate(cls, v):
        if v.endswith('%'):
            return v
        try:
            rate_float = float(v)
            return f"{(rate_float - 1) * 100:+.0f}%"
        except ValueError:
            raise ValueError("Rate must be either a decimal number or a percentage")

    @validator('volume')
    def validate_volume(cls, v):
        if 0 <= v <= 100:
            return f"+{v:.0f}%"
        else:
            raise ValueError("Volume must be between 0 and 100")