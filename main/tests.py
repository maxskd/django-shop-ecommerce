from django.test import TestCase

from .services import EmailService


class EmailTestCase(TestCase):

    def test_send_email(self):
        self.assertEqual(EmailService.send_email('Hello', 'Hello', 'test@gmail.book'), 'Your letter has been '
                                                                                       'successfully sent!')

    def test_send_email_with_first_empty_value(self):
        self.assertEqual(EmailService.send_email('', 'Hello', 'test@gmail.book'), 'Make sure all fields are '
                                                                                  'entered and valid')

    def test_send_email_with_second_empty_value(self):
        self.assertEqual(EmailService.send_email('Hello', '', 'test@gmail.book'), 'Make sure all fields are '
                                                                                  'entered and valid')

    def test_send_email_with_third_empty_value(self):
        self.assertEqual(EmailService.send_email('Hello', 'Hello', ''), 'Make sure all fields are '
                                                                        'entered and valid')
    # def test_send_email_with_new_line(self):
    # self.assertEqual(EmailService.send_email('/n/n\n\n/n', 'Hello', 'test@gmail.book', 'Invalid header found')
