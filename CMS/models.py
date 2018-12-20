from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator


class Survey(models.Model):
    """
    Survey model
    """
    survey_completed_by = models.CharField('Survey Completed By', max_length=512, blank=False, null=False)
    agreement_date = models.DateField('Agreement Date', blank=False, null=False)
    account_type = models.CharField(max_length=16, choices=settings.ACCOUNT_TYPE, blank=False, null=False, default='New Customer')
    customer_name = models.CharField('Customer Name', max_length=512, blank=False, null=False)
    completed_by = models.CharField('Completed By', max_length=512, blank=False, null=False)
    service_address = models.CharField('Service Address', max_length=1024, blank=True, null=True)
    billing_address = models.CharField('Billing Address', max_length=1024, blank=True, null=True)
    customer_phone = models.CharField('Customer Phone', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format:'+999999999'. Up to 15 digits allowed.")], max_length=15,\
        unique=True, blank=False, null=False)
    customer_email = models.EmailField('Customer Email', blank=False, null=False, unique=True)
    sbc = models.CharField('SBC', max_length=16, choices=settings.SBC, blank=False, null=False, default='Option1')
    salesperson_name = models.CharField('Salesparson/Broker Name', max_length=512, blank=False, null=False)
    door_to_door = models.BooleanField('Door to door', default=False)
    customer_type = models.CharField('Customer Type', max_length=32, choices=settings.CUSTOMER_TYPE, blank=False, null=False, \
                                     default='Commercial')
    billing = models.CharField('Billing', max_length=16, choices=settings.BILLING, blank=False, null=False, default='POR')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s' % (self.customer_name)
