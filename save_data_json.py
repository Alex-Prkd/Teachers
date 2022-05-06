import json

from main import db, Teachers, Day, Goals
from data import teachers, goals

list_days = {
    "mon": ["Понедельник", "monday"],
    "tue": ["Вторник", "tuesday"],
    "wed": ["Среда", "wednesday"],
    "thu": ["Четверг", "thursday"],
    "fri": ["Пятница", "friday"],
    "sat": ["Суббота", "saturday"],
    "sun": ["Воскресенье", "sunday"]
}


icons = {
    "travel": "⛱",
    "study": "🏫",
    "work": "🏢",
    "relocate": "🚜"
}

for key, value in list_days.items():
    day = Day(
        key_en=key,
        value_en=value[1],
        value_ru=value[0]
    )
    db.session.add(day)


for key_req, value_req in goals.items():
    goal = Goals(
        key=key_req,
        value=value_req,
        icon=icons.get(key_req)
    )
    db.session.add(goal)


for teacher_info in teachers:
    teacher_rec = Teachers(
        name=teacher_info['name'],
        about=teacher_info['about'],
        rating=teacher_info['rating'],
        picture=teacher_info['picture'],
        price=teacher_info['price'],
        free=teacher_info['free']
    )
    for goal in teacher_info['goals']:
        goal_rec = Goals.query.filter(Goals.key == goal).first()
        teacher_rec.goals.append(goal_rec)
    db.session.add(teacher_rec)
db.session.commit()



