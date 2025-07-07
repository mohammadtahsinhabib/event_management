from django import forms
from events.models import Event, Participant, Category



class StyleMixins:
    default_classes = (
        "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm "
        "focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    )

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': self.default_classes,
                'placeholder': f"Enter {field.label.title()}"
            })


class CategoryForm(StyleMixins,forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets={
            "name":forms.TextInput(),
            "description":forms.Textarea(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

class EventForm(StyleMixins,forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea(attrs={'rows':4}),
            'date': forms.DateInput(),
            'time': forms.TimeInput(),
            'location': forms.TextInput(),
            'category': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

class ParticipantForm(StyleMixins,forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
    
        widgets={
            "name":forms.TextInput(),
            "email":forms.EmailInput(),
            "events":forms.Select(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()    
