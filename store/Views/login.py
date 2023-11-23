from django.shortcuts import render, redirect
from django.views import View
from store.models.Coordinator import Coordinator
from store.models.Technician import Technician

class login(View):
    def get(self, request):
        return render(request, 'Login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        request.session['email'] = email
        request.session['password'] = password

        coordinator = Coordinator.objects.filter(email=email, password=password).first()
        technician = Technician.objects.filter(email=email, password=password).first()

        if coordinator:
            return redirect('dashboard')
        else:
            if technician:
                return redirect('form')

        return render(request, 'login.html', {'error': 'Invalid credentials'})
