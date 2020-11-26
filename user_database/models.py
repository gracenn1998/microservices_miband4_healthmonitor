from user_database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hashed = db.Column(db.LargeBinary, nullable=False)
    password_salt = db.Column(db.LargeBinary, nullable=False)
    fullname = db.Column(db.String(120))
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String(1))

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.password}')"

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'password_hashed': str(self.password_hashed),
            'password_salt': str(self.password_salt),
            'fullname': self.fullname,
            'dob': self.dob,
            'gender': self.gender
        }
