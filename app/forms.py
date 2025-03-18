from django.core.exceptions import ValidationError
from django.forms import ModelForm
from app.models import Produto

# Formulário para Cadastro
class ProdutoCreateForm(ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'marca', 'valor', 'quantidade']  # Inclui quantidade

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        marca = cleaned_data.get('marca')

        # Verifica se já existe um produto com o mesmo nome e marca
        if Produto.objects.filter(nome=nome, marca=marca).exists():
            raise ValidationError("Já existe um produto com este nome e marca.")
        return cleaned_data

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor < 0:
            raise ValidationError("O valor do produto não pode ser negativo.")
        return valor

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade < 0:
            raise ValidationError("A quantidade do produto não pode ser negativa.")
        return quantidade

# Formulário para Edição
class ProdutoEditForm(ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'marca', 'valor']  # Exclui quantidade

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor < 0:
            raise ValidationError("O valor do produto não pode ser negativo.")
        return valor
