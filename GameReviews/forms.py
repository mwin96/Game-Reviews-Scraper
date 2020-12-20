from django import forms
from .models import Reviews
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class ReviewsListFormHelper(FormHelper):
    model = Reviews
    form_tag = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'first arg is the legend of the fieldset',
                'website',
                'title',
                'developer',
                'favorite_food',
                'notes'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )


class Subscribe(forms.Form):
    Email = forms.EmailField()
    def __str__(self):
        return self.Email