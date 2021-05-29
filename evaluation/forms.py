from django import forms
from .models import Evals

class EvalForm(forms.ModelForm):
    class Meta:
        model = Evals
        fields =['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = "강의평"

        self.fields['content'].widget.attrs.update({
            'class':'',
            'placeholder': '강의평을 작성해주세요',
        })