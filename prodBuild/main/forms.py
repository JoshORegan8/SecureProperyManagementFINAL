from django import forms
from .models import propDoc1, propDoc, Property


class CreatePortfolio(forms.Form):
    name = forms.CharField(label="Name", max_length=300)


class CreateProperty(forms.Form):
    # streetAddress = forms.CharField(label="Street Address", max_length=300)
    # city = forms.CharField(label="City", max_length=300)
    # occupied = forms.BooleanField(required=False)
    # occupiedBy = forms.CharField(
    #     label="Tenant", max_length=300, required=False)
    # image = forms.ImageField(upload_to='property/images')
    class Meta:
        model = Property
        fields = ('streetAddress', 'city', 'occupied', 'occupiedBy')


class FileForm(forms.ModelForm):
    class Meta:
        model = propDoc1
        fields = ('Property', 'name', 'pdf', 'pdfPass')
