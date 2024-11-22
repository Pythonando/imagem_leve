from django.shortcuts import render, redirect
from django.views import View
from .models import AccessTokens
from django.contrib.messages import constants
from django.contrib import messages

class GenerateToken(View):
    def get(self, request):
        instance, created = AccessTokens.objects.get_or_create(
            user=request.user,
            defaults={'token': AccessTokens.gen_token(request.user.id)}
        )

        if not created:
            instance.token = AccessTokens.gen_token(request.user.id)
            instance.save()

        messages.add_message(request, constants.SUCCESS, 'Token atualizado com sucesso')
        return redirect('perfil')
