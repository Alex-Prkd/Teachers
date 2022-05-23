from wtforms.validators import Length, DataRequired
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, HiddenField, RadioField, SelectField, TelField, PasswordField


csrf = CSRFProtect()


class Booking(FlaskForm):
    weekday = HiddenField()
    time = HiddenField()
    teacher = HiddenField()
    client_name = StringField('Ваше имя:', [Length(min=2, max=20, message='Минимум 2 символа')])
    client_phone = TelField('Ваш номер:', [Length(min=12, message='Формат ввода: 375(XX) XXX XX XX')])


class SelectionTeacher(Booking):
    select_goal = RadioField(
        'goals',
        choices=[('travel', 'Для путешествий'), ('study', 'Для учёбы'),
                 ('work', 'Для работы'), ('relocate', 'Для переезда')]
    )
    select_time = RadioField(
        'time',
        choices=[('1-2', '1-2 часа в неделю'),
                 ('3-5', '3-5 часов в неделю'),
                 ('5-7', '5-7 часов в неделю'),
                 ('7-10', '7-10 часов в неделю')]
    )


class SelectFilter(FlaskForm):
    select_filter = SelectField(
        'select', choices=[('random', 'В случайном порядке'), ('best', 'Сначала лучшие по рейтингу'),
                           ('expensive', 'Сначала дорогие'), ('inexpensive', 'Сначала недорогие')])


class AuthUser(FlaskForm):
    username = StringField('Ваше имя: ', validators=[Length(min=2, max=12, message='От 2 до 12 символов.'),
                                                     DataRequired(message='Поле обязательное к заполнению!')
                                                     ]
                           )
    password = PasswordField('Ваша пароль: ', validators=[Length(min=8, max=32, message='От 8 до 32 символов'),
                                                          DataRequired(message='Заполнить поле!')])