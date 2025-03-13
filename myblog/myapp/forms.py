from django import forms
from django.utils.text import slugify
from .models import BlogPost, Destination, BlogImage

class BlogImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False  # Set to False to allow empty images
    )

    class Meta:
        model = BlogImage
        fields = ['image', 'title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter image title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter image description'}),
        }


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['title', 'slug', 'location', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter destination title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique slug'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            slug = slugify(self.cleaned_data.get('title'))
        return slug


class BlogPostForm(forms.ModelForm):
    new_destination = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'placeholder': 'Or enter a new destination'})
    )

    class Meta:
        model = BlogPost
        fields = ['destination', 'title', 'slug', 'content', 'featured_image', 'category', 'author', 'background_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a title...'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-generated, you can edit'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write something amazing...'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-control'}),  # This will be updated dynamically
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author Name'}),
            'background_image': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Paste background image URL'}),
        }

    def __init__(self, *args, **kwargs):
        """Ensure that the latest destinations are always loaded in the dropdown."""
        super(BlogPostForm, self).__init__(*args, **kwargs)
        self.fields['destination'].queryset = Destination.objects.all()  # Load the latest destinations

    def clean(self):
        cleaned_data = super().clean()
        destination = cleaned_data.get('destination')
        new_destination = cleaned_data.get('new_destination')

        if not destination and not new_destination:
            raise forms.ValidationError("Please select an existing destination or enter a new one.")

        return cleaned_data
