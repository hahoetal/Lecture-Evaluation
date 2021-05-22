from django import forms
from evaluation.models import Evals

class EvalForm(forms.ModelForm):
    class Meta:
        model = Evals
        fields = ['content', 'hw_level', 'test_level', 'lect_power'] # 강의평, 과제 난이도, 시험 난이도, 강의력 정보만 입력받음.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = "강의평"
        self.fields['hw_level'].label = "과제 난이도"
        self.fields['test_level'].label = "시험 난이도"
        self.fields['lect_power'].label = "강의력"

        self.fields['content'].widget.attrs.update({
            'class':'',
            'placeholder': '강의평을 작성해주세요',
        })

        self.fields['test_level'].widget.attrs.update({
            'class': '',
        })

        self.fields['lect_power'].widget.attrs.update({
            'class': '',
        })