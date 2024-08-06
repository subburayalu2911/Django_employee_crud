from django.db import models
import uuid

from EmployeeApp.validators import validate_image_extension

# Create your models here.

employee_status = (
    (0,"In Active"),
    (1,"Active"),
    (2,"Delete"),
)

class Employee(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    employee_status = models.IntegerField(choices=employee_status, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phoneNo = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, validators=[validate_image_extension],upload_to='employee/profile_image/')


class EmployeeAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hno = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    employee = models.ForeignKey(Employee,on_delete=models.SET_NULL,blank=True,null=True,related_name='employee_address')


class EmployeeWorkExperience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    employee = models.ForeignKey(Employee,on_delete=models.SET_NULL,blank=True,null=True,related_name='employee_work_experience')


class EmployeeQualification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qualification_name = models.CharField(max_length=255, blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    employee = models.ForeignKey(Employee,on_delete=models.SET_NULL,blank=True,null=True,related_name='employee_qualification')


class EmployeeProjects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    employee = models.ForeignKey(Employee,on_delete=models.SET_NULL,blank=True,null=True,related_name='employee_projects')