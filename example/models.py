from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON


db = SQLAlchemy()


goals_teachers_associations = db.Table('goals_associations',
                                       db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')),
                                       db.Column('goal_id', db.Integer, db.ForeignKey('goal.id'))
                                       )


class Teachers(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    goals = db.relationship('Goals',
                            secondary=goals_teachers_associations,
                            back_populates='teachers',
                            )
    free = db.Column(JSON)
    bookings = db.relationship('Bookings', back_populates='teacher')


class Goals(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    icon = db.Column(db.String, nullable=False)
    teachers = db.relationship('Teachers',
                               secondary=goals_teachers_associations,
                               back_populates='goals',
                               order_by=Teachers.price.desc()
                               )


class Bookings(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    client_phone = db.Column(db.String)
    client_name = db.Column(db.String, nullable=False)
    teacher_id = db.Column(db.Integer,
                           db.ForeignKey('teacher.id')
                           )

    teacher = db.relationship('Teachers',
                              back_populates='bookings'
                              )


class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    goal_client = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)


class Day(db.Model):
    __tablename__ = 'day'
    id = db.Column(db.Integer, primary_key=True)
    key_en = db.Column(db.String, nullable=False)
    value_en = db.Column(db.String, nullable=False)
    value_ru = db.Column(db.String, nullable=False)


class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
