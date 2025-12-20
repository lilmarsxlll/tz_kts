from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Product, Reservation
from app.db import get_db_session



router = APIRouter(prefix="/api/v1/reserve",)


class ReserveRequest(BaseModel):
    product_id: str
    quantity: int


@router.post("/reserve")
async def reserve_product(request: ReserveRequest, db: AsyncSession = Depends(get_db_session)):
    product_id = request.product_id
    reservation_id = request.reservation_id
    quantity = request.quantity
    try:
        async with db.begin():
            result = await db.execute(
                select(Product)
                .where(Product.id == product_id)
            )
            product = result.scalar_one_or_none()


            if product.available_quantity < quantity:
                return {
                    "status": "error",
                    "message": "Not enough stock available.",
                    "reservation_id": reservation_id
                }

            product.available_quantity -= quantity

            reservation = Reservation(
                product_id = request.product_id,
                quantity = request.quantity,
            )
            db.add(reservation)
            await db.commit()

        return {
                "status": "success",
                "message": "Reservation completed successfully.",
                "reservation_id": reservation_id
            }

    except Exception as e:
        return {
            "status": "error",
            "message": "Not enough stock available.",
            "reservation_id": "98765"
        }






