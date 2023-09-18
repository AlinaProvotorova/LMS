import random
from faker import Faker
from apps.account.models import UserRole, User
from apps.education.models import (
    Education, Subject, Section, Lecture, GradingSystem, Grade,
    Test, Question, Answer, Schedule
)

fake = Faker()
num_users = 2  # Количество пользователей, которые нужно создать

for _ in range(num_users):
    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = fake.password()
    telephone = fake.phone_number()[:15]
    date_of_birth = fake.date_of_birth()
    role = random.choice(UserRole.objects.all())

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    user.telephone = telephone
    user.date_of_birth = date_of_birth
    user.roles.add(role)
    user.save()
num_educations = 5  # Количество программ обучения, которые нужно создать

for _ in range(num_educations):
    title = fake.word()
    description = fake.text()
    status = random.choice([Education.NOT_ACCESSIBLE, Education.IN_DEVELOPMENT, Education.FILLING, Education.ACCESS])
    date_added = fake.date()
    date_start = fake.date()
    is_online = True
    author = random.choice(User.objects.all())

    education = Education.objects.create(
        title=title,
        description=description,
        status=status,
        date_added=date_added,
        date_start=date_start,
        is_online=is_online,
        author=author
    )

    # Создание дисциплин
    num_subjects = random.randint(2, 5)  # Количество дисциплин для каждой программы обучения

    for _ in range(num_subjects):
        subject_title = fake.word()
        subject_description = fake.text()
        subject_date_added = fake.date()
        subject_studying_time = fake.date()
        subject_sequence = random.randint(1, 10)
        subject_education = education
        subject_teachers = random.sample(list(User.objects.all()), random.randint(1, 3))

        subject = Subject.objects.create(
            title=subject_title,
            description=subject_description,
            date_added=subject_date_added,
            studying_time=subject_studying_time,
            sequence=subject_sequence,
            education=subject_education
        )
        subject.teachers.set(subject_teachers)
        subject.save()

        # Создание разделов
        num_sections = random.randint(2, 5)  # Количество разделов для каждой дисциплины

        for _ in range(num_sections):
            section_title = fake.word()
            section_description = fake.text()
            section_date_added = fake.date()
            section_subject = subject

            section = Section.objects.create(
                title=section_title,
                description=section_description,
                date_added=section_date_added,
                subject=section_subject
            )

            # Создание лекций
            num_lectures = random.randint(2, 5)  # Количество лекций для каждого раздела

            for _ in range(num_lectures):
                lecture_title = fake.word()
                lecture_content = None  # Здесь добавьте логику для создания или присвоения контента лекции
                lecture_date_added = fake.date()
                lecture_section = section

                lecture = Lecture.objects.create(
                    title=lecture_title,
                    content=lecture_content,
                    date_added=lecture_date_added,
                    section=lecture_section
                )


# python manage.py shell < script.py