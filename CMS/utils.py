import datetime
import xhtml2pdf.pisa as pisa

from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template

from CMS.models import *

from io import BytesIO


def get_contracts(commodity_type='All', price_type='All', term='All', utility='All', account_type='All', customer_type='All'):
    contracts = Survey.objects.all()
    if commodity_type == 'All':
        contracts = contracts.filter(electric='Yes', commodity_gas='Yes')
        if price_type != 'All':
            contracts = contracts.filter(electric_price_type=price_type, gas_price_plan=price_type)
        if utility != 'All':
            contracts = contracts.filter(electric_utility__name=utility, gas_utility__name=utility)
    elif commodity_type == 'Electric':
        contracts = contracts.filter(electric='Yes', commodity_gas='No')
        if price_type != 'All':
            contracts = contracts.filter(electric_price_type=price_type)
        if utility != 'All':
            contracts = contracts.filter(electric_utility__name=utility)
    elif commodity_type == 'Gas':
        contracts = contracts.filter(electric='No', commodity_gas='Yes')
        if price_type != 'All':
            contracts = contracts.filter(gas_price_plan=price_type)
        if utility != 'All':
            contracts = contracts.filter(gas_utility__name=utility)
    if term != 'All':
        contracts = contracts.filter(agreement_length=int(term))
    if account_type != 'All':
        contracts = contracts.filter(account_type=account_type)
    if customer_type != 'All':
        cust_type = ApplicationMasterTypes.objects.get(type='Customer Type', name=customer_type)
        contracts = contracts.filter(customer_type=cust_type)
    return contracts


class Render:

    @staticmethod
    def pdf_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(response.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)


def get_utility_types():
    electric_utility_types = ApplicationMasterTypes.objects.filter(type='Electric Utility Type').exclude(status='Delete')
    utility_types = [('All', 'All'),]
    for utility in electric_utility_types:
        utility_types.append((utility.name, utility.name))
    return utility_types

def get_customer_types():
    cust_types = ApplicationMasterTypes.objects.filter(type='Customer Type').exclude(status='Delete')
    customer_types = [('All', 'All'),]
    for cust_type in cust_types:
        customer_types.append((cust_type.name, cust_type.name))
    return customer_types

def get_customers_count(customer_type):
    cust_type = ApplicationMasterTypes.objects.get(type='Customer Type', name=customer_type)
    customers_count = []
    customers_count.append(
        Survey.objects.filter(contract_start_date__year = datetime.date.today().year, customer_type = cust_type).count())
    customers_count.append(
        Survey.objects.filter(contract_start_date__year=datetime.date.today().year-1, customer_type=cust_type).count())
    customers_count.append(
        Survey.objects.filter(contract_start_date__year=datetime.date.today().year-2, customer_type=cust_type).count())
    return customers_count


def get_account_types_data(request):
    year = request.GET.get('year', datetime.date.today().year)
    yr_total_contracts = Survey.objects.filter(contract_start_date__year=int(year)).count()
    new_customers = Survey.objects.filter(contract_start_date__year=int(year), account_type='New Customer').count()
    renew_customers = Survey.objects.filter(contract_start_date__year=int(year), account_type='Renewal').count()
    if yr_total_contracts > 0:
        new_y = (new_customers / yr_total_contracts) * 100
        renew_y = (renew_customers / yr_total_contracts) * 100
    else:
        new_y=0
        renew_y=0
    account_types_data = {"result": [{
        'name': 'New Customer',
        'y': new_y,
        'sliced': 'true',
        'selected': 'true'
    }, {
        'name': 'Renewal',
        'y': renew_y
    }]}
    return JsonResponse(account_types_data)
