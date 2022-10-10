from django import forms
from .models import Url
from .utils import valid_url

class OriginalUrlForm(forms.ModelForm):

    #não é na raiz
    class Meta:
        #qual o modelo que estou importando
        model = Url
        #quais campos que quero que o meu modelo mostre no form
        fields = ['original_url']

    #native method who is used when I save form
    
    def clean_original_url(self):
        original_url = self.cleaned_data['original_url']
        if not valid_url(original_url):
            raise forms.ValidationError("This is not a valid URL")

        # Sempre retorna o dado validado, você tendo mudado ele ou não.
        return original_url



