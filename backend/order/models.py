from backend import db


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.BigInteger(), primary_key=True)
    user = db.Column(db.BigInteger(), db.ForeignKey('users.id'))
    first_name = db.Column(db.Unicode(length=20))
    last_name = db.Column(db.Unicode(length=20))
    email = db.Column(db.String(length=50))
    address = db.Column(db.Unicode(length=100))
    zipcode = db.Column(db.String(length=10))
    place = db.Column(db.String())
    phone = db.Column(db.String())
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)
    paid_amount = db.Column(db.Numeric(), nullable=False)
    stripe_token = db.Column(db.String(length=100))


class OrderItem(db.Model):
    __tablename__ = "orderitem"

    id = db.Column(db.BigInteger(), primary_key=True)
    order = db.Column(db.BigInteger(), db.ForeignKey('order.id'))
    product = db.Column(db.BigInteger(), db.ForeignKey('product.id'))
    price = db.Column(db.Numeric(), nullable=False)
    quantity = db.Column(db.Integer(), server_default="1")



