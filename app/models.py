from django.db import models

# Modelo ajustado para "Produto"
class Produto(models.Model):
    nome = models.CharField(max_length=150)  # Nome do Produto
    marca = models.CharField(max_length=100)  # Nome da Marca
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor do Produto
    quantidade = models.IntegerField(default=0)  # Novo campo de quantidade
    
    # Método para calcular o total do valor
    def calcular_total(self):
        return self.valor * self.quantidade

class Meta:
    constraints = [
        models.UniqueConstraint(fields=['nome', 'marca'], name='unique_produto_marca')
        ]

