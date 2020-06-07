from datetime import datetime

from pytz import timezone, utc
from sqlalchemy import Column, String, Integer, DateTime, create_engine, ForeignKey, BigInteger, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Session, relationship
from sqlalchemy_utils import EncryptedType, ScalarListType

from creds import CREDS

Base = declarative_base()

engine = create_engine(CREDS['DATABASE_CONNECTION'], echo=CREDS['SQL_LOGGING'])
db_session = Session(bind=engine)


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


@auto_str
class KarmaChange(Base):
    __tablename__ = 'karma_changes'

    id = Column(Integer, primary_key=True, nullable=False)
    karma_id = Column(Integer, ForeignKey('karma.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    changed_at = Column(DateTime, nullable=False)
    reason = Column(String, nullable=True)
    change = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)

    karma = relationship('Karma', back_populates='changes')

    @hybrid_property
    def local_time(self):
        return utc.localize(self.changed_at).astimezone(timezone('Europe/London'))


@auto_str
class Karma(Base):
    __tablename__ = 'karma'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    added = Column(DateTime, nullable=False,
                   default=datetime.utcnow())
    pluses = Column(Integer, nullable=False, default=0)
    minuses = Column(Integer, nullable=False, default=0)
    neutrals = Column(Integer, nullable=False, default=0)

    changes = relationship('KarmaChange', back_populates='karma', order_by=KarmaChange.changed_at.asc())

    @hybrid_property
    def net_score(self):
        return self.pluses - self.minuses

    @hybrid_property
    def total_karma(self):
        return self.pluses + self.minuses + self.neutrals


@auto_str
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    uid = Column(BigInteger, nullable=False)
    admin = Column(Boolean,nullable=False,default=False)

@auto_str
class Command(Base):
    __tablename__ = 'command'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    name = Column(String, nullable=False)
    description = Column(String)
    command_string = Column(String,nullable=False)
    added = Column(DateTime, nullable=False,default=datetime.utcnow())
    admin = Column(Boolean,nullable=False,default=False)

@auto_str
class GymToken(Base):
    __tablename__ = 'gym_tokens'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    phpsessid = Column(String)
    csrf = Column(String)
    identity = Column(String)
    url = Column(String)

@auto_str
class GymNotification(Base):
    __tablename__ = 'gym_notifications'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    class_name = Column(String, nullable=False)
    class_time = Column(DateTime, nullable=False)
    notified = Column(Boolean,nullable=False,default=False)
