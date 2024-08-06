from django.shortcuts import render
from django.http import JsonResponse
from EmployeeApp.models import *

# Create your views here.


def home_page(request):
    employee_count = Employee.objects.all()
    total_count = employee_count.count()
    active_count = employee_count.filter(employee_status=1).count()
    inactive_count = employee_count.filter(employee_status=0).count()
    deleted_count = employee_count.filter(employee_status=2).count()
    context = {
        "total_employees": total_count,
        "active_employees": active_count,
        "inactive_employees": inactive_count,
        "deleted_employees": deleted_count,
    }
    return render(request, 'home/home.html', context=context)


def table_page(request):
    employee_datas = Employee.objects.all().exclude(employee_status=3)
    context = {
        "queryset": employee_datas
    }
    return render(request, 'table/employee_list_table.html', context=context)


def add_employee_page(request, employee_id=None):
    if employee_id is None:  # if id wasn't pass then it will be redirect to a new create page
        return render(request, 'table/add_employee.html')
    else:
        employee_data = Employee.objects.filter(id=employee_id).exclude(
            employee_status=3).first()  # here we check the given id was valid and not deleted
        # here we get the address details which was created against employee
        address_details = employee_data.employee_address.all().first()
        if not employee_data:  # if we didn't find the employee data then pass the error
            return JsonResponse({'msg': 'Invalid employee ID'}, status=400)
        if request.method == 'GET':  # if it is get method then rediect to page with data
            context = {
                "queryset": employee_data,
                "address_details": address_details
            }
            return render(request, 'table/add_employee.html', context=context)

        if request.method == 'DELETE':  # if it is delete method then we delete the employee
            employee_data.employee_status = 2
            employee_data.save()
            return JsonResponse({'msg': 'Employee Deleted Successfully'}, status=200)

        if request.method == 'POST':  # if it is POST method then we update the employee from the given data
            data = request.POST
            file = request.FILES
            # here we pass the data and query to update
            try:
                update_employee(data, file, employee_data, address_details)
                return JsonResponse({'msg': 'Employee Updated Successfully', 'emp_id': str(employee_data.id)}, status=200)
            except Exception as e:
                return JsonResponse({'msg': f'Error because of {str(e)}'}, status=400)


def update_employee(data, files, employee_data, employee_address):
    name = data.get('name')
    if name:
        employee_data.name = name

    email = data.get('email')
    if email:
        employee_data.email = email

    age = data.get('age')
    if age:
        employee_data.age = age

    employee_status = data.get('active') or 0
    if employee_status:
        employee_data.employee_status = employee_status

    gender = data.get('gender')
    if gender:
        employee_data.gender = gender

    phoneNo = data.get('phoneNo')
    if phoneNo:
        employee_data.phoneNo = phoneNo

    profile_image = files.get('profile_image')
    if profile_image:
        employee_data.profile_image = profile_image

    if employee_address:
        hno = data.get('hno')
        if hno:
            employee_address.hno = hno

        street = data.get('street')
        if street:
            employee_address.street = street

        city = data.get('city')
        if city:
            employee_address.city = city

        state = data.get('state')
        if state:
            employee_address.state = state


def create_employee(request):
    """
    Here we write a function for creating a new employee
    """
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        employee_status = data.get('active') or 0
        gender = data.get('gender')
        phoneNo = data.get('phoneNo')
        profile_image = request.FILES.get('profile_image')
        hno = data.get('hno')
        street = data.get('street')
        city = data.get('city')
        state = data.get('state')

        try:

            if not email:  # here we check the email was given or not
                return JsonResponse({'msg': 'Please enter your email address'}, status=400)

            # here we check the active employee was exist or not
            employee_check = Employee.objects.filter(
                email=email, employee_status=1).first()

            if employee_check:  # here we pass the error because the employee email was already exists
                return JsonResponse({'msg': 'Given Employee Email ID was already exists'}, status=400)

            # once validate done we create a new employee
            employee_create = Employee.objects.create(name=name, email=email, age=age, employee_status=employee_status,
                                                      gender=gender, phoneNo=phoneNo, profile_image=profile_image)

            # then we create a employee details for the employee
            employee_address_create = EmployeeAddress.objects.create(employee=employee_create,
                                                                     hno=hno, street=street, city=city, state=state)

            return JsonResponse({'msg': 'Employee details created successfully', 'emp_id': str(employee_create.id)}, status=200)
        except Exception as e:
            return JsonResponse({'msg': f'Error because of {str(e)}'}, status=400)


def work_experience_page(request, employee_id):
    employee_id_check = Employee.objects.filter(id=employee_id).exclude(employee_status=3).first()  # here we check the given employee id is valid or not
    if not employee_id_check:
        return JsonResponse({'msg': 'Invlaid Employee ID'}, status=400)
    work_experience_data = EmployeeWorkExperience.objects.filter(
        employee_id=employee_id_check)
    context = {
        'work_experience_data': work_experience_data,
        "queryset": employee_id_check,
    }
    return render(request, 'table/work_experience.html', context=context)


def work_experience_create_edit_delete(request, wrk_exp_id=None):
    """
    Here we create , edit and delete the work experience details
    """
    if wrk_exp_id is None and request.method == 'POST':
        data = request.POST
        employee_id = data.get('employee_id')
        company_name = data.get('company_name')
        company_address = data.get('company_address')
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        try:
            employee_id_check = Employee.objects.filter(id=employee_id).exclude(
                employee_status=3).first()  # here we check the given employee id is valid or not
            if not employee_id_check:
                return JsonResponse({'msg': 'Invlaid Employee ID'}, status=400)

            # then we create a new work experience detail against the employee
            work_exp_create = EmployeeWorkExperience.objects.create(employee=employee_id_check, company_address=company_address,
                                    company_name=company_name, from_date=from_date, to_date=to_date)

            return JsonResponse({'msg': 'Work experience created successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'msg': f'Error because of {str(e)}'}, status=400)

    work_exp_data = EmployeeWorkExperience.objects.filter(
        id=wrk_exp_id).first() # here we check the given id is valid or not
    if not work_exp_data:
        return JsonResponse({'msg': "Invalid ID"}, status=400)

    if request.method == 'GET':
        work_exp_data_dict = work_exp_data.__dict__  #  here we get the work_exp_data into a dictionary
        work_exp_data_dict.pop('_state')  #  here we remove the _state from the work_exp_data
        return JsonResponse({'status': 'success', 'data': dict(work_exp_data_dict)}, status=200)

    if request.method == 'POST':
        data = request.POST
        company_name = data.get('company_name')
        company_address = data.get('company_address')
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        try:
            #  here we update the company details.
            work_exp_data.company_name = company_name if company_name else work_exp_data.company_name
            work_exp_data.company_address = company_address if company_address else work_exp_data.company_address
            work_exp_data.from_date = from_date if from_date else work_exp_data.from_date
            work_exp_data.to_date = to_date if to_date else work_exp_data.to_date
            work_exp_data.save()
            return JsonResponse({'msg': "Work Experience Detail Updated Successfully"}, status=200)
        except Exception as e:
            return JsonResponse({'msg': f'Error because of {str(e)}'}, status=400)

    if request.method == 'DELETE':
        work_exp_data.delete() #  here we hard delete the work_exp_data
        return JsonResponse({'msg': "Work Experience Detail Deleted Successfully"}, status=200)


def qualification_page(request, employee_id):
    employee_id_check = Employee.objects.filter(id=employee_id).exclude(employee_status=3).first()  # here we check the given employee id is valid or not
    if not employee_id_check:
        return JsonResponse({'msg': 'Invlaid Employee ID'}, status=400)
    qualification_data = EmployeeQualification.objects.filter(
        employee_id=employee_id_check)
    context = {
        'qualification_datas': qualification_data,
        "queryset": employee_id_check,
    }
    return render(request, 'table/qualifications.html', context=context)


def qualification_create_edit_delete(request, qualification_id=None):
    """
    Here we create , edit and delete the qualification details
    """
    if qualification_id is None and request.method == 'POST':
        data = request.POST
        employee_id = data.get('employee_id')
        qualification_name = data.get('qualification_name')
        percentage = data.get('percentage')

        try:
            employee_id_check = Employee.objects.filter(id=employee_id).exclude(
                employee_status=3).first()  # here we check the given employee id is valid or not
            if not employee_id_check:
                return JsonResponse({'msg': 'Invlaid Employee ID'}, status=400)

            # then we create a new work experience detail against the employee
            qualification_create = EmployeeQualification.objects.create(employee=employee_id_check, 
                                    qualification_name=qualification_name, percentage=percentage)

            return JsonResponse({'msg': 'Qualification added successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'msg': f'Error because of {str(e)}'}, status=400)

    qualification_data = EmployeeQualification.objects.filter(id=qualification_id).first() # here we check the given id is valid or not
    if not qualification_data:
        return JsonResponse({'msg': "Invalid ID"}, status=400)

    if request.method == 'GET':
        qualification_data_dict = qualification_data.__dict__  #  here we get the qualification_data into a dictionary
        qualification_data_dict.pop('_state')  #  here we remove the _state from the qualification_data
        return JsonResponse({'status': 'success', 'data': dict(qualification_data_dict)}, status=200)

    if request.method == 'POST':
        data = request.POST
        qualification_name = data.get('qualification_name')
        percentage = data.get('percentage')
        try:
            #  here we update the company details.
            qualification_data.qualification_name = qualification_name if qualification_name else qualification_data.qualification_name
            qualification_data.percentage = percentage if percentage else qualification_data.percentage
            qualification_data.save()
            return JsonResponse({'msg': "Qualification Detail Updated Successfully"}, status=200)
        except Exception as e:
            return JsonResponse({'msg': f'Error because of {str(e)}'}, status=400)

    if request.method == 'DELETE':
        qualification_data.delete() #  here we hard delete the qualification_data
        return JsonResponse({'msg': "Qualification Deleted Successfully"}, status=200)


def project_page(request, employee_id):
    employee_id_check = Employee.objects.filter(id=employee_id).exclude(employee_status=3).first()  # here we check the given employee id is valid or not
    if not employee_id_check:
        return JsonResponse({'msg': 'Invlaid Employee ID'}, status=400)
    project_data = EmployeeProjects.objects.filter(
        employee_id=employee_id_check)
    context = {
        'project_datas': project_data,
        "queryset": employee_id_check,
    }
    return render(request, 'table/project.html', context=context)


def project_create_edit_delete(request, project_id=None):
    """
    Here we create , edit and delete the project details
    """
    if project_id is None and request.method == 'POST':
        data = request.POST
        employee_id = data.get('employee_id')
        project_name = data.get('project_name')
        description = data.get('description')

        try:
            employee_id_check = Employee.objects.filter(id=employee_id).exclude(
                employee_status=3).first()  # here we check the given employee id is valid or not
            if not employee_id_check:
                return JsonResponse({'msg': 'Invlaid Employee ID'}, status=400)

            # then we create a new project detail against the employee
            project_create = EmployeeProjects.objects.create(employee=employee_id_check, 
                                    title=project_name, description=description)

            return JsonResponse({'msg': 'Project added successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'msg': f'Error because of {str(e)}'}, status=400)

    project_data = EmployeeProjects.objects.filter(id=project_id).first() # here we check the given id is valid or not
    if not project_data:
        return JsonResponse({'msg': "Invalid ID"}, status=400)

    if request.method == 'GET':
        project_data_dict = project_data.__dict__  #  here we get the project_data into a dictionary
        project_data_dict.pop('_state')  #  here we remove the _state from the project_data
        return JsonResponse({'status': 'success', 'data': dict(project_data_dict)}, status=200)

    if request.method == 'POST':
        data = request.POST
        project_name = data.get('project_name')
        description = data.get('description')
        try:
            #  here we update the company details.
            project_data.title = project_name if project_name else project_data.project_name
            project_data.description = description if description else project_data.description
            project_data.save()
            return JsonResponse({'msg': "Project Updated Successfully"}, status=200)
        except Exception as e:
            return JsonResponse({'msg': f'Error because of {str(e)}'}, status=400)

    if request.method == 'DELETE':
        project_data.delete() #  here we hard delete the project_data
        return JsonResponse({'msg': "Project Deleted Successfully"}, status=200)
