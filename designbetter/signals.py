from allauth.account.models import EmailAddress
from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.dispatch import receiver

@receiver(social_account_added)
@receiver(social_account_updated)
def activate_user_on_social_login(request, sociallogin, **kwargs):


    user = sociallogin.user
    user.is_active = True
    user.save()

    # Marca el email como verificado
    email = user.correo_electronico
    EmailAddress.objects.update_or_create(
        user=user,
        email=email,
        defaults={'verified': True, 'primary': True}
    )
    

