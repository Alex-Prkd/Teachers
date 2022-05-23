import json
import random

from flask import render_template, request, session, redirect, url_for, abort

from example import app, db
from example.models import Teachers, Goals, Bookings, Day, Request
from example.forms import Booking, SelectionTeacher, SelectFilter, AuthUser

NAME_SITE = 'TINYSTEPS'


list_days = {
    "mon": ["Понедельник", "monday"],
    "tue": ["Вторник", "tuesday"],
    "wed": ["Среда", "wednesday"],
    "thu": ["Четверг", "thursday"],
    "fri": ["Пятница", "friday"],
    "sat": ["Суббота", "saturday"],
    "sun": ["Воскресенье", "sunday"]
}


def open_goals():
    get_goal = Goals.query.order_by(Goals.id).all()
    return get_goal


def get_teachers():
    teachers = Teachers.query.order_by(Teachers.id).all()
    return teachers


def get_teacher(id):
    teacher = Teachers.query.get_or_404(id)
    return teacher


def free_time(free_teacher):
    vacant_days = {}
    for day, time_day in free_teacher.items():
        vacant_days[list_days[day][0], day] = []
        for time, flag in time_day.items():
            if flag:
                vacant_days[list_days[day][0], day].append(time)
    return vacant_days


def check_enter(valid_data, valid_day, valid_time):
    valid_data = json.loads(valid_data)
    try:
        if valid_data[valid_day][valid_time]:
            found = True
        else:
            found = False
    except KeyError:
        found = False
    return found


@app.errorhandler(404)
def err(error):
    return render_template('error.html', error=error)


@app.route('/')
def index():
    goal = open_goals()
    teachers = get_teachers()
    return render_template('index.html',
                           goals=goal,
                           name_goal=list(goal),
                           teachers=random.sample(teachers, k=6),
                           title=f'{NAME_SITE} - Главная')


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if session.get('user'):
        redirect('/')
    form = AuthUser()
    if not form.validate_on_submit():
        return render_template('auth.html',
                               form=form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        print(username, '\t\t', password)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('user'):
        redirect('/')
    form = Register()



@app.route('/all/', methods=['POST', 'GET'])
def all_teachers():
    teachers = get_teachers()
    select = SelectFilter()
    if select.validate_on_submit():
        user_filter = select.select_filter.data
        if user_filter == 'random':
            return render_template('all.html',
                                   teachers=sorted(teachers, key=lambda k: random.random()),
                                   select=select,
                                   title=f'{NAME_SITE} - Все преподаватели')
        elif user_filter == 'best':
            teachers = Teachers.query.order_by(Teachers.rating.desc()).all()
            return render_template('all.html',
                                   teachers=teachers,
                                   select=select,
                                   title=f'{NAME_SITE} - Все преподаватели')
        elif user_filter == 'expensive':
            teachers = Teachers.query.order_by(Teachers.price.desc()).all()
            return render_template('all.html',
                                   teachers=teachers,
                                   select=select,
                                   title=f'{NAME_SITE} - Все преподаватели')
        elif user_filter == 'inexpensive':
            teachers = Teachers.query.order_by(Teachers.price).all()
            return render_template('all.html',
                                   teachers=teachers,
                                   select=select,
                                   title=f'{NAME_SITE} - Все преподаватели')
    return render_template('all.html',
                           teachers=teachers,
                           select=select,
                           title=f'{NAME_SITE} - Все преподаватели')


@app.route('/goals/<goal>/')
def goals(goal):
    goal = db.session.query(Goals).filter(Goals.key == goal).first()
    teachers_in_goal = goal.teachers
    return render_template('goal.html',
                           data_goal=goal,
                           teachers=teachers_in_goal,
                           title=f'{NAME_SITE} - {goal.value}   ')


@app.route('/profile/<int:id>/')
def profile_teacher(id):
    teacher = get_teacher(id)
    goal_teach = teacher.goals
    day_data_base = Day.query.order_by(Day.id).all()
    vacant_days = free_time(json.loads(teacher.free))
    return render_template(
        'profile.html',
        teacher=teacher,
        goals=goal_teach,
        title=f'{NAME_SITE} - {teacher.name}',
        vacant_days=vacant_days,
        day_base=day_data_base
    )


@app.route('/request/', methods=['GET', 'POST'])
def request_view():
    select_teacher = SelectionTeacher()
    form = Booking()
    if form.validate_on_submit():
        session['request'] = {
            "client_phone": select_teacher.client_phone.data,
            "client_name": select_teacher.client_name.data,
            "goal": select_teacher.select_goal.data,
            "time": select_teacher.select_time.data
        }
        request_add = Request(phone=session['request']['client_phone'][3:],
                              name=session['request']['client_name'],
                              goal_client=session['request']['goal'],
                              time=session['request']['time'])
        db.session.add(request_add)
        db.session.commit()
        return redirect(url_for('done_request'))
    else:
        return render_template('request.html',
                               select=select_teacher,
                               title=f'{NAME_SITE} - Подбор преподователя'
                               )


@app.route('/request_done/')
def done_request():
    client_goal = Goals.query.filter(Goals.key == session['request']['goal']).scalar()
    return render_template('request_done.html',
                           name=session['request']['client_name'],
                           phone=session['request']['client_phone'],
                           goal=client_goal.value,
                           time=session['request']['time'],
                           title=f'{NAME_SITE} - Заявка отправлена'
                           )


@app.route('/booking/<int:id>/<day>/<time>/', methods=['GET', 'POST'])
def booking(id, day, time):
    form = Booking()
    teacher = get_teacher(id)
    if not check_enter(teacher.free, day[:3], time + ':00'):
        abort(404)
    if form.validate_on_submit():
        session['booking'] = {
            "day": day,
            "time": form.time.data,
            "teacher_id": form.teacher.data,
            "client_phone": form.client_phone.data,
            "client_name": form.client_name.data
        }
        create_booking = Bookings(day=session['booking']['day'],
                                    time=session['booking']['time'],
                                    client_phone=session['booking']['client_phone'][3:],
                                    client_name=session['booking']['client_name'],
                                    teacher_id=teacher.id
                                  )
        db.session.add(create_booking)
        db.session.commit()
        return redirect(url_for('booking_done'))
    else:
        day_ru = Day.query.filter(Day.key_en == day).scalar()
        return render_template(
            'booking.html',
            title=f'{NAME_SITE} - Запись.',
            form=form,
            teacher=teacher,
            day=day_ru,
            time=time,
        )


@app.route('/booking_done/', methods=['POST', 'GET'])
def booking_done():
    if request.method == 'POST' or request.method == 'GET':
        day = session['booking']['day']
        return render_template('booking_done.html',
                               day=list_days[day][0],
                               time=session['booking']['time'],
                               name=session['booking']['client_name'],
                               phone=session['booking']['client_phone'],
                               title=f'{NAME_SITE} - Заявка оформлена'
                               )