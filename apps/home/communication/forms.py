from django import forms
from .models import Contact

INPUT_CLASS = (
    "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm "
    "text-slate-900 outline-none transition placeholder:text-slate-400 "
    "focus:border-brand-400 focus:ring-4 focus:ring-brand-100 "
    "dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 "
    "dark:placeholder:text-slate-500 dark:focus:ring-brand-500/20"
)


class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": INPUT_CLASS,
                "placeholder": "Your Name",
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "class": INPUT_CLASS,
                "placeholder": "Your email address",
                "autocomplete": "email",
            }),
            "phone": forms.TextInput(attrs={
                "class": INPUT_CLASS,
                "placeholder": "Your phone number",
                "autocomplete": "tel",
            }),
            "subject": forms.TextInput(attrs={
                "class": INPUT_CLASS,
                "placeholder": "Your request subject",
            }),
            "message": forms.Textarea(attrs={
                "class": INPUT_CLASS,
                "rows": 5,
                "placeholder": "Your message",
            }),
        }

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    def clean_message(self):
        message = (self.cleaned_data.get("message") or "").strip()
        if len(message) < 10:
            raise forms.ValidationError("Please enter a more detailed message.")
        return message

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        return phone



INPUT_CLASS = (
    "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm "
    "text-slate-900 outline-none transition placeholder:text-slate-400 "
    "focus:border-brand-400 focus:ring-4 focus:ring-brand-100 "
    "dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 "
    "dark:placeholder:text-slate-500 dark:focus:ring-brand-500/20"
)

SELECT_CLASS = (
    "w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm "
    "text-slate-900 outline-none transition focus:border-brand-400 "
    "focus:ring-4 focus:ring-brand-100 dark:border-slate-700 "
    "dark:bg-slate-900 dark:text-slate-100 dark:focus:ring-brand-500/20"
)


class SubscriberForm(forms.Form):
    ACTION_SUBSCRIBE = "subscribe"
    ACTION_UNSUBSCRIBE = "unsubscribe"
    ACTION_RESUBSCRIBE = "resubscribe"

    ACTION_CHOICES = (
        (ACTION_SUBSCRIBE, "Subscribe"),
        (ACTION_UNSUBSCRIBE, "Unsubscribe"),
        (ACTION_RESUBSCRIBE, "Resubscribe"),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": "Your email address",
                "autocomplete": "email",
            }
        )
    )

    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={"class": SELECT_CLASS}),
        initial=ACTION_SUBSCRIBE,
    )

    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        return email

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value
