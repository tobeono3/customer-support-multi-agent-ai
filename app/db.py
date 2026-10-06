from datetime import date
from sqlalchemy import create_engine, String, Integer, Date, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, future=True)

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    plan: Mapped[str] = mapped_column(String(50))
    country: Mapped[str] = mapped_column(String(50))
    joined_date: Mapped[date] = mapped_column(Date)

class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, index=True)
    created_at: Mapped[date] = mapped_column(Date)
    subject: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(String(50))
    resolution: Mapped[str] = mapped_column(Text)

def init_db():
    Base.metadata.create_all(engine)

def seed_db():
    init_db()
    with Session(engine) as session:
        if session.query(Customer).count():
            return
        customers = [
            Customer(id=1, name="Ema Johnson", email="ema.johnson@example.com", plan="Pro", country="USA", joined_date=date(2024,2,12)),
            Customer(id=2, name="Liam Chen", email="liam.chen@example.com", plan="Enterprise", country="Canada", joined_date=date(2023,8,4)),
            Customer(id=3, name="Sofia Martinez", email="sofia.martinez@example.com", plan="Starter", country="USA", joined_date=date(2025,1,18)),
            Customer(id=4, name="Noah Williams", email="noah.williams@example.com", plan="Pro", country="UK", joined_date=date(2024,11,9)),
            Customer(id=5, name="Ava Patel", email="ava.patel@example.com", plan="Enterprise", country="India", joined_date=date(2022,6,30)),
        ]
        tickets = [
            Ticket(customer_id=1, created_at=date(2026,8,12), subject="Duplicate charge", status="Resolved", priority="High", resolution="Verified duplicate invoice and initiated a full refund."),
            Ticket(customer_id=1, created_at=date(2026,7,3), subject="Password reset", status="Resolved", priority="Medium", resolution="Guided customer through account recovery."),
            Ticket(customer_id=1, created_at=date(2026,5,21), subject="Export delay", status="Closed", priority="Low", resolution="Explained scheduled export window and confirmed completion."),
            Ticket(customer_id=2, created_at=date(2026,8,28), subject="SSO configuration", status="Open", priority="High", resolution="Escalated to enterprise integrations team."),
            Ticket(customer_id=3, created_at=date(2026,9,1), subject="Trial cancellation", status="Resolved", priority="Medium", resolution="Cancelled trial and confirmed no further billing."),
            Ticket(customer_id=4, created_at=date(2026,6,11), subject="Missing report", status="Closed", priority="Low", resolution="Regenerated the report and confirmed delivery."),
            Ticket(customer_id=5, created_at=date(2026,8,19), subject="API rate limit", status="Open", priority="High", resolution="Provided rate-limit documentation and opened engineering review."),
        ]
        session.add_all(customers + tickets)
        session.commit()
