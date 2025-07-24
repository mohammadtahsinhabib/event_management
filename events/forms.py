import re
from django import forms
from django.contrib.auth.models import User
from events.models import Event, Category
from django.contrib.auth.forms import AuthenticationForm


class StyleMixins:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    default_classes = (
        "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm "
        "focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    )

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if field_name == "confirm_password":
                field.widget.attrs.update({"class": self.default_classes})
            else:
                field.widget.attrs.update(
                    {
                        "class": self.default_classes,
                        "placeholder": f"Enter {field.label.title()}",
                    }
                )


class CategoryForm(StyleMixins, forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(),
            "description": forms.Textarea(
                attrs={"placeholder": "Event description", "rows": 3}
            ),
        }


class EventForm(StyleMixins, forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(),
            "description": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Enter Description"}
            ),  # Not Working
            "date": forms.DateInput(),
            "time": forms.TimeInput(),
            "location": forms.TextInput(),
            "category": forms.Select(),
            "participants": forms.SelectMultiple(),
        }


class SignUpForm(StyleMixins, forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password"})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        errors = []

        if len(password) < 8:
            errors.append("Password must be at least 8 character long")

        if not re.search(r"[A-Z]", password):
            errors.append("Password must include at least one uppercase letter.")

        if not re.search(r"[a-z]", password):
            errors.append("Password must include at least one lowercase letter.")

        if not re.search(r"[0-9]", password):
            errors.append("Password must include at least one number.")

        if not re.search(r"[@#$%^&+=]", password):
            errors.append("Password must include at least one special character.")

        if errors:
            raise forms.ValidationError(errors)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Both Password should be change")
        return cleaned_data


class LoginForm(StyleMixins, AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
