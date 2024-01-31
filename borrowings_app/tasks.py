from celery import shared_task
from datetime import datetime, timedelta
from borrowings_app.models import Borrowing
from django.conf import settings

from telegram_helper import TelegramHelper


@shared_task
def notify_overdue_borrowings():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=tomorrow,
        actual_return_date__isnull=True,
    )

    bot = TelegramHelper(
        token=settings.TELEGRAM_BOT_TOKEN, chat_id=settings.TELEGRAM_CHAT_ID
    )

    if overdue_borrowings.exists():
        for borrowing in overdue_borrowings:
            message = (
                f"Borrowing Overdue:\n"
                f"User: {borrowing.user.username}\n"
                f"Book: {borrowing.book.title}\n"
                f"Expected Return Date: {borrowing.expected_return_date}"
            )
            bot.send_message(text=message)
    else:
        bot.send_message(
            text="No overdue borrowings today!"
        )
