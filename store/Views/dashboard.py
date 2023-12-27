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
        unique_dates = set()
        for date in customers:
                unique_dates.add(date.date_field)
        sorted_unique_dates = sorted(unique_dates, reverse=False)
        formatted_dates = [date.strftime('%Y-%m-%d') for date in sorted_unique_dates]
        total_patients_count = Users.objects.count()
        
        # Divyansh 19 Dec 2023
        # for user in Users.objects.all():
        #     if user.xray:
        #         print(user.location)
        # Users.location = request.POST.get('location', None)
        # if Users.location ==0: 
        xray_modalities = Users.objects.filter(xray=True).count()
        ecg_modalities = Users.objects.filter(ecg=True).count()
        pft_modalities = Users.objects.filter(pft=True).count()
        audiometry_modalities = Users.objects.filter(audiometry=True).count()
        optometry_modalities = Users.objects.filter(optometry=True).count()
        sputum_modalities = Users.objects.filter(sputum=True).count()
        sample_collection_modalities = Users.objects.filter(sample_collection=True).count()
        
        if Users.location == 1:
                xray_modalities = Users.objects.filter(location_id=1, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=1, ecg=True).count()
                pft_modalities = Users.objects.filter(location_id=1, pft=True).count()
                audiometry_modalities = Users.objects.filter(location_id=1, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=1, optometry=True).count()
                sputum_modalities = Users.objects.filter(location_id=1, sputum=True).count()
                sample_collection_modalities = Users.objects.filter(location_id=1, sample_collection=True).count()

        elif Users.location == 2:
                xray_modalities = Users.objects.filter(location_id=2, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=2, ecg=True).count()
                audiometry_modalities = Users.objects.filter(location_id=2, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=2, optometry=True).count()
                sputum_modalities = Users.objects.filter(location_id=2, sputum=True).count()
                sample_collection_modalities = Users.objects.filter(location_id=2, sample_collection=True).count()

        elif Users.location == 3:
                xray_modalities = Users.objects.filter(location_id=3, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=3, ecg=True).count()
                audiometry_modalities = Users.objects.filter(location_id=3, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=3, optometry=True).count()
                sputum_modalities = Users.objects.filter(location_id=3, sputum=True).count()
                sample_collection_modalities = Users.objects.filter(location_id=3, sample_collection=True).count()
        
        elif  Users.location == 4:
                xray_modalities = Users.objects.filter(location_id=4, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=4, ecg=True).count()
                audiometry_modalities = Users.objects.filter(location_id=4, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=4, optometry=True).count()
                sputum_modalities = Users.objects.filter(location_id=4, sputum=True).count()
                sample_collection_modalities = Users.objects.filter(location_id=4, sample_collection=True).count()

        count_modalities = {'xray': xray_modalities,
                            'ecg': ecg_modalities,
                            'pft': pft_modalities,
                            'audiometry': audiometry_modalities,
                            'optometry': optometry_modalities,
                            'sputum': sputum_modalities,
                            'sample_collection': sample_collection_modalities}


        data = {'coordinator': coordinator, 'customers': customers, 'total_patient_counts': total_patients_count,
                'count': count_modalities, 'locations': location, 'date': formatted_dates}
        
        return render(request, 'dashboard.html', {'data': data})
   


