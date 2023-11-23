from django.shortcuts import render
from django.views import View
from store.models.customer import Users
from store.models.Coordinator import Coordinator
from store.models.location import Location

class Dashboard(View):
    def get(self, request):
        email = request.session.get('email')
        password = request.session.get('password')
        coordinator = Coordinator.objects.filter(email=email, password=password).first()
        customers = Users.objects.order_by('-id')
        location = Location.objects.all()
        total_patients_count = Users.objects.count()

        xray_modalities = Users.objects.filter(xray=True).count()
        ecg_modalities = Users.objects.filter(ecg=True).count()
        pft_modalities = Users.objects.filter(pft=True).count()
        audiometry_modalities = Users.objects.filter(audiometry=True).count()
        optometry_modalities = Users.objects.filter(optometry=True).count()
        vitals_modalities = Users.objects.filter(vitals=True).count()
        sample_collection_modalities = Users.objects.filter(sample_collection=True).count()

        count_modalities = {'xray': xray_modalities,
                            'ecg': ecg_modalities,
                            'pft': pft_modalities,
                            'audiometry': audiometry_modalities,
                            'optometry': optometry_modalities,
                            'vitals': vitals_modalities,
                            'sample_collection': sample_collection_modalities}


        data = {'coordinator': coordinator, 'customers': customers, 'total_patient_counts': total_patients_count,
                'count': count_modalities, 'locations': location}

        return render(request, 'dashboard.html', {'data': data})
