from django import forms
from .models import Url

class OriginalUrlForm(forms.ModelForm):

    #não é na raiz
    class Meta:
        #qual o modelo que estou importando
        model = Url
        #quais campos que quero que o meu modelo mostre no form
        fields = ['original_url']

    # #Validar a URL
    # def clean(self):
    #     super(OriginalUrlForm, self).clean()
    #
    #     original_url = self.cleaned_data.get('original_url')
    #
    #     if len(original_url) < 5:
    #         self._errors['original_url'] = self.error_class(['Minimum 5 characters required'])
    #
    #     return self.cleaned_data


