from django.db import models

class Address(models.Model):
    address = models.CharField(max_length=300, blank= True, editable=False)
    lat = models.DecimalField(max_digits=11, decimal_places=8, blank= True, editable=False)
    lng = models.DecimalField(max_digits=11, decimal_places=8, blank= True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    imported_xl = models.FileField(upload_to='imported_xls/')