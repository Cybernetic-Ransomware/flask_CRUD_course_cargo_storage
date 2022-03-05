from storage import db, login_manager
from storage import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False, unique=False)
    budget = db.Column(db.Integer(), nullable=False, default=5000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def form_budget(self):
        return f'{self.budget:,.0f} t'.replace(',', ' ')

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        if item_obj.price:
            return self.budget >= item_obj.price
        return True

    def can_return(self, item_obj):
        return item_obj in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=64), nullable=False, unique=True)
    availability = db.Column(db.String(length=10), nullable=True, unique=False)
    stored = db.Column(db.Integer(), nullable=False, unique=False)
    price = db.Column(db.Integer(), nullable=True, unique=False)
    comments = db.Column(db.String(length=1024), nullable=True, unique=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def possess(self, user):
        self.owner = user.id
        if self.price:
            user.budget -= self.price
        db.session.commit()

    def returning(self, user):
        self.owner = None
        if self.price:
            user.budget += self.price
        db.session.commit()
