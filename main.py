from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from alembic.config import Config
from alembic import command
from faker import Faker
import random

Base = declarative_base()
fake = Faker()


class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship('Student', back_populates='group')


class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.group_id'))
    group = relationship('Group', back_populates='students')
    grades = relationship('Grade', back_populates='student')


class Teacher(Base):
    __tablename__ = 'teachers'

    teacher_id = Column(Integer, primary_key=True)
    name = Column(String)
    subjects = relationship('Subject', back_populates='teacher')


class Subject(Base):
    __tablename__ = 'subjects'

    subject_id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'))
    teacher = relationship('Teacher', back_populates='subjects')
    grades = relationship('Grade', back_populates='subject')


class Grade(Base):
    __tablename__ = 'grades'

    grade_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'))
    score = Column(Integer)
    date_received = Column(Date)
    student = relationship('Student', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')


def create_tables(engine):
    Base.metadata.create_all(engine)


def generate_random_data(session, num_students, num_groups, num_subjects, num_teachers, num_grades_per_student):
    for _ in range(num_groups):
        group = Group(name=fake.word())
        session.add(group)

    for _ in range(num_teachers):
        teacher = Teacher(name=fake.name())
        session.add(teacher)

    for _ in range(num_subjects):
        subject = Subject(name=fake.word(), teacher=random.choice(session.query(Teacher).all()))
        session.add(subject)

    for _ in range(num_students):
        student = Student(name=fake.name(), group=random.choice(session.query(Group).all()))
        session.add(student)

    for _ in range(num_grades_per_student):
        grade = Grade(
            student=random.choice(session.query(Student).all()),
            subject=random.choice(session.query(Subject).all()),
            score=random.randint(50, 100),
            date_received=fake.date_this_decade()
        )
        session.add(grade)

    session.commit()


def main():
    engine = create_engine('sqlite:///my_database.db')
    create_tables(engine)

    # Create Alembic config and run migrations
    alembic_cfg = Config('alembic.ini')  # Assuming alembic.ini is properly configured
    command.upgrade(alembic_cfg, 'head')

    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed the database
    generate_random_data(session, 50, 3, 8, 5, 20)

    # Your queries and other operations go here

    session.close()


if __name__ == '__main__':
    main()
