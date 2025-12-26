from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Product, Reservation
from app.db import get_db_session
from app.schemas import ReserveRequest


router = APIRouter(prefix="/api/v1",)


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
                .with_for_update()
            )
            product = result.scalar_one_or_none()

            if not product:
                return {
                    "status": "error",
                    "message": "Product not found.",
                    "reservation_id": reservation_id
                }

            if product.available_quantity < quantity:
                return {
                    "status": "error",
                    "message": "Not enough stock available.",
                    "reservation_id": reservation_id
                }

            product.available_quantity -= quantity

            reservation = Reservation(
                product_id = request.product_id,
                reservation_id = request.reservation_id,
                quantity = request.quantity,
            )
            db.add(reservation)


        return {
                "status": "success",
                "message": "Reservation completed successfully.",
                "reservation_id": reservation_id
            }

    except Exception as e:
        return {
            "status": "error",
            "message": "Not enough stock available.",
            "reservation_id": reservation_id,
            'description': str(e)
        }


@router.delete('/unreserve')
async def unreserve_product(request: ReserveRequest, db: AsyncSession = Depends(get_db_session)):
    reservation_id = request.reservation_id
    try:
        async with db.begin():
            result = await db.execute(
                select(Reservation)
                .where(Reservation.id == reservation_id)
                .with_for_update()
            )

            reservation = result.scalar_one_or_none()

            if not reservation:
                return {
                    "status": "error",
                    "message": "There is nothing to delete.",
                    "reservation_id": reservation_id
                }

            if reservation:
                await db.delete(reservation)


    except Exception as e:
        return {
            "status": "error",
            "message": "There is nothing to delete.",
            "reservation_id": reservation_id,
            'description': str(e)
        }

