import pytest
from flask.ext.mail import Message
from sourcemash.security import delay_security_email


class TestMail:

    def test_security_mail_enqueue(self, worker, outbox):
        message = Message(subject="Welcome to Sourcemash!",
                          recipients=['user@sourcemash.com'],
                          sender="support@sourcemash.com")
        delay_security_email(message)
        worker.work(burst=True)
        assert len(outbox) == 1
        assert "Welcome to Sourcemash!" in outbox[0].subject
