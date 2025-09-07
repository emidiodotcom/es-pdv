import locale

from django.db import models
from django.core.exceptions import ValidationError


class Cashier(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<Cashier: {self.name}>'

    class Meta:
        ordering = ['name']


class ProductCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<ProductCategory: {self.name}>'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Product(models.Model):
    category = models.ForeignKey(ProductCategory,
                                 on_delete=models.RESTRICT,
                                 related_name='products')
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/',
                              null=True,
                              blank=True)

    @property
    def price_display(self):
        return locale.currency(self.price, grouping=True)

    def __str__(self):
        return f'{self.id} - {self.name} ({self.category})'

    def __repr__(self):
        return f'<Product: id={self.id} name="{self.name}" category="{self.category}">'

    class Meta:
        ordering = ['name']


class Order(models.Model):
    cashier = models.ForeignKey(Cashier,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    def close(self):
        if self.total_paid < self.total:
            raise ValidationError('Pagamento insuficiente.')
        for item in self.products.all():
            item.product.stock -= item.quantity
            item.product.save()
        self.closed = True
        self.save()

    @property
    def total(self):
        return sum(item.subtotal for item in self.products.all())

    @property
    def total_paid(self):
        return sum(p.amount for p in self.payments.all())

    @property
    def total_display(self):
        return locale.currency(self.total, grouping=True)

    @property
    def total_paid_display(self):
        return locale.currency(self.total_paid, grouping=True)

    def __str__(self):
        return f'Pedido #{self.id}'

    def __repr__(self):
        return f'<Order: id={self.id} created_at=<{self.created_at}> closed={self.closed}>'

    class Meta:
        ordering = ['-created_at']


class OrderProduct(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='products')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    @property
    def subtotal_display(self):
        return locale.currency(self.subtotal, grouping=True)

    def __str__(self):
        return f'Produto de Pedido #{self.id}'

    def __repr__(self):
        return f'<OrderProduct: id={self.id} order={self.order.id} product={self.product.id} quantity={self.quantity}>'


class OrderPayment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Dinheiro'),
        ('card', 'Cartão'),
        ('pix', 'PIX'),
    ]

    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='payments')
    method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    @property
    def amount_display(self):
        return locale.currency(self.amount, grouping=True)

    def __str__(self):
        return f'Pagamento #{self.id} em {self.method}'

    def __repr__(self):
        return f'<OrderPayment: id={self.id} order={self.order.id} method={self.method} paid_at=<{self.paid_at}>>'

    class Meta:
        ordering = ['-paid_at']
