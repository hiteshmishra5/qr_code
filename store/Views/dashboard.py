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
        
        selected_location_id = request.GET.get('location', None)
        # print(selected_location_id)
        modalities_filter = {}
        if selected_location_id and selected_location_id != 'all':
                modalities_filter['location_id'] = selected_location_id

        count_modalities = {
                'xray': Users.objects.filter(xray=True, **modalities_filter).count(),
                'ecg': Users.objects.filter(ecg=True, **modalities_filter).count(),
                'pft': Users.objects.filter(pft=True, **modalities_filter).count(),
                'audiometry': Users.objects.filter(audiometry=True, **modalities_filter).count(),
                'optometry': Users.objects.filter(optometry=True, **modalities_filter).count(),
                'sputum': Users.objects.filter(sputum=True, **modalities_filter).count(),
                'sample_collection': Users.objects.filter(sample_collection=True, **modalities_filter).count()
        }

        data = {
                'coordinator': coordinator,
                'customers': customers,
                'total_patient_counts': total_patients_count,
                'count': count_modalities,
                'locations': location,
                'date': formatted_dates  # You need to define formatted_dates
        }

        return render(request, 'dashboard.html', {'data': data})
        # xray_modalities = Users.objects.filter(xray=True).count()
        # ecg_modalities = Users.objects.filter(ecg=True).count()
        # pft_modalities = Users.objects.filter(pft=True).count()
        # audiometry_modalities = Users.objects.filter(audiometry=True).count()
        # optometry_modalities = Users.objects.filter(optometry=True).count()
        # sputum_modalities = Users.objects.filter(sputum=True).count()
        # sample_collection_modalities = Users.objects.filter(sample_collection=True).count()
        
        if selected_location_id==1:
                xray_modalities = Users.objects.filter(location_id=1, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=1, ecg=True).count()
                pft_modalities = Users.objects.filter(location_id=1, pft=True).count()
                audiometry_modalities = Users.objects.filter(location_id=1, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=1, optometry=True).count()
                sputum_modalities = Users.objects.filter(location_id=1, sputum=True).count()
                sample_collection_modalities = Users.objects.filter(location_id=1, sample_collection=True).count()

        elif selected_location_id==2:
                xray_modalities = Users.objects.filter(location_id=2, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=2, ecg=True).count()
                audiometry_modalities = Users.objects.filter(location_id=2, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=2, optometry=True).count()
                sputum_modalities = Users.objects.filter(location_id=2, sputum=True).count()
                sample_collection_modalities = Users.objects.filter(location_id=2, sample_collection=True).count()

        elif selected_location_id==3:
                xray_modalities = Users.objects.filter(location_id=3, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=3, ecg=True).count()
                audiometry_modalities = Users.objects.filter(location_id=3, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=3, optometry=True).count()
                sputum_modalities = Users.objects.filter(location_id=3, sputum=True).count()
                sample_collection_modalities = Users.objects.filter(location_id=3, sample_collection=True).count()
        
        elif  selected_location_id==4:
                xray_modalities = Users.objects.filter(location_id=4, xray=True).count()
                ecg_modalities = Users.objects.filter(location_id=4, ecg=True).count()
                audiometry_modalities = Users.objects.filter(location_id=4, audiometry=True).count()
                optometry_modalities = Users.objects.filter(location_id=4, optometry=True).count()
                sputum_modalities = Users.objects.filter(location_id=4, sputum=True).count()
                sample_collection_modalities = Users.objects.filter(location_id=4, sample_collection=True).count()
        
        else :
                xray_modalities = Users.objects.filter(xray=True).count()
                ecg_modalities = Users.objects.filter(ecg=True).count()
                pft_modalities = Users.objects.filter(pft=True).count()
                audiometry_modalities = Users.objects.filter(audiometry=True).count()
                optometry_modalities = Users.objects.filter(optometry=True).count()
                sputum_modalities = Users.objects.filter(sputum=True).count()
                sample_collection_modalities = Users.objects.filter(sample_collection=True).count()
               

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
   


