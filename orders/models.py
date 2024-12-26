from django.db import models
from django.utils import timezone
from products.models import Product
from django.templatetags.static import static
from django.utils.dateformat import DateFormat


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    paid = models.BooleanField(default=False, null=True, blank=False)
    is_email_sent = models.BooleanField(default=False, null=True, blank=False)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    amount = models.CharField(max_length=5, default=0)
    mpesa_code = models.CharField(max_length=10, blank=True, null=True)
    order_number = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, null=False, blank=True)
    description = models.CharField(max_length=180, null=True, blank=True)
    order_tracking_id = models.CharField(max_length=100, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    qr = models.FileField(upload_to='qrcodes/', blank=True, null=True)
    receipt = models.FileField(upload_to='receipts/', max_length=100, null=True, blank=True)
    payment_date = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Order No. #{self.get_order_number}'

    @property
    def get_phone_number(self):
        if self.phone_number:
            return self.phone_number
        return "N/A"

    @property
    def get_email(self):
        if self.email:
            return self.email
        return "N/A"

    @property
    def get_fullname(self):
        if self.first_name:
            first_name = self.first_name
        else:
            first_name = "John"
        if self.last_name:
            last_name = self.last_name
        else:
            last_name = "Doe"
        return str(f"{first_name} {last_name}")

    @property
    def get_qr(self):
        if self.qr:
            return self.qr.url
        return None

    @property
    def get_receipt(self):
        if self.receipt:
            return self.receipt.url
        return None

    @property
    def get_order_number(self):
        if self.pk:
            return f"400{self.pk}"
        return None

    @property
    def get_order_image(self):
        if self.product.img_md:
            return self.product.img_md
        return static('order.jpg')

    @property
    def get_mpesa_code(self):
        if self.mpesa_code:
            return self.mpesa_code
        return None

    @property
    def get_date(self):
        date_format = DateFormat(self.date_ordered.astimezone(
            timezone.get_current_timezone()))
        formatted_date = date_format.format('M. d, Y')
        return formatted_date

    @property
    def get_cart_total(self):
        if self.amount:
            return self.amount
        elif self.product:
            return self.product.price
        return 0

    # @property
    # def get_cart_total(self):
    #     orderitems = self.orderitem_set.all()
    #     total = sum([item.get_total for item in orderitems])
    #     return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=150, null=True, blank=True)

    @ property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.product

    @ property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.address}'

    @property
    def get_short_address(self):
        short_address = self.address
        return short_address
