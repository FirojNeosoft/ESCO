from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Survey(models.Model):
    """
    Survey model
    """
    survey_completed_by = models.ForeignKey(User, related_name='survey', blank=False, null=False, on_delete=models.CASCADE)
    agreement_date = models.DateField('Agreement Date', blank=False, null=False)
    account_type = models.CharField(max_length=16, choices=settings.ACCOUNT_TYPE, blank=False, null=False, default='New Customer')
    customer_description = models.TextField(null=True, blank=True)
    customer_first_name = models.CharField('Customer First Name', max_length=512, blank=False, null=False)
    customer_last_name = models.CharField('Customer Last Name', max_length=512, blank=False, null=False)
    service_address_line1 = models.CharField(max_length=128, blank=True, null=True)
    service_address_line2 = models.CharField(max_length=128, blank=True, null=True)
    service_address_city = models.CharField(max_length=128, blank=False, null=False)
    service_address_state = models.CharField(max_length=128, blank=False, null=False)
    service_address_country = models.CharField(max_length=128, blank=False, null=False)
    service_address_zip_code = models.PositiveIntegerField('Zip Code', blank=False, null=False)
    billing_address_line1 = models.CharField(max_length=128, blank=True, null=True)
    billing_address_line2 = models.CharField(max_length=128, blank=True, null=True)
    billing_address_city = models.CharField(max_length=128, blank=False, null=False)
    billing_address_state = models.CharField(max_length=128, blank=False, null=False)
    billing_address_country = models.CharField(max_length=128, blank=False, null=False)
    billing_address_zip_code = models.PositiveIntegerField('Zip Code', blank=False, null=False)
    customer_phone = models.CharField('Customer Phone', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format:'+999999999'. Up to 15 digits allowed.")], max_length=15,\
        unique=True, blank=False, null=False)
    customer_email = models.EmailField('Customer Email', blank=False, null=False, unique=True)
    sbc = models.CharField('SBC', max_length=16, choices=settings.SBC, blank=False, null=False, default='Option1')
    salesperson_first_name = models.CharField('Salesparson/Broker First Name', max_length=512, blank=False, null=False)
    salesperson_last_name = models.CharField('Salesparson/Broker Last Name', max_length=512, blank=False, null=False)
    door_to_door = models.CharField('Door To Door', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='Yes')
    customer_type = models.CharField('Customer Type', max_length=32, choices=settings.CUSTOMER_TYPE, blank=False, \
                                     null=False, default='Commercial')
    billing = models.CharField('Billing', max_length=16, choices=settings.BILLING, blank=False, null=False, default='POR')
    utility_description = models.TextField(null=True, blank=True)
    passthru = models.CharField('Passthru(s)', max_length=8, choices=settings.PASSTHRU, blank=False, null=False,
                               default='GRT')
    rate_class = models.CharField('Rate Class', max_length=8, choices=settings.RATE_CLASS, blank=False, null=False,
                               default='OPTION1')
    gas_rate_class = models.CharField('Gas Rate Class', max_length=8, choices=settings.RATE_CLASS, blank=False, null=False,
                               default='OPTION1')
    utility_pool = models.DecimalField('Utility Pool(%)', max_digits=10, decimal_places=2, default=0)
    electric_utility = models.CharField('Utility/LDC - Electric', max_length=16, choices=settings.ELECTRIC_UTILITY, \
                                        blank=False, null=False, default='ConEdison')
    gas_utility = models.CharField('Utility/LDC - Gas', max_length=16, choices=settings.GAS_UTILITY, blank=False, null=False,
                               default='ConEdison')
    utility_account_type = models.CharField('Account Type', max_length=8, choices=settings.UTILITY_ACCOUNT_TYPE,\
                                            blank=False, null=False, default='OPTION1')
    utility_account_nos = models.CharField('Utility Account #s', max_length=1024, blank=True, null=True)
    gas_description = models.TextField(null=True, blank=True)
    commodity_gas = models.CharField('Commodity Gas', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='Yes')
    delivery_type = models.CharField('Delivery Type', max_length=16, choices=settings.DELIVERY_TYPE, blank=False,\
                                    null=False, default='Firm')
    gas_price_plan = models.CharField('Price Plan- Gas', max_length=8, choices=settings.PRICE_PLAN, blank=False,\
                                    null=False, default='Fixed')
    electric_description = models.TextField(null=True, blank=True)
    electric = models.CharField('Electric', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='Yes')
    green = models.CharField('100% Green', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='Yes')
    Zone = models.CharField('Zone', max_length=64, choices=settings.ZONE, blank=False,\
                                    null=False, default='NYISO Zone A through K')
    electric_price_type = models.CharField('Electric Price Type', max_length=8, choices=settings.PRICE_PLAN, blank=False,\
                                    null=False, default='Fixed')
    billing_description = models.TextField(null=True, blank=True)
    therm = models.CharField('Therm', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='Yes')
    tax_exempt = models.CharField('Tax Exempt', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='Yes')
    monthly_budget = models.CharField('Monthly Budget', max_length=3, choices=settings.BINARY_CHOICES, blank=False,\
                                    null=False, default='Yes')
    budget_amount = models.DecimalField('Budget Amount', max_digits=10, decimal_places=2, default=0)
    electric_bandwidth_usage = models.CharField('Bandwidth Usage- Electric', max_length=512, blank=False, null=False)
    gas_bandwidth_usage = models.CharField('Bandwidth Usage- Gas', max_length=512, blank=False, null=False)
    electric_fixed_rate = models.DecimalField('Electric Fixed Rate $/kWh', max_digits=10, decimal_places=2, default=0)
    electric_index_rate = models.DecimalField('Electric Index Rate $/kWh', max_digits=10, decimal_places=2, default=0)
    gas_fixed_rate = models.DecimalField('Gas Fixed Rate $/kWh', max_digits=10, decimal_places=2, default=0)
    gas_index_rate = models.DecimalField('Gas Index Rate $/kWh', max_digits=10, decimal_places=2, default=0)
    agreement_length = models.PositiveIntegerField('Length of Agreement (in months)', blank=False, null=False, default=0)
    contract_start_date = models.DateField('Contractual Start Date', blank=False, null=False)
    deal_description = models.TextField(null=True, blank=True)
    internal_data_available = models.CharField('Internal Data Available', max_length=3, choices=settings.BINARY_CHOICES,\
                                               blank=False, null=False, default='Yes')
    utility_service_class = models.CharField('Utility Service Class', max_length=512, blank=False, null=False)
    broker_margin = models.DecimalField('Broker Margin $/kWh', max_digits=10, decimal_places=2, default=0)
    usage_from_date = models.DateField('Usage From Date', blank=False, null=False)
    usage_to_date = models.DateField('Usage To Date', blank=False, null=False)
    base_icap = models.CharField('Base ICAP', max_length=512, blank=False, null=False)
    base_trans_tag = models.CharField('Base Trans tag (E)', max_length=512, blank=False, null=False)
    base = models.CharField('Base (G)', max_length=512, blank=False, null=False)
    slope = models.CharField('Slope (G)', max_length=512, blank=False, null=False)
    term_volume = models.DecimalField('Term Volume (monthly average volume x term length)', max_digits=10,\
                                      decimal_places=2, default=0)
    utilized_term_net_margin = models.DecimalField('Unitized Term Net Margin', max_digits=10, decimal_places=2, default=0)
    salesperson_or_team = models.CharField('Salesperson/Team', max_length=512, blank=True, null=True)
    energy_deal_component = models.CharField('Deal Components- Energy', max_length=512, blank=True, null=True)
    capacity_deal_component = models.CharField('Deal Components- Capacity', max_length=512, blank=True, null=True)
    line_looses_deal_component = models.CharField('Deal Components- Line Looses', max_length=512, blank=True, null=True)
    rec_or_zec = models.CharField('REC/ZEC', max_length=512, blank=True, null=True)
    srec = models.CharField('SREC', max_length=512, blank=True, null=True)
    nits = models.CharField('NITS', max_length=512, blank=True, null=True)
    taxes = models.DecimalField('Taxes', max_digits=10, decimal_places=2, default=0)
    swing_rate = models.DecimalField('Swing Rate', max_digits=10, decimal_places=2, default=0)
    hedge_type = models.CharField('Hedge Type', max_length=512, blank=True, null=True)
    hedge_product_volume = models.PositiveIntegerField('Hedge Product Volume', blank=False, null=False, default=0)
    hedge_price = models.DecimalField('Hedge Price', max_digits=10, decimal_places=2, default=0)
    estimated_annual_hedge_volume = models.PositiveIntegerField('Est. Annual equivalent hedged volume', blank=False,\
                                                                null=False, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s' % (self.customer_full_name)

    @property
    def customer_full_name(self):
        return '%s %s' % (self.customer_first_name, self.customer_last_name)

    @property
    def salesperson_full_name(self):
        return '%s %s' % (self.salesperson_first_name, self.salesperson_last_name)


