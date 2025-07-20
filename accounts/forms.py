from django import forms
from .models import UserProfile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        fields = [
            'full_name', 'description', 'bio',
            'music_background', 'favorite_genres'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_field_classes = 'border border-gray-300 rounded-lg px-3 py-2 w-full'
        checkbox_classes = 'rounded text-emerald-500 focus:ring-emerald-500 ml-1'
        for field in ['full_name', 'description', 'bio', 'music_background', 'favorite_genres']:
            self.fields[field].widget.attrs.update({'class': text_field_classes})

# We are creating a customized class of the Django AuthenticationForm here
# in order to apply custom Tailwind styling in the inputs for Login
class TailwindAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full',
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full',
            'placeholder': 'Password'
        })

# We are creating a customized class of the Django UserCreationForm here
# in order to apply custom Tailwind styling in the inputs for Register
class TailwindUserCreationForm(UserCreationForm):
    is_seller = forms.BooleanField(
        required=False,
        label='Register as Seller',
        widget=forms.CheckboxInput(attrs={
            'class': 'rounded text-emerald-500 focus:ring-emerald-500 ml-1'
        }),
        help_text='Check to apply as a seller (you can change this later).',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full',
            'placeholder': 'Repeat Password'
        })
