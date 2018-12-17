from datetime import datetime
from app import db

participants_identifier = db.Table('participants_identifier',
    db.Column('user_id', db.String(64), db.ForeignKey('user.id')),
    db.Column('event_id', db.String(64), db.ForeignKey('event.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    avatar = db.Column(db.String(128), index=False, unique=False)
    calendar = db.relationship("Calendar", uselist=False, backref="user")
    events = db.relationship('Event', secondary=participants_identifier, backref='User')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def as_dict(self):
        return {"id": self.id, "name": self.name, "avatar": self.avatar, "calendarId": self.calendar.id }
        #return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Calendar(db.Model):
    __tablename__ = 'calendar'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'))
    events = db.relationship('Event', backref='calendar', lazy=True)

    def __repr__(self):
        return '<Event {}>'.format(self.name)

    def as_dict(self):
        events = []
        for event in self.events:
            events.append(event.as_dict())
        return {"id": self.id, "user": self.user.as_dict(), "events": events}
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    details = db.Column(db.String(1000), index=False, unique=False)
    date = db.Column(db.String(64), index=True, unique=False)
    calendar_id = db.Column(db.String(64), db.ForeignKey('calendar.id'))
    participants = db.relationship('User', secondary=participants_identifier, backref='Event')


    def __repr__(self):
        return '<Event {}>'.format(self.name)

    def participants_dict(self):
        participants = []
        for user in self.participants:
            participants.append(user.as_dict())
        return participants

    def as_dict(self):
        return {"id": self.id, "name": self.name, "details": self.details, "date": self.date}
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}

