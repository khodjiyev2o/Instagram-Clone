from .models import Post,Comment
from django import forms
from users.models import User

class CommmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['class'] = 'comment-box'
        self.fields['text'].widget.attrs['placeholder'] = 'Add a comment'

    class Meta:
        model = Comment                                                                        
        fields = ['text']
        
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