from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .forms import *
from .models import *
from .auth import *


def get_header_context(active_view):
    nav_items = [
        {'name': 'Venda', 'view': 'order'},
        {'name': 'Config', 'url': '#'},
        {'name': 'Admin', 'view': 'admin:index'},
    ]
    if active_view == 'login':
        nav_items += [{'name': 'Login', 'view': 'login'}]
    else:
        nav_items += [{'name': 'Logout', 'view': 'logout'}]
    for item in nav_items:
        if not 'url' in item:
            item['url'] = reverse(item['view'])
        item['active'] = item.get('view') == active_view
    return {'nav_items': nav_items}


def login(request):
    if request.method == 'POST':
        form = CashierLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['cashier'].strip()
            try:
                cashier = Cashier.objects.get(name=name)
            except Cashier.DoesNotExist:
                messages.error(request, 'Caixa não encontrado.')
            else:
                request.session[SESSION_KEY] = cashier.id
                return redirect('order')
    else:
        form = CashierLoginForm()
    return render(request, 'login.html', {
        'header': get_header_context(request.resolver_match.view_name),
        'form': form
    })


def logout(request):
    request.session.pop(SESSION_KEY, None)
    return redirect('login')


@login_required
def order(request, cashier):
    order = Order.objects.filter(cashier=cashier, closed=False).first()

    if request.method == 'POST':
        action = request.POST.get('action')
        if not order and action == 'add_product':
            order = Order.objects.create(cashier=cashier)
        if not order:
            return redirect('order')

        cancel_order = False
        if action == 'add_product':
            form = AddProductForm(request.POST)
            if form.is_valid():
                form.save(order)
            else:
                messages.error(request, 'Erro ao adicionar produto.')
        elif action == 'remove_product':
            form = RemoveProductForm(request.POST)
            if form.is_valid():
                form.save(order)
            else:
                messages.error(request, 'Erro ao remover produto.')
        elif action == 'update_quantity':
            form = UpdateQuantityForm(request.POST)
            if form.is_valid():
                form.save(order)
            else:
                messages.error(request, 'Erro ao atualizar quantidade.')
        elif action == 'add_payment':
            form = AddPaymentForm(request.POST)
            if form.is_valid():
                form.save(order)
            else:
                messages.error(request, 'Erro ao adicionar pagamento.')
        elif action == 'cancel_order':
            cancel_order = True
            messages.info(request, 'Pedido cancelado.')
        elif action == 'finish_order':
            if order.total_paid >= order.total:
                order.close()
                messages.success(request, 'Pedido finalizado!')
            else:
                messages.error(request, 'Pagamento insuficiente.')

        if cancel_order or order.products.count() == 0:
            order.delete()
            order = None
        return redirect('order')

    categories = ProductCategory.objects.all()
    products = Product.objects.filter(is_active=True)
    return render(request, 'order.html', {
        'header': get_header_context(request.resolver_match.view_name),
        'cashier': cashier,
        'order': order,
        'product_categories': categories,
        'products': products,
        'add_product_form': AddProductForm(),
        'remove_product_form': RemoveProductForm(),
        'update_quantity_form': UpdateQuantityForm(),
        'add_payment_form': AddPaymentForm(),
    })
