from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('fashion', 'Fashion & Dresses'),
        ('mobile', 'Mobiles'),
        ('beauty', 'Beauty Products'),
        ('electronic', 'Electronics'),
        ('home_appliance', 'Home Appliances'),
        ('toy', 'Toys'),
    ]

    name = models.CharField(max_length=200)
    price = models.IntegerField() 
    original_price = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    users_bought = models.ManyToManyField(User, blank=True)
    is_cod_available = models.BooleanField(default=True, verbose_name="COD Available?")
    tax_rate = models.DecimalField(
        max_digits=5,        # ആകെ വരാവുന്ന അക്കങ്ങളുടെ എണ്ണം (ഉദാഹരണത്തിന്: 100.00 - ആകെ 5 അക്കങ്ങൾ)
        decimal_places=2,    # ദശാംശത്തിന് ശേഷം വരാവുന്ന അക്കങ്ങൾ (e.g., 1.20, 0.30)
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        help_text="Enter GST/Tax percentage (e.g., 1.2 for 1.2%, 0.3 for 0.3%)"
    )
    # 🌟 Parent-Child Color Variations ഫീൽഡുകൾ
    parent_product = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='variants',
        help_text="മെയിൻ പ്രൊഡക്റ്റ് ആണെങ്കിൽ ഇത് ബ്ലാങ്ക് ഇടുക. ഇതൊരു കളർ വേരിയന്റ് ആണെങ്കിൽ മെയിൻ പ്രൊഡക്റ്റ് സെലക്ട് ചെയ്യുക."
    )
    color_name = models.CharField(max_length=50, blank=True, null=True, help_text="ഉദാ: Matt Black")
    color_code = models.CharField(max_length=7, blank=True, null=True, help_text="Hex code: #000000")

    def get_size_list(self):
        if self.sizes:
            return [size.strip() for size in self.sizes.split(',')]
        return []

    def __str__(self):
        if self.color_name:
            return f"{self.name} ({self.color_name}) - [{self.category}]"
        return f"{self.name} - [{self.category}]"

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return round(discount)
        return 0


# ഓരോ സൈസും അതിന്റെ വിലയും സൂക്ഷിക്കാൻ
class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant')
    size = models.CharField(max_length=10) # S, M, L, XL
    price = models.IntegerField() # ഈ സൈസിന്റെ വില
    original_price = models.IntegerField(null=True, blank=True)
    
    
    @property
    def Discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return round(discount)
        return 0

    def __str__(self):
        return f"{self.product.name} - {self.size} ({self.price})"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='extra_images')
    additional_image = models.ImageField(upload_to='products/additional', null=True, blank=True)

    def __str__(self):
        return f"Extra Image for {self.product.name}"


class MobileSpecification(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='mobile_specs')
    processor = models.CharField(max_length=100, help_text="e.g., Snapdragon 8 Gen 3 / Apple A18 Pro")
    chipset = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 4nm Octa-core")
    ram = models.CharField(max_length=50, help_text="e.g., 8GB / 12GB LPDDR5X")
    storage = models.CharField(max_length=50, help_text="e.g., 128GB / 256GB UFS 4.0")
    battery = models.CharField(max_length=100, help_text="e.g., 5000 mAh with 67W Fast Charging")
    camera = models.CharField(max_length=200, blank=True, null=True, help_text="e.g., 50MP Main + 12MP Ultra-wide")
    display = models.CharField(max_length=150, blank=True, null=True, help_text="e.g., 6.7-inch AMOLED, 120Hz")

    def __str__(self):
        return f"Specs for {self.product.name}"

class Buying(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Cancelled', 'Cancelled'),
    ]

    # 🌟 പേയ്‌മെന്റ് ഓപ്ഷനുകൾക്കായുള്ള ചോയ്‌സ്
    PAYMENT_CHOICES = [
        ('card', 'Credit / Debit Card'),
        ('paypal', 'PayPal'),
        ('upi', 'UPI / NetBanking'),
        ('cod','COD')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_f_name = models.CharField(max_length=100)
    customer_s_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    quantity = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='paypal')
    del_address=models.TextField()

    def __str__(self):
        return f"{self.customer_f_name} - {self.product.name} ({self.status})"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # ഒരു പ്രൊഡക്റ്റ് ഒരു തവണയേ വിഷ്‌ലിസ്റ്റിൽ വരാവൂ

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
class CustomerQuery(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # മെസ്സേജ് വന്ന സമയം ഓട്ടോമാറ്റിക് ആയി എടുക്കും

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

    class Meta:
        verbose_name = "Customer Query"
        verbose_name_plural = "Customer Queries"

