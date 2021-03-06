from django import forms
from publications.models import Publication, Reading, Quote, RATING_CHOICES

class PublicationForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=50, widget=forms.TextInput)
    description = forms.CharField(label='Description', max_length=100, widget=forms.Textarea)
    rating = forms.ChoiceField(label='Rating', choices=RATING_CHOICES)
    
    class Meta:
        model = Publication
        fields = ('title','description')

class ReadingForm(forms.ModelForm):
    rating = forms.ChoiceField(label='Rating', choices=RATING_CHOICES)

    class Meta:
        model = Reading
        fields = ('rating',)

class QuoteForm(forms.ModelForm):
    text = forms.CharField(label='Quote', max_length=250, widget=forms.TextInput)

    class Meta:
        model = Quote
        fields = ('text',)
