from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class EmployeeManager(BaseUserManager):
    def create_user(self, employee_id, name, username, password=None, role='employee'):
        if not username:
            raise ValueError('The Username field is required')
        if not employee_id:
            raise ValueError('The Employee ID field is required')
        
        user = self.model(
            employee_id=employee_id,
            name=name,
            username=username,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_id, name, username, password=None):
        user = self.create_user(
            employee_id=employee_id,
            name=name,
            username=username,
            password=password,
            role='admin'
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Employee(AbstractBaseUser):
    employee_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = EmployeeManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['employee_id', 'name']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
