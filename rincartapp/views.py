from django.shortcuts import render, redirect, get_object_or_404
from .models import Product  ,Buying ,Wishlist,CustomerQuery
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# ================= 1. PAGE VIEWS (FILTERS BY CATEGORY) =================

# Home / All Products Page
def home_page(request):
    all_products = Product.objects.all()
    wishlist_ids = []
    
    if request.user.is_authenticated:
        # യൂസറുടെ വിഷ്‌ലിസ്റ്റിലുള്ള പ്രൊഡക്റ്റ് ഐഡികൾ മാത്രം എടുക്കുന്നു
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    return render(request, 'home.html', {'products': all_products, 'wishlist_ids': wishlist_ids})

# Fashion Page Only
from django.shortcuts import render
from .models import Product, Wishlist

def fashion_page(request):
    # category 'fashion' ഉള്ള പ്രൊഡക്റ്റുകൾ എടുക്കുന്നു, ഒപ്പം സൈസ് വേരിയന്റുകളും പ്രീഫെച്ച് ചെയ്യുന്നു
    products = Product.objects.filter(category='fashion').prefetch_related('variant')
    
    selected_size = request.GET.get('size', None)
    selected_price = request.GET.get('price', None)

    # 1. Budget Range Filter
    if selected_price:
        if selected_price == 'under_500':
            products = products.filter(price__lt=500)
        elif selected_price == '500_1000':
            products = products.filter(price__gte=500, price__lte=1000)
        elif selected_price == '1000_2000':
            products = products.filter(price__gte=1000, price__lte=2000)
        elif selected_price == 'above_2000':
            products = products.filter(price__gt=2000)

    # 2. Size Filter (Django ORM വഴി മാറ്റിയത്)
    if selected_size:
        # ProductSize മോഡലിലെ size ഫീൽഡ് കേസ് ഇൻസെൻസിറ്റീവ് ആയി ഫിൽട്ടർ ചെയ്യുന്നു
        products = products.filter(variant__size__iexact=selected_size)

    # 3. Wishlist Logic
    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        
    context = {
        'products': products,
        'selected_size': selected_size,
        'selected_price': selected_price,
        'wishlist_ids': wishlist_ids
    }
    return render(request, 'fashion.html', context)

# Mobiles Page Only
def mobile_page(request):
    mobile_items = Product.objects.filter(category='mobile')
    selected_price = request.GET.get('price', None)
    
    # 🌟 ആദ്യമേ ഡിഫോൾട്ട് ആയി എല്ലാ മൊബൈലുകളും ഈ വേരിയബിളിലേക്ക് വെക്കുക
    
    products = mobile_items 
    

    if selected_price:
        if selected_price == 'under_2000':
            products = mobile_items.filter(price__lt=2000)
        elif selected_price == '2000_10000':
            products = mobile_items.filter(price__gte=2000, price__lte=10000)
        elif selected_price == '10000_20000':
            products = mobile_items.filter(price__gte=10000, price__lte=20000)
        elif selected_price == '20000_30000':
            products = mobile_items.filter(price__gte=20000, price__lte=30000)
        elif selected_price == '30000_40000':
            products = mobile_items.filter(price__gte=30000, price__lte=40000)
        elif selected_price == 'above_40000':
            products = mobile_items.filter(price__gt=40000)
    wishlist_ids = []
    
    if request.user.is_authenticated:
        # യൂസറുടെ വിഷ്‌ലിസ്റ്റിലുള്ള പ്രൊഡക്റ്റ് ഐഡികൾ മാത്രം എടുക്കുന്നു
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    context = {                       
        'selected_price': selected_price,
        'productss': products,  # 🌟 ഇവിടെ ഫിൽട്ടർ ചെയ്ത 'products' തന്നെ കൊടുക്കുക!
        'wishlist_ids': wishlist_ids
    }
    return render(request, 'mobile.html', context)

# Beauty Page Only
def beauty_page(request):
    beauty_items = Product.objects.filter(category='beauty')
    selected_price = request.GET.get('price', None)
    products=beauty_items

    if selected_price:
        if selected_price == 'under_500':
            products = beauty_items.filter(price__lt=500) # ₹500-ൽ താഴെ മാത്രം
        elif selected_price == '500_1000':
            products = beauty_items.filter(price__gte=500, price__lte=1000) # ₹500 നും ₹1000 നും ഇടയിൽ
        elif selected_price == '1000_2000':
            products = beauty_items.filter(price__gte=1000, price__lte=2000) # ₹1000 നും ₹2000 നും ഇടയിൽ
        elif selected_price == 'above_2000':
            products = beauty_items.filter(price__gt=2000)
    wishlist_ids = []
    
    if request.user.is_authenticated:
        # യൂസറുടെ വിഷ്‌ലിസ്റ്റിലുള്ള പ്രൊഡക്റ്റ് ഐഡികൾ മാത്രം എടുക്കുന്നു
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    context={
        'selected_price': selected_price,
        'productss': products,
        'wishlist_ids': wishlist_ids

    }
    return render(request,'beauty.html',context)

# Electronics Page Only
def electronics_page(request):
    electronic_items = Product.objects.filter(category='electronic')
    selected_price = request.GET.get('price', None)

    if selected_price:
        if selected_price == 'under_500':
            products = electronic_items.filter(price__lt=500) # ₹500-ൽ താഴെ മാത്രം
        elif selected_price == '500_1000':
            products = electronic_items.filter(price__gte=500, price__lte=1000) # ₹500 നും ₹1000 നും ഇടയിൽ
        elif selected_price == '1000_2000':
            products = electronic_items.filter(price__gte=1000, price__lte=2000) # ₹1000 നും ₹2000 നും ഇടയിൽ
        elif selected_price == 'above_2000':
            products = electronic_items.filter(price__gt=2000)
    wishlist_ids = []
    
    if request.user.is_authenticated:
        # യൂസറുടെ വിഷ്‌ലിസ്റ്റിലുള്ള പ്രൊഡക്റ്റ് ഐഡികൾ മാത്രം എടുക്കുന്നു
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    context={
        'selected_price': selected_price,
        'productss': electronic_items,
        'wishlist_ids': wishlist_ids
    }
    return render(request,'electronics.html',context)

# Home Appliances Page
def home_appliances_page(request):
    home_appliance_items = Product.objects.filter(category='home_appliance')
    selected_price = request.GET.get('price', None)

    if selected_price:
        if selected_price == 'under_500':
            products = home_appliance_items.filter(price__lt=500) # ₹500-ൽ താഴെ മാത്രം
        elif selected_price == '500_1000':
            products = home_appliance_items.filter(price__gte=500, price__lte=1000) # ₹500 നും ₹1000 നും ഇടയിൽ
        elif selected_price == '1000_2000':
            products = home_appliance_items.filter(price__gte=1000, price__lte=2000) # ₹1000 നും ₹2000 നും ഇടയിൽ
        elif selected_price == 'above_2000':
            products = home_appliance_items.filter(price__gt=2000)
    wishlist_ids = []
    
    if request.user.is_authenticated:
        # യൂസറുടെ വിഷ്‌ലിസ്റ്റിലുള്ള പ്രൊഡക്റ്റ് ഐഡികൾ മാത്രം എടുക്കുന്നു
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    context={
        'selected_price': selected_price,
        'productss': home_appliance_items,
        'wishlist_ids': wishlist_ids
    }
    return render(request,'home_appliances.html',context)

# Toys Page
def toys_page(request):
    toy_items = Product.objects.filter(category='toy')
    selected_price = request.GET.get('price', None)

    if selected_price:
        if selected_price == 'under_500':
            products = toy_items.filter(price__lt=500) # ₹500-ൽ താഴെ മാത്രം
        elif selected_price == '500_1000':
            products = toy_items.filter(price__gte=500, price__lte=1000) # ₹500 നും ₹1000 നും ഇടയിൽ
        elif selected_price == '1000_2000':
            products = toy_items.filter(price__gte=1000, price__lte=2000) # ₹1000 നും ₹2000 നും ഇടയിൽ
        elif selected_price == 'above_2000':
            products = toy_items.filter(price__gt=2000)
    wishlist_ids = []
    
    if request.user.is_authenticated:
        # യൂസറുടെ വിഷ്‌ലിസ്റ്റിലുള്ള പ്രൊഡക്റ്റ് ഐഡികൾ മാത്രം എടുക്കുന്നു
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    context={
        'selected_price': selected_price,
        'productss': toy_items,
        'wishlist_ids': wishlist_ids
    }
    return render(request,'toys.html',context)
# ================= 2. UNIFIED CART SYSTEM =================

# Since all items are now in the 'Product' model, we only need ONE clean cart function!
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    # Convert ID to string because session keys must be strings
    p_id = str(product_id)
    
    # Increment quantity
    cart[p_id] = cart.get(p_id, 0) + 1
    
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
 
    for item_key, quantity in cart.items():
        # Strip prefixes if old session data still contains 'prod_' or 'fash_'
        clean_id = item_key.replace('prod_', '').replace('fash_', '').replace('mobi_', '').replace('beau_', '').replace('toy_', '').replace('elect_', '').replace('homeappl_', '')
        
        try:
            # Everything is fetched safely from the Product table
            product = Product.objects.get(id=clean_id)
        except Product.DoesNotExist:
            continue  # Skip item if it was deleted from DB

           
        subtotal = product.price * quantity
        total_price += subtotal
        
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    
        
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


# ================= 3. PRODUCT DETAIL & RECOMMENDATION =================


def product_detail_page(request, product_id):
    # നിലവിൽ കാണുന്ന പ്രൊഡക്റ്റ് വേരിയന്റ് എടുക്കുന്നു
    product = get_object_or_404(Product, id=product_id)
    
    size_variants = product.variant.all() 
    # 🌟 1. മെയിൻ പ്രൊഡക്റ്റ് ഏതാണെന്ന് കണ്ടെത്തുന്നു (Parent)
    main_product = product.parent_product if hasattr(product, 'parent_product') and product.parent_product else product
    
    # 🌟 2. ശരിയായ ലോജിക് ഉപയോഗിച്ച് എല്ലാ കളറുകളും ഫിൽട്ടർ ചെയ്യുന്നു
    color_variants = Product.objects.filter(Q(id=main_product.id) | Q(parent_product=main_product))
    
    # Delivery Date Math
    delivery_date = datetime.date.today() + datetime.timedelta(days=4)
    formatted_delivery = delivery_date.strftime("%A, %b %d")

    # Math-Based Discount Calculation
    discount_percentage = 0
    if product.original_price and product.original_price > product.price:
        savings = product.original_price - product.price
        discount_percentage = round((savings / product.original_price) * 100)

    # സമാനമായ മറ്റ് പ്രൊഡക്റ്റുകൾ (നിലവിലെ പ്രൊഡക്റ്റിന്റെ ഗ്രൂപ്പിനെ ഒഴിവാക്കിക്കൊണ്ട്)
    similar_products = Product.objects.filter(category=product.category).exclude(
        Q(id=main_product.id) | Q(parent_product=main_product)
    )[:4]
    
    wishlist_ids = []
    if request.user.is_authenticated:
        # യൂസറുടെ വിഷ്‌ലിസ്റ്റിലുള്ള പ്രൊഡക്റ്റ് ഐഡികൾ മാത്രം എടുക്കുന്നു
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    
    context = {
        'product': product,
        'delivery_date': formatted_delivery,
        'discount_percentage': discount_percentage,
        'similar_products': similar_products,
        'color_variants': color_variants,
        'wishlist_ids': wishlist_ids,
        'size_variants': size_variants,
    }
    return render(request, 'product_detail.html', context)
def return_policy_view(request):
    return render(request, 'return_policy.html')

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        # Example if using session-based cart:
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart
            
        # Example if using Model-based cart:
        # cart_item = CartItem.objects.filter(user=request.user, product_id=product_id)
        # cart_item.delete()
        
    return redirect('cart_view') # Change 'cart' to whatever name matches your cart route



@login_required
def dashboard_view(request):
    return render(request, 'home.html')


@login_required
def setup_view(request):
    if request.POST:
        # Get the name entered in the form
        first_name = request.POST.get('first_name')
        
        # Save it to the logged-in user profile
        request.user.first_name = first_name
        request.user.save()
        
        # Take them to the dashboard once they are done
        return redirect('home')
        
    return render(request, 'setup.html')


def sign_up(request):
    if request.method == 'POST':
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')
        retype_password_input = request.POST.get('retype_password') # പുതിയ ഇൻപുട്ട് വാല്യൂ എടുക്കുന്നു
        
        # 🔍 രണ്ടു പാസ്‌വേഡും ഒന്നുതന്നെയാണോ എന്ന് പരിശോധിക്കുന്നു
        if password_input != retype_password_input:
            messages.error(request, "Passwords do not match! Please try again.")
            return render(request, 'sign_up.html')
            
        # ഇമെയിൽ ഓൾറെഡി ഡാറ്റാബേസിൽ ഉണ്ടോ എന്ന് നോക്കുന്നു
        if User.objects.filter(email=email_input).exists():
            messages.error(request, "This email is already registered. Please sign in.")
            return render(request, 'sign_up.html')
            
        # യൂസർനെയിം ജനറേറ്റ് ചെയ്യുന്നു
        generated_username = email_input.split('@')[0]
        if User.objects.filter(username=generated_username).exists():
            generated_username = f"{generated_username}{random.randint(10, 99)}"

        # പുതിയ യൂസറെ ഡാറ്റാബേസിലേക്ക് സേവ് ചെയ്യുന്നു
        new_user = User.objects.create_user(
            username=generated_username,
            email=email_input,
            password=password_input
        )
        
        login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, "Account created successfully! Welcome to RinCart.")
        return redirect('home')
        
    return render(request, 'sign_up.html')


# 🔑 2. SIGN IN VIEW (ഓൾറെഡി അക്കൗണ്ട് ഉള്ളവർക്ക് ലോഗിൻ ചെയ്യാൻ)
def sign_in(request):
    if request.method == 'POST':
        email_input = request.POST.get('username')  # HTML-ൽ name="username" ആയതുകൊണ്ട്
        password_input = request.POST.get('password')
        
        try:
            # ഇമെയിൽ വഴി യൂസറെ കണ്ടുപിടിക്കുന്നു
            user_obj = User.objects.get(email=email_input)
            
            # പാസ്‌വേഡ് കറക്റ്റ് ആണോ എന്ന് നോക്കുന്നു
            if user_obj.check_password(password_input):
                login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')
                
                # ഫസ്റ്റ് നെയിം സെറ്റ് ചെയ്തിട്ടില്ലെങ്കിൽ പ്രൊഫൈൽ സെറ്റപ്പിലേക്ക് വിടുന്നു
                if not user_obj.first_name:
                    return redirect('continue-setup')
                    
                messages.success(request, "Welcome back!")
                return redirect('home')
            else:
                messages.error(request, "Incorrect password. Please try again.")
                return render(request, 'sign_in.html')
                
        except User.DoesNotExist:
            # ഇമെയിൽ ഡാറ്റാബേസിൽ ഇല്ലെങ്കിൽ സൈൻ അപ്പ് ചെയ്യാൻ പറയുന്നു
            messages.error(request, "Account not found with this email. Please sign up first.")
            return render(request, 'sign_in.html')
            
    return render(request, 'sign_in.html')

# 4. ഡീൽസ് പേജിൽ എപ്പോഴും കാണിക്കാൻ (Deals View)
def deals_page_view(request):
    products = Product.objects.all()
    active_orders = []
    bought_product_ids = []

    if request.user.is_authenticated:
        # 🌟 പ്രധാന മാറ്റം: ഇവിടെ status='Active' എന്ന് നിർബന്ധമായും ചേർക്കണം!
        # എന്നാലേ ക്യാൻസൽ ചെയ്ത ഓർഡറുകൾ മാറി, നിലവിൽ ആക്റ്റീവ് ആയ പുതിയ ഓർഡർ മുകളിൽ വരൂ.
        active_orders = Buying.objects.filter(user=request.user, status='Active').order_by('-id')
        
         
            
        # കസ്റ്റമർ നിലവിൽ വാങ്ങി വെച്ചിരിക്കുന്ന (Active ആയ) പ്രൊഡക്റ്റുകൾക്ക് മാത്രം 'Already Booked' കാണിക്കാൻ
        bought_product_ids = active_orders.values_list('product_id', flat=True)

    context = {
        'products': products,
        'active_orders': active_orders, 
        'bought_product_ids': bought_product_ids, 
    }
    return render(request, 'deals.html', context)

@login_required(login_url='sign_in')
def order_tracking_page(request, buying_id): # 🌟 product_id മാറ്റി buying_id ആക്കി
    # 🛒 പ്രൊഡക്റ്റിന് പകരം ഓർഡർ ചെയ്ത 'Buying' ഒബ്ജക്റ്റ് എടുക്കുന്നു
    order = get_object_or_404(Buying, id=buying_id, user=request.user)
    
    # 🚚 Delivery Date & Time Math
    delivery_date = datetime.date.today() + datetime.timedelta(days=4)
    formatted_delivery = delivery_date.strftime("%A, %b %d")
    arrived_time = "10:00 AM - 05:00 PM" 

    context = {
        'order': order,  # 🌟 പ്രൊഡക്റ്റിന് പകരം ഫുൾ ഓർഡർ വിവരങ്ങൾ പാസ്സ് ചെയ്യുന്നു
        'delivery_date': formatted_delivery,
        'arrived_time': arrived_time,
    }
    return render(request, 'order_tracking.html', context)


@login_required(login_url='sign_in')
def cancel_order_view(request, buying_id):
    # 1. ക്യാൻസൽ ചെയ്യേണ്ട ആക്റ്റീവ് ഓർഡർ കണ്ടെത്തുന്നു
    order_query = Buying.objects.filter(id=buying_id, user=request.user, status='Active')
    
    if order_query.exists():
        cancelled_order = order_query.first() # 🌟 ഓർഡർ ഒബ്ജക്റ്റ് എടുക്കുന്നു
        
        # 2. സ്റ്റാറ്റസ് 'Cancelled' എന്ന് അപ്ഡേറ്റ് ചെയ്യുന്നു
        order_query.update(status='Cancelled')
        
        # 3. ക്യാൻസൽ ചെയ്ത പ്രൊഡക്റ്റിന്റെ വിവരങ്ങൾ കൺഫേം പേജിലേക്ക് അയക്കുന്നു 🌟
        context = {
            'product': cancelled_order.product,
            'price': cancelled_order.total_amount, # അല്ലെങ്കിൽ product.price നൽകാം
            'quantity': cancelled_order.quantity
        }
        return render(request, 'cancel_confirm.html', context)
    else:
        messages.warning(request, "Order not found or already cancelled.")
        return redirect('view_deals')

def cancellation(request,buying_id):
    order = get_object_or_404(Buying, id=buying_id, user=request.user)
    context={
        'order': order
    }
    return render(request,'cancellation.html',context)

from django.views.decorators.csrf import ensure_csrf_cookie

@login_required(login_url='sign_in')
@ensure_csrf_cookie
def checkout_view(request, product_id=None):
    cart_items = []
    cod_allowed = True
    is_single_product = False

    # 🛒 കേസ് 1: നേരിട്ട് "Buy Now" വഴി വരുമ്പോൾ
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        quantity = 1
        subtotal = product.price * quantity
        is_single_product = True
        
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        
        if not getattr(product, 'is_cod_available', True):
            cod_allowed = False

    # 🛒 കേസ് 2: കാർട്ടിൽ നിന്നാണ് വരുന്നതെങ്കിൽ
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('cart_view')

        for item_key, quantity in cart.items():
            clean_id = item_key.replace('prod_', '').replace('fash_', '').replace('mobi_', '').replace('beau_', '').replace('toy_', '').replace('elect_', '').replace('homeappl_', '')
            try:
                product = Product.objects.get(id=clean_id)
                subtotal = product.price * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal,
                })
                
                if not getattr(product, 'is_cod_available', True):
                    cod_allowed = False
                    
            except Product.DoesNotExist:
                continue

    # 🔢 ടാക്സും ആകെ തുകയും ഇവിടെ കണക്കാക്കുന്നു (ഇത് പേജ് ലോഡ് ചെയ്യുമ്പോഴും സബ്മിറ്റ് ചെയ്യുമ്പോഴും വർക്ക് ചെയ്യും)
    grand_original_total = 0
    grand_discounted_total = 0  # ഇത് തന്നെയാണ് ടാക്സിന് മുൻപുള്ള ടോട്ടൽ പ്രൈസ് (Subtotal)
    grand_tax_amount = 0
    grand_final_amount = 0

    for item in cart_items:
        prod = item['product']
        qty = item['quantity']

        orig_price = prod.original_price if prod.original_price else prod.price
        original_total = float(orig_price) * qty
        discounted_total = float(prod.price) * qty
        
        # ടാക്സ് റേറ്റ് മോഡലിൽ ഇല്ലെങ്കിൽ 0 ആയി എടുക്കും
        tax_rate = getattr(prod, 'tax_rate', 0)
        tax_amount = (discounted_total * float(tax_rate)) / 100
        final_amount = discounted_total + tax_amount

        # ഐറ്റത്തിലേക്ക് ടാക്സ് ഡാറ്റ കൂടി ആഡ് ചെയ്യുന്നു (ആവശ്യമെങ്കിൽ ടെംപ്ലേറ്റിൽ കാണിക്കാം)
        item['tax_amount'] = tax_amount
        item['final_amount'] = final_amount

        grand_original_total += original_total
        grand_discounted_total += discounted_total
        grand_tax_amount += tax_amount
        grand_final_amount += final_amount

    # 📦 ഓർഡർ കൺഫേം ചെയ്യുമ്പോൾ (POST METHOD)
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        s_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        selected_payment = request.POST.get('payment_method')
        del_address = request.POST.get('address')

        if selected_payment == 'cod' and not cod_allowed:
            messages.error(request, "Cash on Delivery is not available for this order.")
            return redirect('checkout_view', product_id=product_id) if product_id else redirect('checkout_view')

        ordered_products_summary = []

        for item in cart_items:
            prod = item['product']
            qty = item['quantity']
            final_amount = item['final_amount']

            # ഡാറ്റാബേസിലേക്ക് ഓർഡർ സേവ് ചെയ്യുന്നു 🌟
            Buying.objects.create(
                user=request.user,
                product=prod,
                quantity=qty,
                total_amount=final_amount, # ടാക്സ് ഉൾപ്പെടെയുള്ള ഫൈനൽ തുക
                customer_f_name=f_name,
                customer_s_name=s_name,
                customer_email=email,
                customer_phone=phone,
                payment_method=selected_payment,
                status='Active',
                del_address=del_address
            )

            ordered_products_summary.append({
                'product': prod,
                'quantity': qty,
                'final_amount': final_amount
            })

        if not is_single_product:
            request.session['cart'] = {}

        success_context = {
            'ordered_items': ordered_products_summary,
            'original_total': grand_original_total,
            'discounted_total': grand_discounted_total,
            'total_savings': grand_original_total - grand_discounted_total,
            'tax_amount': grand_tax_amount,
            'final_amount': grand_final_amount
        }
        messages.success(request, "Your order has been placed successfully! 🎉")
        return render(request, 'buy_success.html', success_context)

    # 📄 പേജ് ആദ്യം ലോഡ് ചെയ്യുമ്പോൾ കാണിക്കേണ്ട വിവരങ്ങൾ (GET Method Context)
    context = {
        'cart_items': cart_items,
        'total_price': grand_discounted_total, # Subtotal (ടാക്സ് ഇല്ലാതെ)
        'tax_amount': grand_tax_amount,        # ആകെ ടാക്സ് തുക
        'final_amount': grand_final_amount,    # യൂസർ പേ ചെയ്യേണ്ട തുക (Grand Total)
        'cod_allowed': cod_allowed,
        'product_id': product_id
    }
    return render(request, 'buy.html', context)

def search_products(request):
    query = request.GET.get('q')
    results = Product.objects.none()
    similar_products = Product.objects.none()

    if query:
        # യൂസർ സെർച്ച് ചെയ്ത വാക്കുള്ള പ്രൊഡക്റ്റുകൾ കണ്ടുപിടിക്കുന്നു
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
        # Similar Products കണ്ടെത്താൻ: സെർച്ച് റിസൾട്ടിലുള്ള പ്രൊഡക്റ്റുകളുടെ അതേ കാറ്റഗറിയിലുള്ള മറ്റ് പ്രൊഡക്റ്റുകൾ എടുക്കുന്നു
        if results.exists():
            categories = results.values_list('category', flat=True).distinct()
            similar_products = Product.objects.filter(category__in=categories).exclude(id__in=results)[:4]
        else:
            # റിസൾട്ട് ഒന്നും ഇല്ലെങ്കിൽ തൽക്കാലം ഏതെങ്കിലും 4 പ്രൊഡക്റ്റുകൾ കാണിക്കും
            similar_products = Product.objects.all().order_count()[:4] if hasattr(Product.objects, 'order_count') else Product.objects.all()[:4]

    context = {
        'query': query,
        'results': results,
        'similar_products': similar_products,
    }
    return render(request, 'search_results.html', context)

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')
        
        # ഡാറ്റാബേസിലേക്ക് സേവ് ചെയ്യുന്നു
        CustomerQuery.objects.create(
            name=name,
            email=email,
            message=message_text
        )
        
        # വിജയിച്ചു എന്ന് യൂസർക്ക് കാണിക്കാൻ ഒരു അലേർട്ട് മെസ്സേജ്
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact') # നിങ്ങളുടെ കോൺടാക്ട് പേജിന്റെ URL name കൊടുക്കുക
        
    return render(request, 'contact.html')

@login_required(login_url='sign_in') # ലോഗിൻ ചെയ്തിട്ടില്ലെങ്കിൽ സൈൻ-ഇൻ പേജിലേക്ക് വിടും
def account_view(request):
    return render(request, 'account.html')

@login_required(login_url='sign_in')
def addresses_view(request):
    # 🔍 ലോഗിൻ ചെയ്ത യൂസറുടെ ഏറ്റവും പുതിയ ഓർഡർ കണ്ടുപിടിക്കുന്നു
    latest_order = Buying.objects.filter(user=request.user).order_by('-booking_date').first()
    
    # ഡാറ്റാബേസിൽ ഉള്ള അഡ്രസ്സ് എടുക്കുന്നു (ഓർഡർ ഇല്ലെങ്കിൽ None ആയിരിക്കും)
    current_address = latest_order.del_address if latest_order else ""

    if request.method == 'POST':
        new_address = request.POST.get('user_address')
        
        # 💾 യൂസർ അഡ്രസ്സ് മാറ്റി അടിച്ചാൽ, അവരുടെ എല്ലാ Active ഓർഡറുകളിലെയും അഡ്രസ്സ് അപ്ഡേറ്റ് ചെയ്യുന്നു
        Buying.objects.filter(user=request.user, status='Active').update(del_address=new_address)
        
        return redirect('address_edit')

    return render(request, 'addresses.html', {
        'current_address': current_address,
        'latest_order': latest_order
    })

@login_required(login_url='sign_in')
def payments_view(request):
    return render(request, 'payments.html')

@login_required(login_url='sign_in')
def wishlist_view(request):
    # യൂസർ സേവ് ചെയ്ത എല്ലാ വിഷ്‌ലിസ്റ്റ് സാധനങ്ങളും എടുക്കുന്നു
    my_wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'my_wishlist': my_wishlist})

from django.http import JsonResponse


@login_required(login_url='sign_in')
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
    
    # 1. വിഷ്‌ലിസ്റ്റിൽ ഉണ്ടോ എന്ന് നോക്കി ആഡ് ചെയ്യുകയോ കളയുകയോ ചെയ്യുന്നു
    if wishlist_item.exists():
        wishlist_item.delete()
        status = 'removed'
    else:
        Wishlist.objects.create(user=request.user, product=product)
        status = 'added'
        
    # 2. റിക്വസ്റ്റ് AJAX വഴി (JavaScript) ആണോ വന്നതെന്ന് പരിശോധിക്കുന്നു
    # (AJAX ആണെങ്കിൽ പേജ് റീഫ്രഷ് ആകില്ല, JSON മറുപടി മാത്രം നൽകിയാൽ മതി)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': status})
    
    # 3. സാധാരണ ലിങ്ക് വഴിയോ ബട്ടൺ വഴിയോ ആണെങ്കിൽ താഴെ പറയുന്ന റീഡയറക്റ്റ് ലോജിക് വർക്ക് ചെയ്യും
    referer_url = request.META.get('HTTP_REFERER', '')
    
    # യൂസർ പെയ്‌മെന്റ്/ചെക്കൗട്ട് പേജിൽ നിന്നാണ് അമർത്തുന്നതെങ്കിൽ
    if 'payment' in referer_url or 'buying' in referer_url or 'checkout' in referer_url:
        return redirect('wishlist') # നിങ്ങളുടെ വിഷ്‌ലിസ്റ്റ് യു.ആർ.എൽ പേര് കൊടുക്കുക
        
    # മറ്റ് പേജുകളിൽ നിന്നാണെങ്കിൽ അതേ പേജിലേക്ക് തന്നെ റീഫ്രഷ് ചെയ്യുന്നു
    return redirect(request.META.get('HTTP_REFERER', 'home'))