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
        fields = "__all__"
        widgets = {
            "likes": forms.HiddenInput(),
            "created": forms.HiddenInput(),
            "author": forms.HiddenInput()
        }