from .models import Post
from django import forms
from users.models import User

class PostForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['id'] = 'files'
        self.fields['description'].widget.attrs['class'] = 'form-control'
   
        self.fields['description'].widget.attrs['placeholder'] = 'type description...'

    class Meta:
        model = Post                                                                        
        fields = ['image', 'description']


class ProfileForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['id'] = 'files'
        for fieldname in ['username', 'image', 'bio','email']:
            self.fields[fieldname].widget.attrs['class'] = 'form-control'


    class Meta:
        model = User                                                                        
        fields = ['image', 'email','username','bio']
        widgets = {
            'image': forms.FileInput(),
        }