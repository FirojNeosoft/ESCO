from django.db import models
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
    created_by = models.ForeignKey(User, blank=True, related_name='type_created_by', null=True,
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


class Survey(models.Model):
    """
    Survey model
    """
    survey_completed_by = models.ForeignKey(User, related_name='survey', blank=True, null=True, on_delete=models.SET_NULL)
    agreement_date = models.DateField('Agreement Date', blank=True, null=True)
    account_type = models.CharField(max_length=16, choices=settings.ACCOUNT_TYPE, blank=False, null=False, default='New Customer')
    customer_description = models.TextField(null=True, blank=True)
    customer_name = models.CharField('Customer Name', max_length=512, blank=False, null=False)
    service_address_line1 = models.CharField(max_length=128, blank=True, null=True)
    service_address_line2 = models.CharField(max_length=128, blank=True, null=True)
    service_address_city = models.CharField(max_length=128, blank=False, null=False)
    service_address_state = models.CharField(max_length=128, blank=False, null=False)
    # service_address_country = models.CharField(max_length=128, blank=False, null=False)
    service_address_zip_code = models.PositiveIntegerField('Zip Code', blank=True, null=True)
    billing_address_line1 = models.CharField(max_length=128, blank=True, null=True)
    billing_address_line2 = models.CharField(max_length=128, blank=True, null=True)
    billing_address_city = models.CharField(max_length=128, blank=False, null=False)
    billing_address_state = models.CharField(max_length=128, blank=False, null=False)
    # billing_address_country = models.CharField(max_length=128, blank=False, null=False)
    billing_address_zip_code = models.PositiveIntegerField('Zip Code', blank=True, null=True)
    customer_phone = models.CharField('Customer Phone', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format:'+999999999'. Up to 15 digits allowed.")], max_length=15,\
        blank=True, null=True)
    customer_email = models.EmailField('Customer Email', blank=True, null=True)
    sbc = models.CharField('SBC', max_length=16, choices=settings.SBC, blank=True, null=True)
    salesperson_name = models.CharField('Salesperson/Broker Name', max_length=512, blank=False, null=False)
    door_to_door = models.CharField('Door To Door', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='No')
    customer_type = models.ForeignKey(ApplicationMasterTypes, limit_choices_to={'type': 'Customer Type', 'status':'Active'},\
                                      related_name='contract_cust_type', blank=False, null=False, default='Residential',\
                                                                                          on_delete=models.SET_DEFAULT)
    billing = models.CharField('Billing', max_length=16, choices=settings.BILLING, blank=False, null=False, default='POR')
    utility_description = models.TextField(null=True, blank=True)
    passthru = models.ManyToManyField(ApplicationMasterTypes, limit_choices_to={'type': 'Passthru', 'status':'Active'},\
                                      related_name='contract_passthru', default='Not listed')
    rate_class = models.CharField('Rate Class', max_length=8, blank=True, null=True)
    gas_rate_class = models.CharField('Gas Rate Class', max_length=8, blank=True, null=True)
    utility_pool = models.DecimalField('Utility Pool(%)', max_digits=10, decimal_places=2, default=0)
    electric_utility = models.ForeignKey(ApplicationMasterTypes, limit_choices_to={'type': 'Electric Utility Type', 'status':'Active'},
                      related_name='contract_electric_utility', blank=False, null=False, default='ConEdison',\
                                         on_delete=models.SET_DEFAULT)

    gas_utility = models.ForeignKey(ApplicationMasterTypes, limit_choices_to={'type': 'Gas Utility Type', 'status':'Active'},
                      related_name='contract_gas_utility', blank=False, null=False, default='ConEdison',\
                                         on_delete=models.SET_DEFAULT)
    utility_account_type = models.CharField('Account Type', max_length=8, blank=True, null=True)
    utility_account_nos = models.CharField('Utility Account #s', max_length=1024, blank=True, null=True)
    gas_description = models.TextField(null=True, blank=True)
    commodity_gas = models.CharField('Commodity Gas', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='No')
    delivery_type = models.ForeignKey(ApplicationMasterTypes, limit_choices_to={'type': 'Delivery Type', 'status':'Active'},
                      related_name='contract_delivery_type', blank=True, null=True, on_delete=models.SET_NULL)
    gas_price_plan = models.CharField('Price Plan- Gas', max_length=8, choices=settings.PRICE_PLAN, blank=True,\
                                    null=True)
    electric_description = models.TextField(null=True, blank=True)
    electric = models.CharField('Electric', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='No')
    green = models.CharField('100% Green', max_length=3, choices=settings.BINARY_CHOICES, blank=True,\
                                    null=True)
    zone = models.ManyToManyField(ApplicationMasterTypes, limit_choices_to={'type': 'Zone', 'status':'Active'},\
                                      related_name='contract_zone', default='Not listed')
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
    # document = models.FileField('Document', upload_to='upload_docs/', null=True, blank=True)
    # deal_description = models.TextField(null=True, blank=True)
    # internal_data_available = models.CharField('Internal Data Available', max_length=3, choices=settings.BINARY_CHOICES,\
    #                                            blank=False, null=False, default='Yes')
    # utility_service_class = models.CharField('Utility Service Class', max_length=512, blank=False, null=False)
    # broker_margin = models.DecimalField('Broker Margin $/kWh', max_digits=10, decimal_places=2, default=0)
    # usage_from_date = models.DateField('Usage From Date', blank=False, null=False)
    # usage_to_date = models.DateField('Usage To Date', blank=False, null=False)
    # base_icap = models.CharField('Base ICAP', max_length=512, blank=False, null=False)
    # base_trans_tag = models.CharField('Base Trans tag (E)', max_length=512, blank=False, null=False)
    # base = models.CharField('Base (G)', max_length=512, blank=False, null=False)
    # slope = models.CharField('Slope (G)', max_length=512, blank=False, null=False)
    # term_volume = models.DecimalField('Term Volume (monthly average volume x term length)', max_digits=10,\
    #                                   decimal_places=2, default=0)
    # utilized_term_net_margin = models.DecimalField('Unitized Term Net Margin', max_digits=10, decimal_places=2, default=0)
    # salesperson_or_team = models.CharField('Salesperson/Team', max_length=512, blank=True, null=True)
    # energy_deal_component = models.CharField('Deal Components- Energy', max_length=512, blank=True, null=True)
    # capacity_deal_component = models.CharField('Deal Components- Capacity', max_length=512, blank=True, null=True)
    # line_looses_deal_component = models.CharField('Deal Components- Line Looses', max_length=512, blank=True, null=True)
    # rec_or_zec = models.CharField('REC/ZEC', max_length=512, blank=True, null=True)
    # srec = models.CharField('SREC', max_length=512, blank=True, null=True)
    # nits = models.CharField('NITS', max_length=512, blank=True, null=True)
    # taxes = models.DecimalField('Taxes', max_digits=10, decimal_places=2, default=0)
    # swing_rate = models.DecimalField('Swing Rate', max_digits=10, decimal_places=2, default=0)
    # hedge_type = models.CharField('Hedge Type', max_length=512, blank=True, null=True)
    # hedge_product_volume = models.PositiveIntegerField('Hedge Product Volume', blank=False, null=False, default=0)
    # hedge_price = models.DecimalField('Hedge Price', max_digits=10, decimal_places=2, default=0)
    # estimated_annual_hedge_volume = models.PositiveIntegerField('Est. Annual equivalent hedged volume', blank=False,\
    #                                                             null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, related_name='survey_created_by', null=True,
                                   on_delete=models.SET_NULL)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, related_name='survey_modified_by', null=True,
                                on_delete=models.SET_NULL)

    def __str__(self):
        return '%s' % (self.customer_name)


class Doc(models.Model):
    survey = models.ForeignKey('Survey', related_name='survey_doc', blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    document = models.FileField('Document', upload_to='upload_docs/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

