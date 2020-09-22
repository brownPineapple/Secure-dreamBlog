from django import forms
from tinymce import TinyMCE
from .models import Post, Comment
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail', 'categories', 'featured', 'previous_post', 'next_post')

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Type your comment',
        'id' : 'usercomment',
        'rows' : '4'
    }))
    class Meta:
        model = Comment
        fields = ('content', )


User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def claen(self, *args , **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Incorrect username or password !')
            if not user.check_password(password):
                raise forms.ValidateError('Incorrect username or password !')
            if not user.is_active:
                raise forms.ValidationError('Incorrect username or password !')
            return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email Address")

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password1',
            'password2',
        ]
