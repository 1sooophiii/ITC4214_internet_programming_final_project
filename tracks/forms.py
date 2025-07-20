from django import forms
from .models import Track

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'genre', 'price', 'description', 'audio_file', 'image']
        # Customize the 'description' field with a larger textarea widget
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    # Apply Tailwind CSS classes to all input widgets
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full p-2 border rounded'})
