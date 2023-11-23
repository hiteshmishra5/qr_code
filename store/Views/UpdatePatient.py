from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models.customer import Users

class UpdatePatient(View):
    def get(self, request, customer_id):
        customer = Users.objects.get(id=customer_id)
        return render(request, 'updatepatient.html', {'customer': customer})

    def post(self, request, customer_id):
        # Check for the presence of the 'optometry_form' parameter
        if 'optometry_form' in request.POST:
            print("Hitesh")
            far_vision_right = request.POST.get("far_vision_right")
            far_vision_left = request.POST.get("far_vision_left")
            near_vision_right = request.POST.get("near_vision_right")
            near_vision_left = request.POST.get("near_vision_left")
            color_vision = request.POST.get("color_vision")
            others = request.POST.get("others")

            optometry = OptometryModel(
                far_vision_right=far_vision_right,
                far_vision_left=far_vision_left,
                near_vision_right=near_vision_right,
                near_vision_left=near_vision_left,
                color_vision=color_vision,
                others=others
            )
            optometry.save()

            return redirect("form")

        # If 'optometry_form' is not present, it's a regular patient update form
        customer = get_object_or_404(Users, pk=customer_id)
        customer.patient_id = request.POST.get('patient_id')
        customer.patient_name = request.POST.get('patient_name')
        customer.age = request.POST.get('age')
        customer.weight = request.POST.get('weight')
        customer.gender = request.POST.get('gender')
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        customer.address = request.POST.get('address')

        customer.save()
        return redirect('form')

# delete Data
class DeletePatient(View):
    def post(self, request, customer_id):
        user = Users.objects.get(pk=customer_id)
        user.delete()
        return redirect('form')
