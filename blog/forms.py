from django.forms import Form,ModelForm,widgets, ModelChoiceField,ChoiceField
from .models import *
from django.forms import IntegerField

class PostForm(ModelForm):
    class Meta:
        model=ArticleSheet
        fields=('title','content','tag','type')
        widgets={
            'title':widgets.TextInput(attrs={'placeholder':'title'}),
            'content':widgets.Textarea(attrs={'placeholder':'content'}),
            'tag':widgets.TextInput(attrs={'placeholder':'tag'}),
            'type':widgets.Select(),
        }