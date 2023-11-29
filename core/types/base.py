from pydantic import BaseModel, ConfigDict

__all__ = ["Schema"]


class Schema(BaseModel):
    model_config = ConfigDict(
        ser_json_bytes="utf8",
        ser_json_timedelta="float",
        use_enum_values=True,
        allow_inf_nan=False,
        from_attributes=True
    )
