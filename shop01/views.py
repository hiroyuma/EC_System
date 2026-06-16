from django.shortcuts import render, redirect, get_object_or_404
from shop01.models import AccountUser, ShoppingItem, ShoppingItemincart, ShoppingPurchase, ShoppingPurchasedetail
from django.views.generic import View, TemplateView
from shop01.forms import UserLoginForm, UserForm, KeywordForm, ItemNumForm, UpdataUserForm, ConfirmUserForm
# Create your views here.

class Toppage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'toppage.html')
    
    def post(self, request, *args, **kwargs):
        return render(request, 'toppage.html')

class UserLogin(View):
    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        context = {
            'form':form,
        }
        return render(request, 'login.html', context)
    
    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if not form.is_valid():
            accout_list = AccountUser.objects.all()
            context = {
                'account_list':accout_list,
                'form':form
            }
            return render(request, "login.html", context)
        
        user_id = form.cleaned_data.get('user_id')
        password = form.cleaned_data.get('password')

        user_info = AccountUser.objects.filter(user_id=user_id, password=password).first()

        if user_info is None:
            form.add_error(None,'会員IDまたはパスワードが間違っています')
            context={
                'form':form,
            }
            return render(request, 'login.html', context)
        
        request.session['is_login'] = True
        request.session['user_id'] = user_id

        return redirect('shop01:main')
    
class UserCreate(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        context = {
            'form':form,
            'password_num':'*'*6
        }
        return render(request, 'register_user.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ConfirmUserForm(request.POST)
        if not form.is_valid():
                form = UserForm()
                return render(request, 'register_user.html', {
                    'form': form,
                })
        
        password_num = len(request.POST.get('password1'))
        print(password_num)

        context = {
            'form':form,
            'password_num':'*'*password_num,
        }
        return render(request, 'register_user_confirm.html', context)
    
class UserConfirm(View):
    def get(self, request, *args, **kwargs):
        form = ConfirmUserForm()
        context = {
            'form':form,
            'password_num':'*'*6
        }
        return render(request, 'register_user_confirm.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ConfirmUserForm(request.POST)
        if not form.is_valid():
            user_list = AccountUser.objects.all()
            context = {
                'user_list':user_list,
                'form':form
            }
            return render(request, "login.html", context)
        
        new_user_data = AccountUser()
        new_user_data.user_id = form.cleaned_data.get('user_id')
        new_user_data.password = form.cleaned_data.get('password2')
        new_user_data.name = form.cleaned_data.get('name')
        new_user_data.address = form.cleaned_data.get('address')


        
        if AccountUser.objects.filter(user_id=new_user_data.user_id).exists():
            form.add_error('user_id', 'この会員IDは既に登録済みです')
            return render(request, 'register_user.html', {
                'form': form,
            })

        new_user_data.save()

        request.session['is_login'] = True
        request.session['user_id'] = new_user_data.user_id

        context = {
            'name':new_user_data.name
        }

        return render(request, 'register_user_commit.html', context)
    
class UserLogout(View):
    def get(self, request):
        request.session.flush()
        return redirect('shop01:login')
    
class UserDetail(View):
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user_info = AccountUser.objects.filter(user_id=user_id).first()
        
        form = ConfirmUserForm(initial={
                    'user_id': user_info.user_id,
                    'password1': '表示なし',
                    'name': user_info.name,
                    'address': user_info.address,
                })
        context = {
            'form': form
        }
        return render(request, 'user_info.html', context)
    
class UpdataUser(View):
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user_info = AccountUser.objects.filter(user_id=user_id).first()
        
        form = UpdataUserForm(initial={
                    'user_id': user_info.user_id,
                    'name': user_info.name,
                    'address': user_info.address,
                })
        context = {
            'form': form
        }
        return render(request, 'update_user.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ConfirmUserForm(request.POST)
        if not form.is_valid():
                return render(request, 'update_user.html', {
                    'form': form,
                })
        password_num = len(request.POST.get('password1'))

        context = {
            'form':form,
            'password_num':'*'*password_num,
        }
        return render(request, 'update_user_confirm.html', context)
    
class UpdateUserConfirm(View):
    def get(self, request, *args, **kwargs):
        form = ConfirmUserForm()
        context = {
            'form':form,
            'password_num':'*'*6
        }
        return render(request, 'update_user_confirm.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ConfirmUserForm(request.POST)
        if not form.is_valid():
            form = ConfirmUserForm()
            context = {
                'form':form
            }
            return render(request, "update_user.html", context)
        
        user_id = request.session.get('user_id')
        
        new_user_data = AccountUser.objects.filter(user_id=user_id).first()
        new_user_data.password = form.cleaned_data.get('password2')
        new_user_data.name = form.cleaned_data.get('name')
        new_user_data.address = form.cleaned_data.get('address')

        new_user_data.save()

        password_num = len(form.cleaned_data.get('password2'))

        form = ConfirmUserForm(initial={
                    'user_id': user_id,
                    'name': new_user_data.name,
                    'address': new_user_data.address,
                })
        context = {
            'form': form,
            'password_num':'*'*password_num,
        }
        return render(request, 'update_user_commit.html', context)
    
class Withdraw(View):
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user_info = AccountUser.objects.filter(user_id=user_id).first()
        context = {
            'user_name': user_info.name
        }
        return render(request, 'withdrawconfrm.html', context)
    
class withdrawCommit(View):
    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user_info = AccountUser.objects.filter(user_id=user_id).first()
        context = {
            'user_name': user_info.name
        }   
        if user_info:
            user_info.delete()

        request.session.flush()
        return render(request, 'withdrawcommit.html', context)

class SearchItem(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('is_login'):
            form = KeywordForm()
            context = {
                'form': form,
                }
            return render(request, 'main.html', context)
        
        user_id = request.session.get('user_id')
        user_info = AccountUser.objects.filter(user_id=user_id).first()
        form = KeywordForm()
        context = {
            'form': form,
            'user_name': user_info.name
        }
        return render(request, 'main.html', context)
    
class SearchResult(View):
    def get(self, request, *args, **kwargs):
        form = KeywordForm(request.GET)
        if not form.is_valid():
            return redirect('shop01:main')

        category = form.cleaned_data.get('category')
        keyword = form.cleaned_data.get('item_keyword')

        search_result = ShoppingItem.objects.filter(name__icontains=keyword)
        if category:
            search_result = search_result.filter(category=category)

        context = {
            'category':category,
            'keyword':keyword,
            'search_result':search_result,
        }
        return render(request, 'search_result.html', context)
    
class ItemDetail(View):
    def get(self, request, item_id, *args, **kwargs):
        
        item = get_object_or_404(ShoppingItem, pk=item_id)

        form = ItemNumForm(stock_num=item.stock)

        context = {
            'item': item,
            'form': form
        }
        return render(request, 'item_detail.html', context)
    
    def post(self, request, item_id, *args, **kwargs):
        
        item_id = request.POST.get('item_id')
        stock = request.POST.get('stock')
        user_id = request.session.get('user_id')

        item = get_object_or_404(ShoppingItem, pk=item_id)
        user = get_object_or_404(AccountUser, pk=user_id)
        
        cart_item = ShoppingItemincart()
        cart_item.amount = stock
        cart_item.item = item
        cart_item.user = user

        cart_item.save()

        return redirect('shop01:cart')



class Cart(View):
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        cart_items = ShoppingItemincart.objects.filter(user_id=user_id)

        total_price = 0
        for item in cart_items:
            total_price += item.amount*item.item.price

        context = {
            'cart_items':cart_items,
            'total_price':total_price,
        }

        return render(request, 'cart.html', context)



    # def post(self, request, *args, **kwargs):

    #     context = {}
    #     return render(request, 'cart.html', context)


