import poplib
import re
import time

class MailHelper:

    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject, max_attempts=10, wait=3):
        for attempt in range(max_attempts):
            try:
                pop = poplib.POP3(self.app.config['james']['host'])
                pop.user(username)
                pop.pass_(password)
                num_messages = pop.stat()[0]
                if num_messages > 0:
                    for n in range(num_messages):
                        msglines = pop.retr(n + 1)[1]
                        msgtext = b"\n".join(msglines).decode(errors="ignore")  # игнорируем бинарные символы
                        if subject in msgtext:
                            pop.dele(n + 1)
                            pop.quit()
                            return msgtext
                pop.quit()
            except Exception as e:
                print(f"Ошибка при чтении почты: {e}")
            time.sleep(wait)
        return None

    @staticmethod
    def extract_confirmation_url(text):
        if not text:
            return None
        match = re.search(r"http://\S+", text)
        return match.group(0) if match else None
