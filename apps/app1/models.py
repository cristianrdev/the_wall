from django.db import models
from datetime import date, datetime, timedelta
import re

# Create your models here.


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['firstnameHTML'])<2:
            errors['firstnameHTML'] = "El nombre debe tener al menos de 2 caracteres"

        if len(postData['lastnameHTML'])<2:
            errors['lastnameHTML'] = "El apellido debe tener al menos de 2 caracteres"

        # valida el password
        if len(postData['passwordHTML'])<8:
            errors['passwordHTML'] = "la contraseña debe contener al menos 8 caracteres"

        if postData['passwordHTML'] != postData['password_confirmHTML']:
            errors['passwordHTML'] = "La contraseña no coincide con la de confirmación"

        #valida que la fecha esté ingresada
        if postData['birth_dateHTML']:
            #valida que la fecha no esté en el futuro
            date_today = date.today() #fecha hoy 
            if  postData['birth_dateHTML'] > str(date_today):
                errors['birth_dateHTML'] = "La fecha no puede estar en el futuro"
            else:
                # valida la edad mayor a 13 años
                birth_year = int(datetime.strptime(postData['birth_dateHTML'], '%Y-%m-%d').year) #año nacimieno
                birth_month = int(datetime.strptime(postData['birth_dateHTML'], '%Y-%m-%d').month) #mes de nacimiento
                birth_day = int(datetime.strptime(postData['birth_dateHTML'], '%Y-%m-%d').day) #día de nacimiento
                birth_date_user = date(birth_year, birth_month, birth_day )
                days_has_passed = (date_today-birth_date_user).days
                if days_has_passed < (365.2425*13):
                    errors['birth_dateHTML'] = "Debe ser mayor de 13 años para ingresar"
        else:
            errors['birth_dateHTML'] = "Debe ingresar su fecha de nacimiento"

        # valida el formato del email
        EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not EMAIL_REGEX.match(postData['emailHTML']):          
            errors['emailHTML'] = "Correo Invalido"
      
        # valida que el email no exista
        for s in User.objects.all():
            # se usa .lower() para ovbiar las mayúsculas en la comparación de palabras
            if postData['emailHTML'].lower() == s.email.lower(): 
                errors['emailHTML'] = "Este email ya existe"
        return errors



class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    birth_date = models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()