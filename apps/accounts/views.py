from django.shortcuts import render, redirect
from django.views import View
from .forms import UserCreationForm


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