from app import create_app, db

application = create_app()

# Initialize database
with application.app_context():
    db.create_all()

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=10000)
