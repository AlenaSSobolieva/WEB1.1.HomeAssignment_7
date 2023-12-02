import unittest
from faker import Faker  # Add this line
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Group, Student, Teacher, Subject, Grade, create_tables, generate_random_data

fake = Faker()  # Initialize Faker

class TestModels(unittest.TestCase):
    def setUp(self):
        # Set up an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        create_tables(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        # Clean up the database after each test
        self.session.close()

    def test_group_model(self):
        group = Group(name='Test Group')
        self.session.add(group)
        self.session.commit()

        result = self.session.query(Group).filter_by(name='Test Group').first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'Test Group')

    def test_student_model(self):
        group = Group(name='Test Group')
        student = Student(name='Test Student', group=group)
        self.session.add(group)
        self.session.add(student)
        self.session.commit()

        result = self.session.query(Student).filter_by(name='Test Student').first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'Test Student')
        self.assertEqual(result.group.name, 'Test Group')

    def test_teacher_model(self):
        teacher = Teacher(name='Test Teacher')
        self.session.add(teacher)
        self.session.commit()

        result = self.session.query(Teacher).filter_by(name='Test Teacher').first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'Test Teacher')

    def test_subject_model(self):
        teacher = Teacher(name='Test Teacher')
        subject = Subject(name='Test Subject', teacher=teacher)
        self.session.add(teacher)
        self.session.add(subject)
        self.session.commit()

        result = self.session.query(Subject).filter_by(name='Test Subject').first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'Test Subject')
        self.assertEqual(result.teacher.name, 'Test Teacher')

    def test_grade_model(self):
        group = Group(name='Test Group')
        student = Student(name='Test Student', group=group)
        subject = Subject(name='Test Subject', teacher=Teacher(name='Test Teacher'))

        # Use fake.date_this_decade() to generate a random date
        grade = Grade(
            student=student,
            subject=subject,
            score=90,
            date_received=fake.date_this_decade()
        )

        self.session.add(group)
        self.session.add(student)
        self.session.add(subject)
        self.session.add(grade)
        self.session.commit()

        result = self.session.query(Grade).filter_by(score=90).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.score, 90)
        self.assertEqual(result.student.name, 'Test Student')
        self.assertEqual(result.subject.name, 'Test Subject')


if __name__ == '__main__':
    unittest.main()
