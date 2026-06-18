from django import forms

class CarContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    car_details = forms.CharField(widget=forms.Textarea, label="Car Details")
    email = forms.EmailField(required=False, label="Your Email (optional)")
    whatsapp_number = forms.CharField(max_length=15, required=False, label="Your WhatsApp Number")   



class CarSubmissionForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    phone = forms.CharField(max_length=15, label="Your Phone")
    message = forms.CharField(widget=forms.Textarea, label="Your Message")



#forms for multiple images for custmers to view car when they click on views
from django import forms
from .models import ProductImage

class ProductContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    product_details = forms.CharField(widget=forms.Textarea, label="Car Details")
    email = forms.EmailField(required=False, label="Your Email (optional)")
    whatsapp_number = forms.CharField(max_length=15, required=False, label="Your WhatsApp Number")

class ProductSubmissionForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    phone = forms.CharField(max_length=15, label="Your Phone")
    message = forms.CharField(widget=forms.Textarea, label="Your Message")

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']



