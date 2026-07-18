from django.contrib import admin
from . models import Product,ProductImage,MobileSpecification, Buying,CustomerQuery,ProductSize,SellerProfile


class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_name', 'is_approved', 'created_at','phone_number','gst_number') # നിങ്ങളുടെ മോഡലിലെ ഫീൽഡ് പേരുകൾ നൽകുക
    list_filter = ('is_approved',)
    search_fields = ('store_name', 'user__username')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class MobileSpecificationInline(admin.StackedInline):
    model = MobileSpecification
    can_delete = False
    verbose_name_plural = 'Mobile Phone Specifications (Fill only for Mobiles)'

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    # 🌟 ProductColorVariantInline ഇവിടെ നിന്നും ഒഴിവാക്കി
    inlines = [ProductImageInline, MobileSpecificationInline, ProductSizeInline]
    list_display = ['name', 'category', 'price', 'color_name', 'parent_product']
    list_filter = ['category', 'parent_product']
    search_fields = ['name']
    
admin.site.register(Product, ProductAdmin,SellerProfile)

@admin.register(Buying)
class BookingAdmin(admin.ModelAdmin):
    # അഡ്മിൻ പാനലിൽ വരിവരിയായി കാണിക്കേണ്ട കോളംസുകൾ
    list_display = ('customer_f_name','status', 'customer_s_name','customer_email', 'customer_phone','payment_method','total_amount', 'product', 'quantity', 'booking_date','del_address')
    # സെർച്ച് ചെയ്യാനുള്ള ബോക്സ്
    search_fields = ('customer_f_name', 'customer_email', 'customer_phone', 'product__name','status')
    # ഫിൽട്ടർ ചെയ്യാനുള്ള ഓപ്ഷൻ
    list_filter = ('booking_date', 'product','status')

@admin.register(CustomerQuery)
class CustomerQueryAdmin(admin.ModelAdmin):
    # അഡ്മിൻ പാനലിൽ ലിസ്റ്റ് ആയി കാണിക്കേണ്ട ഫീൽഡുകൾ
    list_display = ('name', 'email','message', 'created_at')
    
    # സെർച്ച് ചെയ്യാനുള്ള ഓപ്ഷൻ
    search_fields = ('name', 'email', 'message')
    
    # ഫിൽട്ടർ ചെയ്യാനുള്ള ഓപ്ഷൻ
    list_filter = ('created_at',)
    
    # ലിസ്റ്റിൽ പുതിയത് ആദ്യം കാണിക്കാൻ
    ordering = ('-created_at',)
