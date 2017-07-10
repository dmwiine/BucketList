from instance.config import db

class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    items = db.relationship('Items', backref="Bucketlist")
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    #created_by = db.Column(db.Integer())

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        """This method saves a new bucketlist item into the database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """This method queries the database and returns all the the bucketlist items"""
        return Bucketlist.query.all()

    def delete(self):
        """This method deletes a bucketlist item from the database"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)


class Items(db.Model):
    __tablename__ = 'BucketlistItems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __init__(self, name, id):
        self.name = name
        self.bucketlist_id = id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Items {}'.format(self.name)

