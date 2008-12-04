from django import forms
from publications.models import Publication

class PublicationForm(forms.ModelForm):
    title = forms.CharField(max_length=50, widget=forms.TextInput)
    description = forms.CharField(max_length=100, widget=forms.Textarea)

    class Meta:
        model = Publication
        fields = ('title','description')
