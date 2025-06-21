from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

def send_verification_email(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verify_url = request.build_absolute_uri(
        reverse('accounts:email-verify', kwargs={'uidb64': uidb64, 'token': token})
    )

    subject = 'تأیید ایمیل شما در بلیتو ✉️'
    from_email = None
    to_email = [user.email]

    html_message = render_to_string('emails/verify_email.html', {
        'user': user,
        'verify_url': verify_url,
    })

    message = EmailMultiAlternatives(subject, '', from_email, to_email)
    message.attach_alternative(html_message, "text/html")
    message.send()
