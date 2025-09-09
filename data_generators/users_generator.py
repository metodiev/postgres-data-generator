# data_generators/users_generator.py
import uuid
from datetime import datetime
from faker import Faker

fake = Faker()

class UsersGenerator:
    """Generates DB-safe rows for 'users' table."""
    
    MAX_LENGTHS = {
        "phone_number": 20,
        "username": 150,
        "email": 255,
        "user_type": 50,
        "auth_provider": 50,
        "timezone": 50,
        "language": 10,
    }

    USER_TYPES = ["customer", "admin", "vendor", "staff"]
    GENDERS = ["male", "female", "other"]
    AUTH_PROVIDERS = ["local", "google", "facebook", "github"]

    def generate(self):
        row = {
            "id": str(uuid.uuid4()),
            "email": fake.email()[:self.MAX_LENGTHS["email"]],
            "username": fake.user_name()[:self.MAX_LENGTHS["username"]],
            "password_hash": fake.sha256(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone_number": fake.phone_number()[:self.MAX_LENGTHS["phone_number"]],
            "date_of_birth": fake.date_of_birth(),
            "gender": fake.random_element(self.GENDERS),
            "profile_picture": fake.image_url(),
            "user_type": fake.random_element(self.USER_TYPES),
            "is_active": fake.boolean(),
            "is_email_verified": fake.boolean(),
            "last_login_at": fake.date_time_this_year(),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "deleted_at": None,
            "auth_provider": fake.random_element(self.AUTH_PROVIDERS)[:self.MAX_LENGTHS["auth_provider"]],
            "role_id": None,
            "timezone": fake.timezone()[:self.MAX_LENGTHS["timezone"]],
            "language": fake.language_code()[:self.MAX_LENGTHS["language"]],
        }
        return row
