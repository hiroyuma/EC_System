from django.shortcuts import render, redirect
from shop01.models import AccountUser
from django.views.generic import View, TemplateView
from shop01.forms import UserLoginForm, UserForm, KeywordForm
# Create your views here.

class Toppage(View):
    def get(self, request, *args, **kwargs):
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
            'form':form
        }
        return render(request, 'register_user.html', context)
    
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if not form.is_valid():
                return render(request, 'register_user.html', {
                    'form': form,
                })
        context = {
            'form':form,
        }
        return render(request, 'register_user_comfirm.html', context)
    
class UserComfirm(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        context = {
            'form':form,
        }
        return render(request, 'register_user_comfirm.html', context)
    
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
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
        
        form = UserForm(initial={
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
        
        form = UserForm(initial={
                    'user_id': user_info.user_id,
                    'name': user_info.name,
                    'address': user_info.address,
                })
        context = {
            'form': form
        }
        return render(request, 'update_user.html', context)
    
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if not form.is_valid():
                return render(request, 'update_user.html', {
                    'form': form,
                })
        context = {
            'form':form,
        }
        return render(request, 'update_user_comfirm.html', context)
    
class UpdateUserComfirm(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        context = {
            'form':form,
        }
        return render(request, 'update_user_comfirm.html', context)
    
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if not form.is_valid():
            form = UserForm()
            context = {
                'form':form
            }
            return render(request, "update_user.html", context)
        
        new_user_data = AccountUser()
        new_user_data.user_id = form.cleaned_data.get('user_id')
        new_user_data.password = form.cleaned_data.get('password2')
        new_user_data.name = form.cleaned_data.get('name')
        new_user_data.address = form.cleaned_data.get('address')

        new_user_data.save()

        form = UserForm(initial={
                    'user_id': new_user_data.user_id,
                    'name': new_user_data.name,
                    'address': new_user_data.address,
                })
        context = {
            'form': form
        }
        return render(request, 'update_user_commit.html', context)
    
class Withdraw(View):
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        user_info = AccountUser.objects.filter(user_id=user_id).first()
        context = {
            'user_name': user_info.name
        }
        return render(request, 'withdrawcomfrm.html', context)
    
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