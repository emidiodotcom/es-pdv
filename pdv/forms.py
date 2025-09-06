from decimal import Decimal

from django import forms
from django.shortcuts import get_object_or_404

from .models import *


class CashierLoginForm(forms.Form):
    cashier = forms.CharField(label='Nome do caixa')


class AddProductForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True),
        label='Produto'
    )
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantidade')

    def save(self, order):
        product = self.cleaned_data['product']
        quantity = self.cleaned_data['quantity']

        item, created = OrderProduct.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()


class UpdateQuantityForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=0, label='Quantidade')

    def save(self, order):
        item = get_object_or_404(OrderProduct, pk=self.cleaned_data['item_id'], order=order)
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()


class AddPaymentForm(forms.Form):
    method = forms.ChoiceField(choices=OrderPayment.METHOD_CHOICES, label='Forma de pagamento')
    amount = forms.CharField(label='Valor')

    def clean_amount(self):
        data = self.cleaned_data['amount'].replace(',', '.')
        try:
            value = Decimal(data)
            if value < 0.01 or value >= 10**8:
                raise forms.ValidationError
        except:
            raise forms.ValidationError('Valor inválido')
        return value

    def save(self, order):
        payment = OrderPayment.objects.create(
            order=order,
            method=self.cleaned_data['method'],
            amount=self.cleaned_data['amount']
        )
