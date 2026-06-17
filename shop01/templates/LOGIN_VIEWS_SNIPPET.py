# views.pyへの追加スニペット — ログイン成功後にお祝いフラグをセッションへ
#
# ① ログイン処理のviewでセッションにフラグをセット:
#
#   def login_view(request):
#       if request.method == 'POST':
#           # ... 認証処理 ...
#           if user is not None:
#               login(request, user)
#               request.session['just_logged_in'] = True   # ← 追加
#               request.session['user_name'] = user.username  # ← 追加
#               return redirect('shop01:main')
#
# ② login.htmlをレンダリングするviewでフラグを読み出してcontextに渡す:
#
#   def login_view(request):
#       just_logged_in = request.session.pop('just_logged_in', False)  # ← 追加(一度読んだら削除)
#       user_name = request.session.get('user_name', '')              # ← 追加
#       ...
#       return render(request, 'shop01/login.html', {
#           'form': form,
#           'just_logged_in': just_logged_in,   # ← 追加
#           'user_name': user_name,              # ← 追加
#       })
#
# これで login.html の {% if just_logged_in %} が有効になり、
# ページロード時に花火・コンフェッティ・ウェルカム画面が表示されます。
