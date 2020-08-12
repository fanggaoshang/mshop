from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'shop'
    verbose_name = 'Shop'

    def ready(self):
        import shop.signal