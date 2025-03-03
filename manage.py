from app import create_app, db
from app.models import User, Image

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database reset successfully!")

if __name__ == '__main__':
    init_db()