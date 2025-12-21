# tests.py (замените полностью)
import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

client = TestClient(app)

def test_reserve_success():
    """✅ Успешное резервирование"""
    response = client.post(
        "/api/v1/reserve",
        json={
            "product_id": "1",
            "reservation_id": "98765",
            "quantity": 3,
            "timestamp": "2025-12-21T23:00:00"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["reservation_id"] == "98765"

def test_reserve_not_enough_stock():
    """❌ Недостаточно товара"""
    response = client.post(
        "/api/v1/reserve",
        json={
            "product_id": "1",
            "reservation_id": "98765",
            "quantity": 999,
            "timestamp": "2025-12-21T23:00:00"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "Not enough stock available."

def test_reserve_product_not_found():
    """❌ Товар не найден"""
    response = client.post(
        "/api/v1/reserve",
        json={
            "product_id": "999",
            "reservation_id": "99999",
            "quantity": 1
        }
    )
    data = response.json()
    assert data["status"] == "error"  # После вашего исправления
