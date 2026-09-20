from django import forms

MIN_MESSAGE_LENGTH = 10

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField(required=False, min_value=1, max_value=5)

    def clean_message(self):
        message = self.cleaned_data.get("message", "").strip()
        if len(message) < MIN_MESSAGE_LENGTH:
            raise forms.ValidationError(f"Message must be at least {MIN_MESSAGE_LENGTH} characters long.")
        return message