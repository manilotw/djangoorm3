from datacenter.models import Mark, Schoolkid, Chastisement, Commendation, Lesson
import random


def get_schoolkid(kid):
    try:
        return Schoolkid.objects.get(full_name__contains=kid)
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем '{kid}' не найден.")
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем '{kid}'.")
    return None


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


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

    child = get_schoolkid(kid)
    if not child:
        return

    lessons = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title__contains=schoolsubject
    ).order_by('-date')

    lesson = random.choice(lessons)

    if not lesson:
        print(f"Урок по предмету '{schoolsubject}' не найден.")
        return

    Commendation.objects.create(
        text=random.choice(commendation_texts),
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher
    )

    print(f"Похвала для ученика {child.full_name} успешно создана!")
