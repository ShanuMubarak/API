# Placeholder for crud.py
from sqlalchemy.orm import Session
from app.models import Order, User

def get_all_orders(db: Session):
    return db.query(Order).all()

def get_user_by_id(db: Session, customer_id: str):
    return db.query(User).filter(User.customer_id == customer_id).first()

def add_order(db: Session, order_data: dict):
    order = Order(**order_data)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def add_user(db: Session, user_data: dict):
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
