from django import forms
from tasks.models import Task,TaskDetails

class TaskForm(forms.Form):

    title=forms.CharField(label="Task Title")
    descriptions=forms.CharField(widget=forms.Textarea,label="Task Descriptions")
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(
    widget=forms.CheckboxSelectMultiple, choices=[], label='Assigned To')
    
    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]




class StyledFormMixin:
    default_classes = (
        "w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm "
        "focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500 "
        "bg-white text-gray-900 placeholder-gray-400"
    )

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': self.default_classes
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2 ml-3 text-gray-800"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })


class TaskModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','descriptions','due_date','assigned_to']
        widgets={
            "due_date":forms.SelectDateWidget,
            "assigned_to":forms.CheckboxSelectMultiple,
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

class TaskDetailsModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=TaskDetails
        fields = ["priority","notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()    
