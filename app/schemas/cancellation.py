from pydantic import BaseModel


class CancellationSchema(BaseModel):
    fund_id: str
