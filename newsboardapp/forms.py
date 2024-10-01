from django import forms
from .models import Post,Category
from django.core.exceptions import ValidationError
from datetime import datetime

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['caption', 'text', 'сategory']

   def clean(self):
       cleaned_data = super().clean()
       caption = cleaned_data.get("caption")
       text = cleaned_data.get("text")
       if caption == text:
           raise ValidationError("Заголовок не должен быть идентичен тексту новости.")
       date_time = cleaned_data.get("datetime")
       if date_time == None:
           cleaned_data.datetime = datetime.utcnow()
       return cleaned_data




class ArticleForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['caption', 'text', 'сategory']

   def clean(self):
       cleaned_data = super().clean()
       caption = cleaned_data.get("caption")
       text = cleaned_data.get("text")
       if caption == text:
           raise ValidationError("Заголовок не должен быть идентичен тексту статьи.")
       return cleaned_data


class CatForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

