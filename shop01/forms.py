from django import forms
from shop01.models import ShoppingCategory

class UserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
    
    user_id = forms.CharField(label='会員ID', max_length=128)
    password1 = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput())
    password2 = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput())
    name = forms.CharField(label='名前', max_length=128)
    address = forms.CharField(label='住所', max_length=256)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('パスワードとパスワード（確認用）が違います。')

class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    user_id = forms.CharField(label='会員ID', max_length=128)
    password = forms.CharField(label='パスワード', max_length=256)

class KeywordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        
    category = forms.ModelChoiceField(ShoppingCategory.objects.order_by('category_id'), label='カテゴリ', to_field_name='category_id', empty_label='すべて')
    item_keyword = forms.CharField(label='キーワード', max_length=128)
    