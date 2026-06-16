from django.contrib import admin
from .models import AccountUser, ShoppingCategory, ShoppingItem, ShoppingItemincart, ShoppingPurchase, ShoppingPurchasedetail, AdministratorAdmin

# Register your models here.
admin.site.register(AccountUser)
admin.site.register(ShoppingCategory)
admin.site.register(ShoppingItem)
admin.site.register(ShoppingItemincart)
admin.site.register(ShoppingPurchase)
admin.site.register(ShoppingPurchasedetail)
admin.site.register(AdministratorAdmin)