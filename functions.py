from datacenter.models import *
import random


def fix_marks(schoolkid):
    schoolkid = Mark.objects.get(schoolkid=schoolkid)
    for point in schoolkid:
        point.points = 5
        point.save()


def remove_chastisements(schoolkid):
    Chastisement.objects.get(schoolkid=schoolkid).delete()


def create_commendation(kid, schoolsubject):
    commendation_texts = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!'
    ]

    commendation = random.choice(commendation_texts)

    lesson = Lesson.objects.filter(
        year_of_study=6,
        group_letter__contains='А',
        subject__title__contains=schoolsubject
    ).first()

    if not lesson:
        print(f"Урок по предмету '{schoolsubject}' не найден.")
        return

    try:
        child = Schoolkid.objects.get(full_name__contains=kid)
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем '{kid}' не найден.")
        return
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем '{kid}'.")
        return

    Commendation.objects.create(
        text=commendation,
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher
    )

    print(f"Похвала для ученика {child.full_name} успешно создана!")
