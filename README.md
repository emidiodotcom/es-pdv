## Ponto de venda (PDV) em Django
    

Configuração para desenvolvimento (unix-like):

    python -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py pdv_populate
    ./manage.py runserver


![[pdv.png]](doc/pdv.png)
