from app import app, db
from models import User, Patient, Examination, Invoice, Payment
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            name='Admin',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create doctor user
        doctor = User(
            username='doctor',
            email='doctor@example.com',
            name='Doctor',
            role='doctor'
        )
        doctor.set_password('doctor123')
        db.session.add(doctor)
        
        # Commit the changes
        db.session.commit()
        print("Database initialized successfully with admin and doctor users.")

if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        print(f"Error: {str(e)}")
