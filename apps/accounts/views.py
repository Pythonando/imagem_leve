from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserCreationForm
from payments.asaas.asaas_payment import AsaasInvoice
from django.core.cache import cache
from optimizer.models import AccessTokens, WebhookLog
from django.contrib.messages import constants
from django.contrib import messages

class Register(View):
    template_name = 'register.html'
    form = UserCreationForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

        return render(request, self.template_name, {'form': form})


class Perfil(View):
    template_name = 'perfil.html'

    def get(self, request):
        
        cache_key = f'invoices_{request.user.id}'

        invoices = cache.get(cache_key)

        if not invoices:
            print('entrei aqui')
            asaas = AsaasInvoice()
            invoices = asaas.list_invoices(request.user.customer_id)
            cache.set(cache_key, invoices, 60 * 5)
        
        logs = WebhookLog.objects.filter(user=request.user)
        # TODO: PAGINAR
        access_token = AccessTokens.objects.filter(user=request.user).first()
        
        return render(request, self.template_name, {'invoices': invoices['data'], 'access_token':access_token, 'logs': logs})

class SetWebhook(View):

    def get(self, request):
        url = request.GET.get('webhook')

        request.user.webhook = url
        request.user.save()
        messages.add_message(request, constants.SUCCESS, 'Webhook definido com sucesso')
        return redirect('perfil')

class ViewLog(View):
    template_name = 'view_log.html'
    def get(self, request, id):
        log = get_object_or_404(WebhookLog, id=id)
        return render(request, self.template_name, {'log': log})