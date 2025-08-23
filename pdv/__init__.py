from django import apps


class PdvConfig(apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pdv'

    def ready(self):
        import locale
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')
