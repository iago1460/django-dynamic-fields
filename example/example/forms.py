from django import forms
from example.models import Survey


class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = '__all__'
