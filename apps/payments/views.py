from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from payments.asaas.asaas_payment import AsaasInvoice
from payments.asaas.payments_dataclasses import Billing, CreditCard, creditCardHolderInfo
from payments.asaas.payment_enum import BillingType
from datetime import date, timedelta
from django.http import HttpResponse, Http404
from .models import CreditCards
from .forms import CheckoutCreditCard
from django.contrib import messages
from django.contrib.messages import constants

class Step1(View):
    template_name = 'step1.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        value = float(request.POST.get('value').replace('R$', '').replace('.', '').replace(',', '.'))
        billing_type = request.POST.get('billing_type')

        asaas = AsaasInvoice()
        due_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        billing = Billing(request.user.customer_id, billing_type, value, due_date)
        response = asaas.create_invoice(billing)

        return redirect(reverse('step2', kwargs={'invoice_id': response['id']}))
    
class Step2(View):
    template_name = 'step2.html'
    def get(self, request, invoice_id):
        asaas = AsaasInvoice()
        invoice = asaas.get_invoice(invoice_id)

        if invoice['customer'] != request.user.customer_id:
            raise Http404()
        
        pix_data = None
        if invoice['billingType'] == BillingType.PIX.value:
            pix_data = asaas.get_pix_invoice(invoice_id)
            print(pix_data)

        credit_cards = None
        if invoice['billingType'] == BillingType.CREDIT_CARD.value:
            credit_cards = CreditCards.objects.filter(user=request.user)

        form = CheckoutCreditCard()

        return render(request, self.template_name, {'pix_data': pix_data, 'invoice': invoice, 'credit_cards': credit_cards, 'form': form})
    
    def post(self, request, invoice_id):
        asaas = AsaasInvoice()
        invoice = asaas.get_invoice(invoice_id)

        if invoice['customer'] != request.user.customer_id:
            raise Http404()
        
        if credit_card_token := request.POST.get('credit_card_token'):
            card = CreditCards.objects.get(credit_card_token=credit_card_token)
            
            if card.user != request.user:
                raise Http404()
            
            response = asaas.pay_invoice(invoice_id, None, None, credit_card_token)
        else:
            form = CheckoutCreditCard(request.POST)

            if form.is_valid():
                expiration_month, expiration_year = form.cleaned_data['expiration_date'].split('/')
                credit_card = CreditCard(
                    form.cleaned_data['holder_name'],
                    form.cleaned_data['card_number'],
                    expiration_month,
                    expiration_year,
                    form.cleaned_data['cvc']
                )
                holder_info = creditCardHolderInfo(
                    request.user.first_name,
                    request.user.email,
                    request.user.cpf_cnpj,
                    form.cleaned_data['postal_code'],
                    form.cleaned_data['house_number'],
                    form.cleaned_data['phone'],
                )

                response = asaas.pay_invoice(invoice_id, credit_card, holder_info)
                
                
                try:
                    tokenize = asaas.tokenize_credit_card(
                        request.user.customer_id,
                        credit_card,
                        holder_info,
                        request.META['REMOTE_ADDR']
                    )
                    credit_cards = CreditCards(
                        last_numbers_credit_card=tokenize['creditCardNumber'],
                        credit_card_brand=tokenize['creditCardBrand'],
                        credit_card_token=tokenize['creditCardToken'],
                        user=request.user,
                    )
                    credit_cards.save()
                except:
                    pass
            
        if response.status_code != 200:
            for error in response.json()['errors']:
                messages.add_message(request, constants.ERROR, error['description'])
            
            return redirect(reverse('step2', kwargs={'invoice_id': invoice_id}))
        
        return redirect(reverse('home'))