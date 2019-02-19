from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserVerification(models.Model):
    user = models.ForeignKey(User, related_name='user_verification', blank=False, null=False, on_delete=models.CASCADE)
    otp = models.PositiveIntegerField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ApplicationMasterTypes(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    type = models.CharField(max_length=128, choices=settings.MASTER_TYPES, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, blank=False, related_name='type_created_by', null=True,
                                   on_delete=models.SET_NULL)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, related_name='type_modified_by', null=True,
                                on_delete=models.SET_NULL)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.name

    class meta:
        unique_together = ('name', 'type',)

    def delete(self):
        """
        Delete employee
        """
        self.status = 'Delete'
        self.save()


class Customer(models.Model):
    """
    Customer
    """
    name = models.CharField('Customer Name', max_length=512, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, blank=False, related_name='customer_created_by', null=True,
                                   on_delete=models.SET_NULL)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, related_name='customer_managed_by', null=True,
                                on_delete=models.SET_NULL)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')

    def __str__(self):
        return '%s' % (self.name)

    def delete(self):
        """
        Delete employee
        """
        self.status = 'Delete'
        self.save()


class Survey(models.Model):
    """
    Survey model
    """
    survey_completed_by = models.ForeignKey(User, related_name='survey', blank=True, null=True, on_delete=models.SET_NULL)
    agreement_date = models.DateField('Agreement Date', blank=True, null=True)
    account_type = models.CharField(max_length=16, choices=settings.ACCOUNT_TYPE, blank=False, null=False, default='New Customer')
    customer_description = models.TextField(null=True, blank=True)
    customer = models.ForeignKey(Customer, related_name='survey_customer', blank=False, null=True, on_delete=models.SET_NULL,\
                                 limit_choices_to=Q(status='Active') | Q(status='Inactive'))
    service_address_line1 = models.CharField(max_length=128, blank=True, null=True)
    service_address_line2 = models.CharField(max_length=128, blank=True, null=True)
    service_address_city = models.CharField(max_length=128, blank=False, null=False)
    service_address_state = models.CharField(max_length=128, blank=False, null=False)
    service_address_zip_code = models.PositiveIntegerField('Zip Code', blank=True, null=True)
    billing_address_line1 = models.CharField(max_length=128, blank=True, null=True)
    billing_address_line2 = models.CharField(max_length=128, blank=True, null=True)
    billing_address_city = models.CharField(max_length=128, blank=False, null=False)
    billing_address_state = models.CharField(max_length=128, blank=False, null=False)
    billing_address_zip_code = models.PositiveIntegerField('Zip Code', blank=True, null=True)
    customer_phone = models.CharField('Customer Phone', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format:'+999999999'. Up to 15 digits allowed.")], max_length=15,\
        blank=True, null=True)
    customer_email = models.EmailField('Customer Email', blank=True, null=True)
    sbc = models.CharField('SBC', max_length=16, blank=True, null=True)
    salesperson_name = models.CharField('Salesperson/Broker Name', max_length=512, blank=False, null=False)
    door_to_door = models.CharField('Door To Door', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='No')
    customer_type = models.ForeignKey(ApplicationMasterTypes, related_name='contract_cust_type',\
                                    limit_choices_to= Q(type='Customer Type') & Q(status='Active') | Q(status='Inactive'), \
                                    blank=False, null=False, default=1, on_delete=models.SET_DEFAULT)
    billing = models.CharField('Billing', max_length=16, choices=settings.BILLING, blank=False, null=False, default='POR')
    billing_method = models.CharField('Billing Method', max_length=8, choices=settings.BILLING_METHOD, blank=False, null=False,\
                                       default='Mail')
    billing_contact = models.CharField('Billing Contact', max_length=64, blank=True, null=True)
    utility_description = models.TextField(null=True, blank=True)
    passthru = models.ManyToManyField(ApplicationMasterTypes, related_name='contract_passthru', default=1,\
                                      limit_choices_to=Q(type='Passthru') & Q(status='Active') | Q(status='Inactive'))
    electric_rate_class = models.ForeignKey(ApplicationMasterTypes, related_name='contract_electrict_rate_class', \
                                   limit_choices_to=Q(type='Electric Rate Class') & Q(status='Active') | Q(status='Inactive'),\
                                    blank=False, null=True, on_delete=models.SET_NULL)
    gas_rate_class = models.ForeignKey(ApplicationMasterTypes, related_name='contract_gas_rate_class', \
                                   limit_choices_to=Q(type='Gas Rate Class') & Q(status='Active') | Q(status='Inactive'),\
                                    blank=False, null=True, on_delete=models.SET_NULL)
    utility_pool = models.DecimalField('Utility Pool(%)', max_digits=10, decimal_places=2, default=0)
    electric_utility = models.ForeignKey(ApplicationMasterTypes, related_name='contract_electric_utility',\
                            limit_choices_to=Q(type='Electric Utility Type') & Q(status='Active') | Q(status='Inactive'),\
                            blank=False, null=False, default=1, on_delete=models.SET_DEFAULT)

    gas_utility = models.ForeignKey(ApplicationMasterTypes, related_name='contract_gas_utility',\
                        limit_choices_to=Q(type='Gas Utility Type') & Q(status='Active') | Q(status='Inactive'),\
                        blank=False, null=False, default=1,on_delete=models.SET_DEFAULT)
    utility_account_type = models.CharField('Account Type', max_length=8, blank=True, null=True)
    utility_account_nos = models.CharField('Utility Account #s', max_length=1024, blank=True, null=True)
    gas_description = models.TextField(null=True, blank=True)
    commodity_gas = models.CharField('Commodity Gas', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='No')
    delivery_type = models.ForeignKey(ApplicationMasterTypes, related_name='contract_delivery_type',\
                                      limit_choices_to=Q(type='Delivery Type') & Q(status='Active') | Q(status='Inactive'),\
                                      blank=True, null=True, on_delete=models.SET_NULL)
    gas_price_plan = models.CharField('Price Plan- Gas', max_length=8, choices=settings.PRICE_PLAN, blank=True,\
                                    null=True)
    electric_description = models.TextField(null=True, blank=True)
    electric = models.CharField('Electric', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='No')
    green = models.CharField('100% Green', max_length=3, choices=settings.BINARY_CHOICES, blank=True,\
                                    null=True)
    zone = models.ManyToManyField(ApplicationMasterTypes, related_name='contract_zone', default=1,\
                                  limit_choices_to=Q(type='Zone') & Q(status='Active') | Q(status='Inactive'))
    electric_price_type = models.CharField('Electric Price Type', max_length=8, choices=settings.PRICE_PLAN, blank=True,\
                                    null=True)
    billing_description = models.TextField(null=True, blank=True)
    therm = models.CharField('Therm', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='No')
    tax_exempt = models.CharField('Tax Exempt', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='No')
    monthly_budget = models.CharField('Monthly Budget', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='No')
    budget_amount = models.DecimalField('Budget Amount', max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    electric_bandwidth_usage = models.DecimalField('Bandwidth Usage- Electric(%)', max_digits=10, decimal_places=2, default=0)
    gas_bandwidth_usage = models.DecimalField('Bandwidth Usage- Gas(%)', max_digits=10, decimal_places=2, default=0)
    electric_fixed_rate = models.DecimalField('Electric Fixed Rate $/kWh', max_digits=10, decimal_places=6, blank=True,\
                                    null=True)
    electric_index_rate = models.DecimalField('Electric Index Rate $/kWh', max_digits=10, decimal_places=6, blank=True,\
                                    null=True)
    gas_fixed_rate = models.DecimalField('Gas Fixed Rate $/kWh', max_digits=10, decimal_places=6, blank=True,\
                                    null=True)
    gas_index_rate = models.DecimalField('Gas Index Rate $/kWh', max_digits=10, decimal_places=6, blank=True,\
                                    null=True)
    agreement_length = models.PositiveIntegerField('Length of Agreement (in months)', blank=True, null=True)
    contract_start_date = models.DateField('Contractual Start Date', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, related_name='survey_created_by', null=True,
                                   on_delete=models.SET_NULL)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, related_name='survey_modified_by', null=True,
                                on_delete=models.SET_NULL)

    def __str__(self):
        return '%s' % (self.customer.name)


class Doc(models.Model):
    survey = models.ForeignKey('Survey', related_name='survey_doc', blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    document = models.FileField('Document', upload_to='upload_docs/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
