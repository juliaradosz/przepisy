from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe, Comment, Ingredient, Step, UserProfile, Category, Event


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
        fields = ['title', 'category', 'tags', 'description',
                  'servings', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa przepisu'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Krotki opis przepisu'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'np. 4'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class IngredientForm(forms.ModelForm):
    """Formularz składnika."""
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']


IngredientFormSet = forms.inlineformset_factory(
    Recipe, Ingredient,
    form=IngredientForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class StepForm(forms.ModelForm):
    """Formularz pojedynczego kroku."""
    class Meta:
        model = Step
        fields = ['order', 'text']
        widgets = {
            'order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Opis kroku...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hidden `order` is auto-filled by the template, so Django considers
        # every trailing extra form "changed" and would otherwise validate
        # `text` as required. Make text optional and filter empties in the view.
        self.fields['text'].required = False


StepFormSet = forms.inlineformset_factory(
    Recipe, Step,
    form=StepForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class CategoryForm(forms.ModelForm):
    """Formularz dodawania kategorii."""
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa kategorii'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Opis (opcjonalnie)'}),
        }


class CommentForm(forms.ModelForm):
    """Formularz dodawania komentarza."""
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Napisz komentarz...'}),
            'rating': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)]),
        }


class EventForm(forms.ModelForm):
    """Formularz tworzenia/edycji wydarzenia."""
    class Meta:
        model = Event
        fields = ['name', 'date', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np. Wielkanoc 2026'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Opis (opcjonalnie)'}),
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
