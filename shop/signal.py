from shop import models
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received


def payment_notification(sender, **kwargs):
    inp_obj = sender
    if inp_obj.payment_status == ST_PP_COMPLETED:
        order_id = inp_obj.invoice.split('-')[-1]
        order = models.Order.objects.get(id=order_id)
        order.paid = True
        order.save()

    valid_ipn_received.connect(payment_notification())
