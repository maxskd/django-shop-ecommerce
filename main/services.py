from django.core.mail import BadHeaderError, send_mail


class EmailService:

    @staticmethod
    def send_email(subject, message, email_sender):
        email_recipient = ['test@book.test']
        if subject and message and email_sender:
            try:
                # In real project pass should be removed, and send_mail package should be added
                # send_mail(subject, message, email_sender, email_recipient)
                pass
            except BadHeaderError:
                return 'Invalid header found'
            return 'Your letter has been successfully sent!'
        else:
            return 'Make sure all fields are entered and valid'
