from database import Base, engine
from models import Transaction


def init_db():
    Base.metadata.create_all(bind = engine)
    print("Database initialized")

if __name__ == "__main__":
    init_db()