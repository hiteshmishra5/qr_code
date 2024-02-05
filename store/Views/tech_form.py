from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from store.models.customer import Users
from store.models.location import Location
from django.contrib.auth import logout
from django.db.models import Q
import pandas as pd
from datetime import datetime  
from pytz import timezone
from datetime import timedelta



class AddPatient(View):
    def get(self, request):
        customers = Users.objects.order_by('-id')
        location = Location.objects.all()
        return render(request, 'form.html', {'customers': customers, 'locations': location})

    def post(self, request):
        if 'submit' in request.POST:
            return self.add_patient(request)
        elif 'save_modalities' in request.POST:
            return self.save_modalities(request)
        else:
            return render(request, 'form.html')

    def add_patient(self, request):
        patient_id = request.POST.get('patient_id')
        if Users.objects.filter(patient_id=patient_id).exists():
            error_message = "Patient is already added!"
            customers = Users.objects.order_by('-id')  # Reverse order by id
            locations = Location.objects.all()
            data = {"error": error_message, "customers": customers, "locations": locations}
            return render(request, 'form.html', data)

        patient_name = request.POST.get('patient_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        weight = request.POST.get('weight')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        location_id = request.POST.get('location-select')
        date_field = request.POST.get('date-select')
        datetime_obj = datetime.strptime(date_field, "%Y-%m-%d")
        formatted_date = datetime_obj.strftime("%Y-%m-%d")


        try:
            location_instance = Location.objects.get(pk=location_id)
        except Location.DoesNotExist:
            print("Location not found in the database.")
            return HttpResponse("Location not found", status=400)

        # Fetching Data If validation is wrong.
        value = {"patient_name": patient_name,
                 "age": age,
                 "gender": gender,
                 "phone": phone,
                 "email": email,
                 "location": location_id,
                 "patient_id": patient_id,
                 "date": formatted_date}

        # Validate the customer object
        error_message = self.validate_customer(patient_name, age, phone, email, patient_id)
        if error_message:
            customers = Users.objects.order_by('-id')  # Reverse order by id
            locations = Location.objects.all()
            data = {"error": error_message, "customers": customers, "values": value, "locations": locations}
            return render(request, 'form.html', data)

        if not error_message:
            # Assuming Users is your model for storing patient details
            new_patient = Users.objects.create(
                location=location_instance,
                patient_id=patient_id,
                patient_name=patient_name,
                age=age,
                gender=gender,
                weight=weight,
                phone=phone,
                email=email,
                date_field=formatted_date,
                 
            )

            new_patient.save()
            return redirect('form')
    def validate_customer(self, patient_name, age, phone, email, patient_id):
        if not patient_id:
            return "Patient ID is required!"
        if not patient_name:
            return "Patient Name is required!"
        elif len(patient_name) < 4:
            return "Patient Name must be 4 characters long or more"
        elif not age:
            return "Age field is required"
        elif not phone:
            return "Phone Number is required"
        elif len(phone) < 10 and len(phone) > 10:
            return "Phone Number must be 10 digits"
        elif len(email) < 10:
            return "This is not a valid Email"

        return None
    def save_modalities(self, request):
        for key in request.POST.keys():
            if any(key.startswith(modality) for modality in ['xray+', 'ecg+', 'pft+', 'audiometry+', 'optometry+', 'sputum+']):

                patient_id_from_checkbox = key.split('+')[-1]
                print(patient_id_from_checkbox)

                # Fetch the corresponding patient instance
                try:
                    patient = Users.objects.get(patient_id=patient_id_from_checkbox)
                except Users.DoesNotExist:
                    return HttpResponse("Patient not found", status=400)

                # Fetch the current values from the database
                current_xray = patient.xray
                current_ecg = patient.ecg
                current_pft = patient.pft
                current_audiometry = patient.audiometry
                current_optometry = patient.optometry
                current_sputum = patient.sputum
                # current_sample_collection = patient.sample_collection

                # Update the modalities based on the form data if the checkbox is checked
                if 'xray+{}'.format(patient_id_from_checkbox) in request.POST:
                    patient.xray = True
                if 'ecg+{}'.format(patient_id_from_checkbox) in request.POST:
                    patient.ecg = True
                if 'pft+{}'.format(patient_id_from_checkbox) in request.POST:
                    patient.pft = True
                if 'audiometry+{}'.format(patient_id_from_checkbox) in request.POST:
                    patient.audiometry = True
                if 'optometry+{}'.format(patient_id_from_checkbox) in request.POST:
                    patient.optometry = True
                if 'sputum+{}'.format(patient_id_from_checkbox) in request.POST:
                    patient.sputum = True
                # if 'sample_collection_{}'.format(patient_id_from_checkbox) in request.POST:
                #     patient.sample_collection = True


                # If a checkbox was unchecked in the form but is already checked in the database, prevent the update
                if not patient.xray and current_xray:
                    patient.xray = current_xray
                if not patient.ecg and current_ecg:
                    patient.ecg = current_ecg
                if not patient.pft and current_pft:
                    patient.pft = current_pft
                if not patient.audiometry and current_audiometry:
                    patient.audiometry = current_audiometry
                if not patient.optometry and current_optometry:
                    patient.optometry = current_optometry
                if not patient.sputum and current_sputum:
                    patient.vitals = current_sputum
                # if not patient.sample_collection and current_sample_collection:
                #     patient.sample_collection = current_sample_collection

                patient.save()

        return redirect('form')


# Search Patient With Name
class SearchPatient(View):
    def get(self, request):
        query = request.GET.get('search')
        if query:
            customers = Users.objects.filter(Q(patient_name__icontains=query) | Q(patient_id__icontains=query)).distinct()
        else:
            customers = Users.objects.all()
        context = {'customers': customers}
        return render(request, "form.html", context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class UploadView(View):
    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request, *args, **kwargs):
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']

            # Check if the file is an Excel file
            if not excel_file.name.endswith('.xls') and not excel_file.name.endswith('.xlsx'):
                # Handle invalid file format
                return render(request, 'upload.html', {'error': 'Invalid file format'})

            try:
                df = pd.read_excel(excel_file)

                # Iterate through the DataFrame and save data to the Users table
                for index, row in df.iterrows():
                    patient_id = row['patient_id']

                    # Get or create patient by patient_id
                    patient, created = Users.objects.get_or_create(patient_id=patient_id)
                    # Assign values to fields
                    patient.patient_name = row['patient_name']
                    patient.age = row['age']
                    patient.gender = row['gender']
                    patient.phone = row['phone']
                    patient.email = row['email']
                    patient.weight = row['weight']
                    patient.address = row['address']
                    patient.audiometry = row['audiometry']
                    patient.ecg = row['ecg']
                    patient.optometry = row['optometry']
                    patient.pft = row['pft']
                    patient.sample_collection = row['sample_collection']
                    patient.vitals = row['vitals']
                    patient.xray = row['xray']
                    patient.save()
                return redirect('dashboard')

            except pd.errors.EmptyDataError:
                return render(request, 'upload.html', {'error': 'Empty Excel file'})

            except Exception as e:
                # Handle other exceptions
                print(f'Error processing Excel file: {e}')
                return render(request, 'upload.html', {'error': f'Error processing Excel file: {e}'})

        return render(request, 'upload.html')













