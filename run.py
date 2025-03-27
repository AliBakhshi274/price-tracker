from app import app, db

with app.app_context():
    db.create_all()
    print("Database tables created (if they didn't exist yet).")

if __name__ == '__main__':
    app.run(debug=True)