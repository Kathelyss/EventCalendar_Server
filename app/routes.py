from app import app
from app import db

from flask import render_template
from flask import request

from app.utilities import Utilities

from app.models import User
from app.models import Calendar
from app.models import Event


import json

# USER

@app.route("/user/all")
def all_users():
    result = []
    for user in db.session.query(User).all():
        result.append(user.as_dict())
    return json.dumps(result, ensure_ascii=False)

@app.route("/user/get")
def new_user():
    name = request.args.get('name')
    instance = db.session.query(User).filter_by(name=name).first()
    if instance:
        return json.dumps(instance.as_dict(), ensure_ascii=False)

    util = Utilities()
    id = util.new_uuid()
    calendar_id = util.new_uuid()
    calendar = Calendar(id=calendar_id)
    user = User(id=id, name=name, avatar="")
    user.calendar = calendar
    db.session.add(user)
    db.session.commit()
    return json.dumps(user.as_dict(), ensure_ascii=False)

# EVENT

@app.route("/event/post")
def new_event():
    calendar_id = request.args.get('calendarId')
    calendar = db.session.query(Calendar).get(calendar_id)
    if not calendar:
        return json.dumps("", ensure_ascii=False)

    util = Utilities()
    id = util.new_uuid()
    name = request.args.get('name')
    details = request.args.get('details')
    date = request.args.get('date')
    event = Event(id=id, name=name, details=details, date=date, calendar_id=calendar.id)
    event.participants.append(calendar.user)
    calendar.events.append(event)
    db.session.add(calendar)
    db.session.commit()
    return json.dumps(event.as_dict(), ensure_ascii=False)

@app.route("/event/participants")
def event_participants():
    id = request.args.get('id')
    event = db.session.query(Event).get(id)
    if not event:
        return json.dumps("", ensure_ascii=False)

    return json.dumps(event.participants_dict(), ensure_ascii=False)

@app.route("/event/participants/add")
def event_add_participant():
    id = request.args.get('id')
    user_id = request.args.get('userId')
    event = db.session.query(Event).get(id)
    user = db.session.query(User).get(user_id)
    if not event:
        return json.dumps("", ensure_ascii=False)
    if not user:
        return json.dumps("", ensure_ascii=False)

    event.participants.append(user)
    db.session.add(event)
    db.session.commit()
    return json.dumps(event.participants_dict(), ensure_ascii=False)

@app.route("/event/participants/remove")
def event_remove_participant():
    id = request.args.get('id')
    user_id = request.args.get('userId')
    event = db.session.query(Event).get(id)
    user = db.session.query(User).get(user_id)
    if not event:
        return json.dumps("", ensure_ascii=False)
    if not user:
        return json.dumps("", ensure_ascii=False)

    index = event.participants.index(user)
    del event.participants[index]
    db.session.add(event)
    db.session.commit()
    return json.dumps(event.participants_dict(), ensure_ascii=False)


@app.route("/event/all")
def all_events():
    result = []
    for event in db.session.query(Event).all():
        result.append(event.as_dict())
    return json.dumps(result, ensure_ascii=False)

# CALENDAR

@app.route("/calendar/get")
def get_calendar():
    user_id = request.args.get('userId')

    instance = db.session.query(Calendar).filter_by(user_id=user_id).first()
    if instance:
        return json.dumps(instance.as_dict(), ensure_ascii=False)

    return json.dumps("", ensure_ascii=False)












