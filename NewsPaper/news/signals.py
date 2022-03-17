from .models import Post
from django.core.mail import send_mail, mail_managers
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=Post)
def notify_managers_post(sender, instance, created, **kwargs):
    # в зависимости от того, есть ли такой объект уже в базе данных или нет, тема письма будет разная
    if created:
        subject = f'{instance.title} {instance.dateCreation.strftime("%d.%m.%Y")}'
    else:
        subject = f'Была изменена новость: {instance.title} {instance.dateCreation.strftime("%d.%m.%Y")}'

    send_mail(
        subject=subject,
        message=instance.text,
        from_email='skillfactor@yandex.ru',
        recipient_list=['kirsan0ff@yandex.ru', ]
    )


@receiver(post_delete, sender=Post)
def notify_managers_appointment_canceled(sender, instance, **kwargs):
    subject = f'{instance.title} - статья удалена!'
    mail_managers(
        subject=subject,
        message=f'Удалена статья от: {instance.dateCreation.strftime("%d.%m.%Y")}',
    )

    print(subject)