import threading
from django.core.mail import send_mail
from conf.settings import EMAIL_HOST

def send_to_email_code(email, code):
    def send_in_threading():
        send_mail(
            from_email=EMAIL_HOST,
            recipient_list=[email],
            subject='Royhatni tasdiqlash',
            message=f'Your code: {code}',
        )
        
    thread = threading.Thread(target=send_in_threading)
    thread.start()
    
    
    return True