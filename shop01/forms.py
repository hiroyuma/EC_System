from django import forms

class AccountCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
    
    user_id = forms.CharField(label='会員ID', max_length=128)
    password1 = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput(render_value=True))
    name = forms.CharField(label='名前', max_length=128)
    address = forms.CharField(label='住所', max_length=256)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('パスワードとパスワード（確認用）が違います。')

class AccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    user_id = forms.CharField(label='会員ID', max_length=128)
    password = forms.CharField(label='パスワード', max_length=256)