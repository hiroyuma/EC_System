from django import forms
from shop01.models import ShoppingCategory,ShoppingItem

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

class AdminItemSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    keyword = forms.CharField(label='商品名', max_length=128, required=False)
    category = forms.ModelChoiceField(
        queryset=ShoppingCategory.objects.order_by('category_id'),
        label='カテゴリ',
        to_field_name='category_id',
        empty_label='すべて',
        required=False
    )
    recommend_only = forms.BooleanField(label='おすすめのみ', required=False)


class AdminItemForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
    item_id = forms.IntegerField(label='商品ID')
    category = forms.ModelChoiceField(
        queryset=ShoppingCategory.objects.order_by('category_id'),
        label='カテゴリ',
        to_field_name='category_id'
    )
    name = forms.CharField(label='商品名', max_length=128)
    manufacture = forms.CharField(label='メーカ名', max_length=32)
    color = forms.CharField(label='色', max_length=16)
    price = forms.IntegerField(label='価格', min_value=0)
    stock = forms.IntegerField(label='在庫数', min_value=0)
    recommend = forms.BooleanField(label='おすすめ', required=False)

    def clean_item_id(self):
        item_id = self.cleaned_data['item_id']
        if ShoppingItem.objects.filter(item_id=item_id).exists():
            raise forms.ValidationError('その商品IDはすでに登録されてる')
        return item_id

class AdminPurchaseSearchForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
    purchase_id = forms.IntegerField(label='注文ID', required=False)
    user_id = forms.CharField(label='会員ID', max_length=128, required=False)
    cancel_status = forms.ChoiceField(
        label='キャンセル状態',
        required=False,
        choices=(
            ('', 'すべて'),
            ('0', '未キャンセル'),
            ('1', 'キャンセル済み'),
        )
    )
class AdminLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    admin_id = forms.CharField(label='管理者ID', max_length=128)
    password = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput())
