from sqlalchemy import Boolean
from sqlalchemy import Column, String, Integer, Float, Table
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

actor_subject = Table('actor_subject', Base.metadata,
                      Column('a_id', ForeignKey('celebrity.id'), primary_key=True),
                      Column('s_id', ForeignKey('subject.id'), primary_key=True)
                      )

director_subject = Table('director_subject', Base.metadata,
                         Column('d_id', ForeignKey('celebrity.id'), primary_key=True),
                         Column('s_id', ForeignKey('subject.id'), primary_key=True)
                         )

screenwriter_subject = Table('screenwriter_subject', Base.metadata,
                             Column('sw_id', ForeignKey('celebrity.id'), primary_key=True),
                             Column('s_id', ForeignKey('subject.id'), primary_key=True)
                             )


class Subject(Base):

    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    title = Column(String(2000))
    type = Column(String(255))
    product_nation = Column(String(255))
    language = Column(String(255))
    premiere = Column(String(2000))
    duration = Column(Float)
    rating_num = Column(Float)
    rating_people = Column(Integer)
    periods = Column(Integer)
    period_duration = Column(Float)
    photo = Column(String(2000))
    year = Column(String(255))

    actors = relationship('Celebrity', secondary=actor_subject, back_populates='starred', lazy='subquery')
    directors = relationship('Celebrity', secondary=director_subject, back_populates='directed', lazy='subquery')
    screenwriters = relationship('Celebrity', secondary=screenwriter_subject, back_populates='wrote', lazy='subquery')

    def __repr__(self):
        return '(Subject: %d, %s)' % (self.id, self.title)


class Celebrity(Base):

    __tablename__ = 'celebrity'

    id = Column(Integer, primary_key=True)
    zodiac = Column(String(255))
    birthday = Column(String(255))
    birthplace = Column(String(255))
    profession = Column(String(255))
    for_lang_names = Column(String(2000))
    name = Column(String(2000))
    photo = Column(String(2000))
    gender = Column(String(255))

    starred = relationship('Subject', secondary=actor_subject, back_populates='actors', lazy='subquery')
    directed = relationship('Subject', secondary=director_subject, back_populates='directors', lazy='subquery')
    wrote = relationship('Subject', secondary=screenwriter_subject, back_populates='screenwriters', lazy='subquery')

    def __repr__(self):
        return '(Celebrity: %d, %s)' % (self.id, self.name)


class YearTag(Base):

    __tablename__ = 'year_tag'

    id = Column(Integer, primary_key=True)
    year = Column(String(255))
    page = Column(Integer)
    isScanned = Column(Boolean)

    def __repr__(self):
        return '(YearTag: %d, %s)' % (self.id, self.year)


class Task(Base):

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    url = Column(String(2000))
    isScanned = Column(Boolean)

    def __repr__(self):
        return '(Task: %d, %s)' % (self.id, self.url)


class Proxy(Base):

    __tablename__ = 'proxy'

    id = Column(Integer, primary_key=True)
    ip = Column(String(255))
    port = Column(String(255))
    status = Column(String(255))

    def __repr__(self):
        return '(Proxy: %d, %s)' % (self.id, self.ip)
