from miband4_database import db

class Miband4(db.Model):
    __tablename__ = 'miband4_devices'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    serial = db.Column(db.String(12), unique=True)
    software_revision = db.Column(db.String(10))
    hardware_revision = db.Column(db.String(10))
    mac_address = db.Column(db.String(17), nullable=False)
    auth_key = db.Column(db.String(32), nullable=False)
    last_fetch_data_timestamp = db.Column(db.DateTime(timezone=True))
    activities_records = db.relationship('ActivityRecord', backref='band', lazy=True)
    
    def __repr__(self):
        return f"Band('{self.serial}')"
    
    def serialize(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'serial': self.serial, 
            'software_revision': self.software_revision,
            'hardware_revision': self.hardware_revision,
            'mac_address':self.mac_address,
            'auth_key' : self.auth_key
        }


class ActivityRecord(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey(Miband4.id), nullable=False, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, primary_key=True)
    category = db.Column(db.Integer)
    intensity = db.Column(db.Integer)
    steps = db.Column(db.Integer)
    heartrate = db.Column(db.Integer)
    
    def __repr__(self):
        return f"Data('{self.timestamp}, '{self.category}','{self.steps}', '{self.heartrate}')"
    
    def serialize(self):
        return {
            'band_id': self.band_id,
            'timestamp': self.timestamp,
            'category': self.category,
            'intensity': self.intensity,
            'steps' : self.steps,
            'heartrate' : self.heartrate
        }