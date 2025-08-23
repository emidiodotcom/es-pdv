import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from pdv.models import ProductCategory, Product, Cashier


class Command(BaseCommand):
    def handle(self, *args, **options):
        if ProductCategory.objects.exists():
            self.stdout.write(self.style.WARNING('Example data already exists.'))
            return

        categories = {
            'Bebidas': [
                'Coca-Cola 350ml', 'Guaraná Antarctica 350ml', 'Suco de Laranja 300ml',
                'Água Mineral 500ml', 'Cerveja Skol 350ml', 'Cerveja Brahma 350ml',
                'Refrigerante Fanta Uva 350ml', 'Refrigerante Sprite 350ml',
                'Suco de Uva Integral 300ml', 'Chá Gelado 300ml'
            ],
            'Lanches': [
                'X-Burguer', 'X-Salada', 'X-Bacon', 'Cachorro Quente Simples',
                'Cachorro Quente Especial', 'Cheeseburger Duplo', 'Bauru Tradicional',
                'Misto Quente', 'Sanduíche de Frango', 'Hambúrguer Vegano'
            ],
            'Restaurante': [
                'Feijoada Completa', 'Bife à Parmegiana', 'Frango à Passarinho',
                'Strogonoff de Frango', 'Peixe Frito', 'Lasanha de Carne',
                'Moqueca Baiana', 'Costela Assada', 'Escondidinho de Carne Seca',
                'Picadinho com Arroz e Feijão'
            ],
            'Sobremesas': [
                'Brigadeiro', 'Beijinho', 'Pudim de Leite', 'Mousse de Maracujá',
                'Quindim', 'Doce de Leite', 'Torta de Limão', 'Gelatina Colorida',
                'Sorvete de Chocolate', 'Bolo de Cenoura com Cobertura'
            ]
        }

        for cat_name, products in categories.items():
            cat = ProductCategory.objects.create(name=cat_name)
            for prod_name in products:
                Product.objects.create(
                    category=cat,
                    name=prod_name,
                    price=Decimal(random.randint(500, 3000)) / 100,
                    stock=random.randint(5, 20),
                    is_active=True
                )

        if not Cashier.objects.exists():
            Cashier.objects.create(name='caixa')

        self.stdout.write(self.style.SUCCESS('Example data was inserted!'))
