# my_select.py

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload  # Add joinedload
from main import Group, Student, Teacher, Subject, Grade

def select_1(session):
    # Find the 5 students with the highest average scores in all subjects.
    result = (
        session.query(Student)
        .join(Student.grades)
        .group_by(Student)
        .order_by(func.avg(Grade.score).desc())
        .limit(5)
        .all()
    )
    return result

def select_2(session, subject_name):
    # Find a student with a high GPA in a specific subject.
    query = (
        session.query(Student)
        .join(Student.grades)
        .join(Grade.subject)  # Add the necessary join condition
        .filter(Subject.name == subject_name)
        .group_by(Student)
        .order_by(func.avg(Grade.score).desc())
    )

    print(query)  # Print the generated SQL query

    result = query.first()

    if result is not None:
        # Add print statements to check the data
        print("Subjects and scores for the student:")
        for grade in result.grades:
            print(f"Subject: {grade.subject.name}, Score: {grade.score}")
    else:
        print("No result found for the query.")

    return result


def select_3(session, group_name, subject_name):
    # Find the average score in groups in a specific subject.
    result = (
        session.query(func.avg(Grade.score).label('average_score'))
        .join(Student.grades)
        .options(joinedload(Grade.subject))  # Load the Grade and Subject relationships
        .join(Student.group)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .first()
    )

    print(result)
    return result


def select_4(session: Session, subject_name: str):
    """
    Find the average score in groups in a specific subject.
    """
    result = (
        session.query(Group.name, func.avg(Grade.score).label('average_score'))
        .join(Student, Group.group_id == Student.group_id)
        .join(Grade, Student.student_id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.subject_id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .all()
    )
    return result


def select_5(session: Session):
    """
    Find the average score on the stream (across the entire rating table).
    """
    result = session.query(func.avg(Grade.score).label('average_score')).scalar()
    return result


def select_6(session: Session, teacher_name: str):
    """
    Find what courses a specific teacher teaches.
    """
    result = (
        session.query(Subject.name)
        .join(Teacher, Subject.teacher_id == Teacher.teacher_id)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return result


def select_7(session: Session, group_name: str):
    """
    Find a list of students in a specific group.
    """
    result = (
        session.query(Student.name)
        .join(Group, Student.group_id == Group.group_id)
        .filter(Group.name == group_name)
        .all()
    )
    return result


def select_8(session: Session, group_name: str, subject_name: str):
    """
    Find the grades of students in a specific group in a specific subject.
    """
    result = (
        session.query(Student.name, Grade.score)
        .join(Group, Student.group_id == Group.group_id)
        .join(Grade, Student.student_id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.subject_id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return result


def select_9(session: Session, teacher_name: str):
    """
    Find the average grade given by a certain teacher in his subjects.
    """
    result = (
        session.query(func.avg(Grade.score).label('average_score'))
        .join(Subject, Grade.subject_id == Subject.subject_id)
        .options(joinedload(Subject.teacher))  # Load the Subject and Teacher relationships
        .join(Teacher, Subject.teacher_id == Teacher.teacher_id)
        .filter(Teacher.name == teacher_name)
        .all()
    )

    print(result)
    return result


def select_10(session: Session, student_name: str):
    """
    Find a list of courses the student is taking.
    """
    result = (
        session.query(Subject.name)
        .join(Grade, Subject.subject_id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.student_id)
        .filter(Student.name == student_name)
        .all()
    )
    return result
