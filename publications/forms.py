from django import forms
from publications.models import Publication, Reading

class PublicationForm(forms.ModelForm):
    title = forms.CharField(max_length=50, widget=forms.TextInput)
    description = forms.CharField(max_length=100, widget=forms.Textarea)
    
    class Meta:
        model = Publication
        fields = ('title','description')

class ReadingForm(forms.ModelForm):

    class Meta:
        model = Reading
        fields = ('rating')
