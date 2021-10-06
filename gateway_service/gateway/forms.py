from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    library = forms.ChoiceField()


class NewLibrary(forms.Form):
    city = forms.CharField(label='City:', widget=forms.TextInput(attrs={'class': 'form-control'}))


class NewBook(forms.Form):
    name = forms.CharField(label='Name:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    genre = forms.CharField(label='Genre:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.ChoiceField()


class NewLibraryBook(forms.Form):
    book = forms.ChoiceField()
    library = forms.ChoiceField()


class DeleteBook(forms.Form):
    book = forms.ChoiceField()
