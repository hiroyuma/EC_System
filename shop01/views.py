from django.shortcuts import render, redirect
from shop01.models import AccountUser
from django.views.generic import View, TemplateView
from shop01.forms import AccountForm, AccountCreateForm
# Create your views here.

class Toppage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'toppage.html')

class AccoutLogin(View):
    def get(self, request, *args, **kwargs):
        form = AccountForm()
        context = {
            'form':form,
        }
        return render(request, 'login.html', context)
    
    def post(self, request, *args, **kwargs):
        form = AccountForm(request.POST)
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

        return redirect('shop01:toppage')
    
class AccountCreate(View):
    def get(self, request, *args, **kwargs):
        form = AccountCreateForm()
        context = {
            'form':form
        }
        return render(request, 'register_user.html', context)
    
    def post(self, request, *args, **kwargs):
        form = AccountCreateForm(request.POST)
        context = {
            'form':form,
        }

        return render(request, 'register_user_comfirm.html', context)
    

    
class AccountComfirm(View):
    def get(self, request, *args, **kwargs):
        form = AccountForm()
        context = {
            'form':form,
        }
        return render(request, 'register_user_comfirm.html', context)
    
    def post(self, request, *args, **kwargs):
        form = AccountCreateForm(request.POST)
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

        context = {
            'name':new_user_data.name
        }

        return render(request, 'register_user_commit.html', context)