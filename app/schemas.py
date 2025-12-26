from datetime import datetime
from pydantic import BaseModel


class ReserveRequest(BaseModel):
    product_id: str
    reservation_id: str
    quantity: int
    timestamp: datetime