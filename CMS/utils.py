import xhtml2pdf.pisa as pisa

from django.http import HttpResponse
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
            contracts = contracts.filter(electric_utility=utility, gas_utility=utility)
    elif commodity_type == 'Electric':
        contracts = contracts.filter(electric='Yes', commodity_gas='No')
        if price_type != 'All':
            contracts = contracts.filter(electric_price_type=price_type)
        if utility != 'All':
            contracts = contracts.filter(electric_utility=utility)
    elif commodity_type == 'Gas':
        contracts = contracts.filter(electric='No', commodity_gas='Yes')
        if price_type != 'All':
            contracts = contracts.filter(gas_price_plan=price_type)
        if utility != 'All':
            contracts = contracts.filter(gas_utility=utility)
    if term != 'All':
        contracts = contracts.filter(agreement_length=int(term))
    if account_type != 'All':
        contracts = contracts.filter(account_type=account_type)
    if customer_type != 'All':
        cust_type = ApplicationMasterTypes.object.get(type='Customer Type', name=customer_type)
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
