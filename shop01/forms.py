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
        
class UpdataUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
    
    user_id = forms.CharField(label='会員ID', max_length=128, widget=forms.TextInput(attrs={'readonly':'readonly'}))
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
        
class ConfirmUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
    
    user_id = forms.CharField(label='会員ID', max_length=128, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    password1 = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput())
    password2 = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput())
    name = forms.CharField(label='名前', max_length=128, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    address = forms.CharField(label='住所', max_length=256, widget=forms.TextInput(attrs={'readonly':'readonly'}))

class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    user_id = forms.CharField(label='会員ID', max_length=128)
    password = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput())

class KeywordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        
    category = forms.ModelChoiceField(ShoppingCategory.objects.order_by('category_id'), label='カテゴリ', to_field_name='category_id', empty_label='すべて', required=False,)
    item_keyword = forms.CharField(label='キーワード', max_length=128)

class ItemNumForm(forms.Form):

    stock = forms.ChoiceField(label='数量')
    def __init__(self, stock_num, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['stock'].choices = [(i, i) for i in range(1, stock_num + 1)]

class PurchaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    destination = forms.CharField(label='配送先', max_length=256)

    



        
    
    