from celery import Celery
from celery.schedules import crontab
from app.repositories import OrderRepository
from app.db.db_helper import db_helper
from app.core.config import settings

from aiosmtplib import SMTP
from email.message import EmailMessage


app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

app.conf.beat_schedule = {
    'check-orders-status-every-hour': {
        'task': 'app.celery.celery_app.check_order_status',
        'schedule': crontab(minute='*/15'),
    },
}


@app.task(bind=True)
def send_email_task(self, email_to: str, subject: str, message_content: str):
    import asyncio

    async def send_email():
        # Создание сообщения
        message = EmailMessage()
        message["From"] = settings.celery.email_sender
        message["To"] = email_to
        message["Subject"] = subject
        message.set_content(message_content)

        try:
            # Асинхронное подключение и отправка через SMTP
            async with SMTP(hostname=settings.celery.smtp_hostname, port=settings.celery.smtp_port, use_tls=True) as smtp:
                await smtp.login(settings.celery.email_username, settings.celery.email_password)
                await smtp.send_message(message)
            print(f"Сообщение успешно отправлено на {email_to}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения на {email_to}: {e}")
            raise e

    # Выполнение асинхронной функции
    asyncio.run(send_email())


@app.task
def check_order_status():
    import asyncio  # Импорт внутри задачи, чтобы избежать конфликтов

    async def process():
        async for db in db_helper.session_getter():
            order_repository = OrderRepository()
            orders = await order_repository.get_orders_to_complete(db)
            for order in orders:
                if order.status == 0:
                    await send_email(
                            order.customer_car.customer.email, 
                            f"Здравствуйте, {order.customer_car.customer.first_name}! 👋",
                            f"Хотим сообщить, что выполнение вашего заказа #{order.id} немного задерживается. Мы прилагаем все усилия, чтобы завершить работу как можно быстрее.\n\nПриносим извинения за доставленные неудобства и благодарим за ваше понимание. Мы обязательно уведомим вас, как только автомобиль будет готов.\n\nСпасибо за ваше терпение! 🙏"
                        )
                    order.status = 2
            await db.commit()

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(process())


async def send_email(email: str, subject: str, body: str):
    """Асинхронная отправка письма"""
    # Создание сообщения
    message = EmailMessage()
    message["From"] = settings.celery.email_sender
    message["To"] = email
    message["Subject"] = subject
    message.set_content(body)

    try:
        # Асинхронное подключение и отправка через SMTP
        async with SMTP(hostname=settings.celery.smtp_hostname, port=settings.celery.smtp_port, use_tls=True) as smtp:
            await smtp.login(settings.celery.email_username, settings.celery.email_password)
            await smtp.send_message(message)
        print(f"Сообщение успешно отправлено на {email}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения на {email}: {e}")