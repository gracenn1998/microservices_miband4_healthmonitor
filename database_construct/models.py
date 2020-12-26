from database_construct import db

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'user_api'}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hashed = db.Column(db.LargeBinary, nullable=False)
    password_salt = db.Column(db.LargeBinary, nullable=False)
    fullname = db.Column(db.String(120))
    activities_records = db.relationship('Miband', backref='user', cascade="save-update, merge, refresh-expire, expunge", lazy=True)
    activities_records = db.relationship('ActivityRecord', backref='user', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"User('{self.id}')"

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'password_hashed': str(self.password_hashed),
            'password_salt': str(self.password_salt),
            'fullname': self.fullname,
        }   

class Miband4(db.Model):
    __tablename__ = 'miband4_devices'
    __table_args__ = {'schema': 'miband_api'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_api.users.id'))
    serial = db.Column(db.String(12), unique=True)
    software_revision = db.Column(db.String(10))
    hardware_revision = db.Column(db.String(10))
    mac_address = db.Column(db.String(17), nullable=False)
    auth_key = db.Column(db.String(32), nullable=False)
    last_fetch_data_timestamp = db.Column(db.DateTime(timezone=True))
    activities_records = db.relationship('ActivityRecord', backref='band', cascade="all", lazy=True)
    
    def __repr__(self):
        return f"Band('{self.serial}')"
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'serial': self.serial, 
            'software_revision': self.software_revision,
            'hardware_revision': self.hardware_revision,
            'mac_address':self.mac_address,
            'auth_key' : self.auth_key
        }


class ActivityRecord(db.Model):
    __tablename__ = 'activity_records'
    __table_args__ = {'schema': 'miband_api'}
    # id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey(Miband4.id), primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)
    category = db.Column(db.Integer)
    intensity = db.Column(db.Integer)
    steps = db.Column(db.Integer)
    heartrate = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user_api.users.id'), primary_key=True)
    
    def __repr__(self):
        return f"Data('{self.timestamp}, '{self.category}','{self.steps}', '{self.heartrate}')"
    
    def serialize(self):
        return {
            'band_id': self.band_id,
            'user_id': self.user_id,
            'timestamp': self.timestamp,
            'category': self.category,
            'intensity': self.intensity,
            'steps' : self.steps,
            'heartrate' : self.heartrate
        }