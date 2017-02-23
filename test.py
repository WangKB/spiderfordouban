from dbUtil import DBSession
from entity import Subject, Celebrity


def main():
    session = DBSession()
    subject = session.query(Subject).filter(Subject.id == 1).first()
    subject.language = '汉语'
    subject.actors.append(session.query(Celebrity).filter(Celebrity.id == 1).first())
    session.commit()
    print()

if __name__ == "__main__":
    main()
