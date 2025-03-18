from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from app.forms import ProdutoCreateForm, ProdutoEditForm
from app.models import Produto
from django.db.models import Sum, F

def sell(request):
    data = {}
    search = request.GET.get('search')
    if search:
        data['db'] = Produto.objects.filter(nome__icontains=search) | Produto.objects.filter(marca__icontains=search)
    else:
        data['db'] = Produto.objects.all()
    return render(request, 'sell.html', data)


def process_sell(request):
    if request.method == "POST":
        error_messages = []
        quantities = request.POST.getlist("quantity")
        product_ids = request.POST.getlist("product_id")

        for product_id, quantity_str in zip(product_ids, quantities):
            try:
                # Tenta carregar o produto com base no ID
                produto = Produto.objects.get(id=product_id)

                # Verifica se o valor é um número inteiro
                if not quantity_str.isdigit():
                    error_messages.append(f"Quantidade inválida inserida para o produto {produto.nome} ({produto.marca}). Apenas números inteiros são permitidos.")
                    continue

                # Converte para inteiro
                quantity = int(quantity_str)

                if quantity < 0:
                    error_messages.append(f"A quantidade não pode ser negativa para o produto {produto.nome} ({produto.marca}).")
                    continue

                # Valida a quantidade em estoque
                if quantity > produto.quantidade:
                    error_messages.append(f"A quantidade vendida ({quantity}) excede o estoque disponível ({produto.quantidade}) para o produto {produto.nome} ({produto.marca}).")
                    continue

                # Atualiza o estoque
                produto.quantidade -= quantity
                produto.save()

            except Produto.DoesNotExist:
                error_messages.append(f"Produto não encontrado para o ID {product_id}.")
                continue

        # Se houver erros, retorna ao formulário com mensagens de erro
        if error_messages:
            return render(request, "sell.html", {"db": Produto.objects.all(), "error_messages": error_messages})

        # Redireciona ao sucesso após venda
        return redirect("/")
    return HttpResponseBadRequest("Método não permitido.")

def add_stock(request):
    data = {}
    search = request.GET.get('search')
    if search:
        data['db'] = Produto.objects.filter(nome__icontains=search) | Produto.objects.filter(marca__icontains=search)
    else:
        data['db'] = Produto.objects.all()
    return render(request, 'add_stock.html', data)

def process_stock(request):
    if request.method == "POST":
        error_messages = []
        quantities = request.POST.getlist("quantity")
        product_ids = request.POST.getlist("product_id")

        for product_id, quantity_str in zip(product_ids, quantities):
            try:
                # Tenta carregar o produto com base no ID
                produto = Produto.objects.get(id=product_id)

                # Verifica se o valor é um número inteiro
                if not quantity_str.isdigit():
                    error_messages.append(f"Quantidade inválida inserida para o produto {produto.nome} ({produto.marca}). Apenas números inteiros são permitidos.")
                    continue

                # Converte para inteiro
                quantity = int(quantity_str)

                if quantity < 0:
                    error_messages.append(f"A quantidade para adicionar não pode ser negativa para o produto {produto.nome} ({produto.marca}).")
                    continue

                # Atualiza o estoque
                produto.quantidade += quantity
                produto.save()

            except Produto.DoesNotExist:
                error_messages.append(f"Produto não encontrado para o ID {product_id}.")
                continue

        # Se houver erros, retorna ao formulário com mensagens de erro
        if error_messages:
            return render(request, "add_stock.html", {"db": Produto.objects.all(), "error_messages": error_messages})

        # Redireciona ao sucesso após adicionar estoque
        return redirect("/")
    return HttpResponseBadRequest("Método não permitido.")


def home(request):
    data = {}
    search = request.GET.get('search')
    if search:
        data['db'] = Produto.objects.filter(nome__icontains=search) | Produto.objects.filter(marca__icontains=search)
    else:
        data['db'] = Produto.objects.all()  # Buscar produtos
    
    # Calcula o valor total do estoque
    data['valor_total_estoque'] = Produto.objects.aggregate(
        total=Sum(F('valor') * F('quantidade'))
    )['total'] or 0  # Define 0 como padrão caso esteja vazio

    return render(request, 'index.html', data)


def form(request):
    data = {}
    data['form'] = ProdutoCreateForm()  # Formulário de Produto
    return render(request, 'form.html', data)

# Para Cadastro
def create(request):
    form = ProdutoCreateForm(request.POST or None)
    if form.is_valid():
        form.save()  # Salva no banco
        return redirect('home')
    return render(request, 'form.html', {'form': form})

# Para Edição
def edit(request, pk):
    produto = Produto.objects.get(pk=pk)
    form = ProdutoEditForm(request.POST or None, instance=produto)
    if form.is_valid():
        form.save()  # Salva no banco sem modificar 'quantidade'
        return redirect('home')
    return render(request, 'edition.html', {'form': form, 'db': produto})

def view(request, pk):
    produto = get_object_or_404(Produto, id=pk)
    valor_total = produto.calcular_total()  # Método da classe Produto
    return render(request, "view.html", {"produto": produto, "valor_total": valor_total})


def update(request, pk):
    # Busca o produto pelo ID
    produto = Produto.objects.get(pk=pk)
    
    # Processa o formulário de edição (ProdutoEditForm) sem o campo 'quantidade'
    form = ProdutoEditForm(request.POST or None, instance=produto)
    if form.is_valid():
        # Salva os dados do formulário
        produto = form.save(commit=False)
        
        # Atribui o valor atual de 'quantidade' para mantê-lo inalterado
        # (Se necessário, podemos adicioná-lo explicitamente, mas ele já será mantido)
        produto.save()
        
        # Redireciona para a home após o salvamento bem-sucedido
        return redirect('home')
    else:
        # Renderiza a página de edição novamente com os erros
        return render(request, 'edition.html', {'form': form, 'db': produto})




def delete(request, pk):
    db = Produto.objects.get(pk=pk)
    db.delete()
    return redirect('home')