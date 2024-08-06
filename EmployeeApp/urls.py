from django.urls import path ,include
from EmployeeApp.views import *

app_name = 'employee_app'

urlpatterns = [

    path('', home_page,name="home_page"),
    path('table/', table_page,name="table_page"),
    path('table/add_employee_screen/', add_employee_page,name="add_employee_page"),
    path('table/add_employee_screen/<uuid:employee_id>/', add_employee_page,name="single_employee_crud"),
    path('table/employee/', create_employee,name="create_employee"),


    path('table/employee/work_experience/<uuid:employee_id>/', work_experience_page, name="work_experience_page"),
    path('table/employee/work_experience/create/', work_experience_create_edit_delete, name="work_experience_create"),
    path('table/employee/work_experience/crud/<uuid:wrk_exp_id>/', work_experience_create_edit_delete, name="work_experience_crud"),


    path('table/employee/qualification/<uuid:employee_id>/', qualification_page, name="qualification_page"),
    path('table/employee/qualification/create/', qualification_create_edit_delete, name="qualification_create"),
    path('table/employee/qualification/crud/<uuid:qualification_id>/', qualification_create_edit_delete, name="qualification_crud"),



    path('table/employee/project/<uuid:employee_id>/', project_page, name="project_page"),
    path('table/employee/project/create/', project_create_edit_delete, name="project_create"),
    path('table/employee/project/crud/<uuid:project_id>/', project_create_edit_delete, name="project_crud"),

]
