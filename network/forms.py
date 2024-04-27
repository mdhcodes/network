# Create forms from models.
# https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
# https://www.geeksforgeeks.org/django-modelform-create-form-from-models/


from django import forms
from .models import Post

# Create a Post ModelForm.
class CreatePostForm(forms.ModelForm):
    # Specify the name of the model to use.
    class Meta:
        model = Post
        fields = '__all__'
        # https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
        # https://medium.com/swlh/how-to-style-your-django-forms-7e8463aae4fa
        # https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
        # Style Django forms with built-in widgets.
        widgets = {            
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'post': forms.Textarea(attrs={'class': 'form-control'}),
            'likes': forms.HiddenInput(),
            'created': forms.HiddenInput(),
            'author': forms.HiddenInput()
        }