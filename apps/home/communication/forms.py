from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}))
    # message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your request subject'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your message'}),
        }
