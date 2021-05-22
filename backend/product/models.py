from backend import db


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    slug = db.Column(db.String(), unique=True, nullable=False)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.BigInteger(), primary_key=True)
    category = db.Column(db.BigInteger(), db.ForeignKey('category.id'))
    name = db.Column(db.String(), unique=True, nullable=False)
    slug = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.Unicode(), nullable=True)
    price = db.Column(db.Numeric(), nullable=False)
    image = db.Column(db.String(), nullable=True)
    thumbnail = db.Column(db.String(), nullable=True)
    date_added = db.Column(db.DateTime(), nullable=False)
