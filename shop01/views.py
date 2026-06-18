from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Max
from shop01.models import AccountUser, ShoppingItem, ShoppingItemincart, ShoppingPurchase, ShoppingPurchasedetail,ShoppingCategory
from django.views.generic import View, TemplateView
from shop01.forms import AdminPurchaseSearchForm,UserLoginForm, UserForm, KeywordForm, ItemNumForm, UpdataUserForm, ConfirmUserForm,AdminItemSearchForm, AdminItemForm
from shop01.models import AccountUser, ShoppingItem, ShoppingItemincart, ShoppingPurchase, ShoppingPurchasedetail, AdministratorAdmin
from django.views.generic import View, TemplateView
from shop01.forms import UserLoginForm, UserForm, KeywordForm, ItemNumForm, UpdataUserForm, ConfirmUserForm, AdminLoginForm
import random
import datetime
from django.utils import timezone
# Create your views here.

class Toppage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'shop01/toppage.html')
    
    def post(self, request, *args, **kwargs):
        return render(request, 'shop01/toppage.html')

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
            form = UserForm(request.POST)
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
        recommended_items = ShoppingItem.objects.filter(recommend=True)
        if not request.session.get('is_login'):
            recommended_items = ShoppingItem.objects.filter(recommend=True)
            form = KeywordForm()
            purchase_form = AdminPurchaseSearchForm()
            context = {
                'form': form,
                'purchase_form': purchase_form,
                'purchase_list': [],
                'recommended_items':recommended_items,
            }
            return render(request, 'main.html', context)
        
        user_id = request.session.get('user_id')
        user_info = AccountUser.objects.filter(user_id=user_id).first()
        form = KeywordForm()
        purchase_form = AdminPurchaseSearchForm(request.GET or None)
        purchase_list = ShoppingPurchase.objects.filter(
            user_id=user_id
        ).order_by('-purchase_id')
        if purchase_form.is_valid():
            purchase_id = purchase_form.cleaned_data.get('purchase_id')
            show_canceled = purchase_form.cleaned_data.get('show_canceled')

            if purchase_id:
                purchase_list = purchase_list.filter(purchase_id=purchase_id)

            if not show_canceled:
                purchase_list = purchase_list.filter(cancel=False)
        context = {
            'form': form,
            'purchase_form': purchase_form,
            'purchase_list': purchase_list,
            'user_name': user_info.name,
            'recommended_items':recommended_items,
        }
        return render(request, 'main.html', context)
    def post(self, request, *args, **kwargs):
        if not request.session.get('is_login'):
            return redirect('shop01:login')
        purchase_id = request.POST.get('purchase_id')
        user_id = request.session.get('user_id')
        purchase = get_object_or_404(
            ShoppingPurchase,
            purchase_id=purchase_id,
            user_id=user_id
        )
        if purchase.cancel:
            return redirect('shop01:main')
        with transaction.atomic():
            details = ShoppingPurchasedetail.objects.filter(purchase=purchase)
            for detail in details:
                item = detail.item
                item.stock += detail.amount
                item.save()
            purchase.cancel = True
            purchase.save()
        return redirect('shop01:main')
    
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


        discount = request.session.get("discount", 0)
        discounted_total = int(total_price * (100 - discount) / 100)
        abs_discount = abs(discount)


        context = {
            'cart_items':cart_items,
            'total_price':total_price,

            'discount': discount,
            'discounted_total': discounted_total,
            'abs_discount': abs_discount,

        }

        return render(request, 'cart.html', context)
    
def lottery_discount(request):
    if 'discount' in request.session:
        return redirect('shop01:cart')
    
    discount = random.randint(-100, 100)
    request.session['discount'] = discount
    return redirect('shop01:cart')

class PurchaseView(View):
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('shop01:login')

        user_info = AccountUser.objects.filter(user_id=user_id).first()
        cart_items = ShoppingItemincart.objects.filter(user_id=user_id)

        if not cart_items.exists():
            return redirect('shop01:cart')

        total_price = sum(item.amount * item.item.price for item in cart_items)
        
        discount = request.session.get("discount", 0)
        discounted_total = int(total_price * (100 - discount) / 100)
        abs_discount = abs(discount)

        context = {
            'user_info': user_info,
            'cart_items': cart_items,
            'total_price': total_price,
            
            'discount': discount,
            'discounted_total': discounted_total,
            'abs_discount': abs_discount,

        }
        return render(request, 'purchase.html', context)


class PurchaseCommitView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user_info = AccountUser.objects.filter(user_id=user_id).first()
        
        if not user_info:
            return redirect('shop01:login')

        custom_address = request.POST.get('destination')
        destination = custom_address if custom_address else user_info.address

        cart_items = ShoppingItemincart.objects.filter(user_id=user_id)
        if not cart_items.exists():
            return redirect('shop01:cart')
        
                # ✅ これをここに追加！！！
        discount = request.session.get("discount", 0)

        total_price = sum(item.amount * item.item.price for item in cart_items)
        discounted_total = int(total_price * (100 - discount) / 100)


        with transaction.atomic():
            last_purchase = ShoppingPurchase.objects.order_by('-purchase_id').first()
            new_purchase_id = (last_purchase.purchase_id + 1) if last_purchase else 1

            purchase = ShoppingPurchase.objects.create(
                purchase_id=new_purchase_id,
                destination=destination,
                booked_date=timezone.now(),
                cancel=False,
                user=user_info,
                
                discount=discount,
                total_price=discounted_total

            )

            last_detail = ShoppingPurchasedetail.objects.order_by('-purchase_detail_id').first()
            detail_id_counter = (last_detail.purchase_detail_id + 1) if last_detail else 1

            for cart_item in cart_items:
                ShoppingPurchasedetail.objects.create(
                    purchase_detail_id=detail_id_counter,
                    amount=cart_item.amount,
                    item=cart_item.item,
                    purchase=purchase
                )
                detail_id_counter += 1
                cart_item.item.stock -= cart_item.amount
                cart_item.item.save()

            cart_items.delete()

        return render(request, 'purchase_complete.html')


class PurchaseHistoryView(View):
    """購入した商品の履歴確認画面"""
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('shop01:login')
            
        purchases = ShoppingPurchase.objects.filter(user_id=user_id).prefetch_related(
            'shoppingpurchasedetail_set__item'
        ).order_by('-booked_date')

        context = {
            'purchases': purchases
        }
        return render(request, 'purchase_history.html', context)

class UpdateCart(View):
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        new_amount = request.POST.get('amount')

        items = ShoppingItemincart.objects.get(pk=item_id)

        items.amount = new_amount
        items.save()

        return redirect('shop01:cart')
    
class DeleteCart(View):
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')

        items = ShoppingItemincart.objects.get(pk=item_id)
        items.delete()

        return redirect('shop01:cart')
    
class Purchase(View):
    def get(self, request, *args, **kwargs):

        return redirect('shop01:cart')

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        amounts = request.POST.getlist('amount')
        item_ids = request.POST.getlist('item_id')
        cart_items = ShoppingItemincart.objects.filter(user_id=user_id)

        user = AccountUser.objects.filter(user_id=user_id).first()

        for item_id, amount in zip(item_ids, amounts):
            item = ShoppingItem.objects.filter(item_id=item_id).first()
            if item.stock > 0:
                item.stock = int(item.stock) - int(amount)
            else:
                item.stock = 0
            item.save()
        
        total_price = 0
        for item in cart_items:
            total_price += item.amount*item.item.price

        context = {
            'cart_items':cart_items,
            'total_price':total_price,
        }

        return render(request, 'purchase.html', context)

    
        

class AdminLogin(View):
    def get(self, request, *args, **kwargs):
        form = AdminLoginForm()
        context = {
            'form':form,
        }
        return render(request, 'admin_login.html', context)
        
    def post(self, request, *args, **kwargs):
        print("POSTの中身:", request.POST)
        form = AdminLoginForm(request.POST)
        print("バリデーション前")
        if not form.is_valid():
            print("a")
            print("エラー内容:", form.errors)
            account_list = AdministratorAdmin.objects.all()
            context = {
                'account_list':account_list,
                'form':form
            }
            return render(request, "admin_login.html", context)

        print("バリデーション通ったで")
        
        admin_id = form.cleaned_data.get('admin_id')
        password = form.cleaned_data.get('password')
        
        
        print("admin_id:", admin_id) 
        print("password:", password)


        admin_info = AdministratorAdmin.objects.filter(admin_id=admin_id, password=password).first()
        print("DBの中身:", admin_info)
        if admin_info is None:
            form.add_error(None,'会員IDまたはパスワードが間違っています')
            context={
                'form':form,
            }
            return render(request, 'admin_login.html', context)
        
        request.session['is_login'] = True
        request.session['admin_id'] = admin_id
        print("loginでsession:", request.session.get('is_login'))
        return redirect('shop01:admin_main')


class AdminMain(View):
    def get(self, request, *args, **kwargs):
        search_form = AdminItemSearchForm(request.GET or None)
        item_form = AdminItemForm()
        purchase_form = AdminPurchaseSearchForm(request.GET or None)

        items = ShoppingItem.objects.select_related('category').order_by('item_id')
        purchases = ShoppingPurchase.objects.select_related('user').order_by('-purchase_id')
        if search_form.is_valid():
            keyword = search_form.cleaned_data.get('keyword')
            category = search_form.cleaned_data.get('category')
            recommend_only = search_form.cleaned_data.get('recommend_only')

            if keyword:
                items = items.filter(name__icontains=keyword)

            if category:
                items = items.filter(category=category)

            if recommend_only:
                items = items.filter(recommend=True)
        if purchase_form.is_valid():
            purchase_id = purchase_form.cleaned_data.get('purchase_id')
            user_id = purchase_form.cleaned_data.get('user_id')
            cancel_status = purchase_form.cleaned_data.get('cancel_status')

            if purchase_id:
                purchases = purchases.filter(purchase_id=purchase_id)

            if user_id:
                purchases = purchases.filter(user_id__icontains=user_id)

            if cancel_status == '0':
                purchases = purchases.filter(cancel=False)
            elif cancel_status == '1':
                purchases = purchases.filter(cancel=True)

        context = {
            'search_form': search_form,
            'item_form': item_form,
            'purchase_form': purchase_form,
            'items': items,
            'purchases': purchases,
        }
        return render(request, 'admin_main.html', context)


class AdminItemCreate(View):

    def post(self, request, *args, **kwargs):
        search_form = AdminItemSearchForm()
        item_form = AdminItemForm(request.POST, request.FILES)
        items = ShoppingItem.objects.select_related('category').order_by('item_id')
        if not item_form.is_valid():
            context = {
                'search_form': search_form,
                'item_form': item_form,
                'items': items,
            }
            return render(request, 'admin_main.html', context)
        ShoppingItem.objects.create(
            item_id=item_form.cleaned_data['item_id'],
            category=item_form.cleaned_data['category'],
            name=item_form.cleaned_data['name'],
            manufacture=item_form.cleaned_data['manufacture'],
            color=item_form.cleaned_data['color'],
            price=item_form.cleaned_data['price'],
            stock=item_form.cleaned_data['stock'],
            recommend=item_form.cleaned_data['recommend'],
            image=item_form.cleaned_data.get('image'),
        )
        return redirect('shop01:admin_main')


class AdminItemDelete(View):

    def post(self, request, item_id, *args, **kwargs):
        item = get_object_or_404(ShoppingItem, pk=item_id)
        item.delete()
        return redirect('shop01:admin_main')


class AdminRecommendToggle(View):

    def post(self, request, item_id, *args, **kwargs):
        item = get_object_or_404(ShoppingItem, pk=item_id)
        item.recommend = not item.recommend
        item.save()
        return redirect('shop01:admin_main')

class AdminPurchaseCancel(View):

    def post(self, request, purchase_id, *args, **kwargs):
        purchase = get_object_or_404(ShoppingPurchase, pk=purchase_id)
        if purchase.cancel:
            return redirect('shop01:admin_main')
        with transaction.atomic():
            purchase_details = ShoppingPurchasedetail.objects.filter(purchase=purchase)
            for detail in purchase_details:
                item = detail.item
                item.stock += detail.amount
                item.save()
            purchase.cancel = True
            purchase.save()

        return redirect('shop01:admin_main')

class RandomCartAdd(View):
    def get(self, request, *args, **kwargs):
        return redirect("shop01:main")

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect("shop01:login")
        
        user = AccountUser.objects.filter(user_id=user_id).first()

        random_item = ShoppingItem.objects.filter(stock__gt=0).order_by('?').first()
        if random_item:
            randomamount = random.randint(1, random_item.stock)

            
            max_id = ShoppingPurchase.objects.aggregate(Max('purchase_id'))['purchase_id__max'] or 0
            
            new_purchase = ShoppingPurchase.objects.create(
                purchase_id = max_id + 1,
                destination = user.address,
                booked_date = datetime.datetime.now(), 
                user = user
            )

            random_item.stock -= randomamount
            random_item.save()

            max_detail_id = ShoppingPurchasedetail.objects.aggregate(Max('purchase_detail_id'))['purchase_detail_id__max'] or 0
            ShoppingPurchasedetail.objects.create(
                purchase_detail_id = max_detail_id + 1,
                amount = randomamount,
                item = random_item,
                purchase = new_purchase
            )
            total_price = randomamount * random_item.price

            context = {
                'item_name': random_item.name,
                "amount": randomamount,
                "total_price": total_price,
                "destination": user.address
            }
            
            return render(request, 'random_purchase_result.html', context)
        
        else:
            return redirect("shop01:main")