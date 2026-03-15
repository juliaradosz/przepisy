from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe, Comment, Ingredient, UserProfile


class UserRegisterForm(UserCreationForm):
    """Formularz rejestracji użytkownika."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    """Formularz edycji profilu użytkownika."""
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'favorite_cuisine']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class RecipeForm(forms.ModelForm):
    """Formularz dodawania/edycji przepisu."""
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'tags', 'description', 'instructions',
                  'servings', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class IngredientForm(forms.ModelForm):
    """Formularz składnika."""
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']


IngredientFormSet = forms.inlineformset_factory(
    Recipe, Ingredient,
    form=IngredientForm,
    extra=5,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class CommentForm(forms.ModelForm):
    """Formularz dodawania komentarza."""
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Napisz komentarz...'}),
            'rating': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)]),
        }


class SearchForm(forms.Form):
    """Formularz wyszukiwania przepisów."""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Szukaj przepisów...', 'class': 'form-control'})
    )
    category = forms.CharField(required=False)
    max_time = forms.ChoiceField(
        choices=[
            ('', 'Dowolny czas'),
            ('15', 'Do 15 min'),
            ('30', 'Do 30 min'),
            ('60', 'Do 1 godziny'),
            ('120', 'Do 2 godzin'),
        ],
        required=False,
    )
