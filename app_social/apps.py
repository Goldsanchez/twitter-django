from django.apps import AppConfig


class AppSocialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_social'

    def ready(self): #esto va junto con @receiver que es la señal
        import app_social.signals