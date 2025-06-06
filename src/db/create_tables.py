from base import Base, engine
# from users.models import User,   # импортируйте все ваши модели

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()