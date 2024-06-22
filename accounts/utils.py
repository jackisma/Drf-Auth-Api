from django.core.mail import EmailMessage
import os 


# We are going to define a class that contains a method that 
# will send an email from the specific email we defined in our project root settings file 
# with the body and subject fields .
class Util:
    @staticmethod
    def email_sender(data):
        email = EmailMessage(subject=data['subject'],body=data['body'],from_email=os.environ.get('EMAIL_USER'),
                             to=[data['to_email']])
        
        email.send()

# we import and use this class above in our serializer file .
