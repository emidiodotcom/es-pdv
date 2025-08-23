from functools import wraps

from django.shortcuts import redirect

from .models import Cashier

SESSION_KEY = 'cashier_id'


def get_current_cashier(request):
    cid = request.session.get(SESSION_KEY)
    if not cid:
        return None
    try:
        return Cashier.objects.get(pk=cid)
    except Cashier.DoesNotExist:
        request.session.pop(SESSION_KEY, None)
        return None


def login_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        cashier = get_current_cashier(request)
        if not cashier:
            return redirect('login')
        return view_func(request, cashier, *args, **kwargs)
    return _wrapped
