from sqlalchemy import Column, String, Integer, DateTime, Float, Table
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
    premiere = Column(DateTime(timezone=False))
    duration = Column(Float)
    rating_num = Column(Float)
    rating_people = Column(Integer)
    periods = Column(Integer)
    period_duration = Column(Float)

    actors = relationship('Celebrity', secondary=actor_subject, back_populates='starred', lazy='subquery')
    directors = relationship('Celebrity', secondary=director_subject, back_populates='directed', lazy='subquery')
    screenwriters = relationship('Celebrity', secondary=screenwriter_subject, back_populates='wrote', lazy='subquery')


class Celebrity(Base):

    __tablename__ = 'celebrity'

    id = Column(Integer, primary_key=True)
    zodiac = Column(String(255))
    birthday = Column(DateTime(timezone=False))
    birthplace = Column(String(255))
    profession = Column(String(255))
    for_lang_names = Column(String(2000))
    name = Column(String(2000))

    starred = relationship('Subject', secondary=actor_subject, back_populates='actors', lazy='subquery')
    directed = relationship('Subject', secondary=director_subject, back_populates='directors', lazy='subquery')
    wrote = relationship('Subject', secondary=screenwriter_subject, back_populates='screenwriters', lazy='subquery')
