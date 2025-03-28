from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from app.forms import ProdutoCreateForm, ProdutoEditForm
from app.models import Produto
from django.db.models import Sum, F, Func
from app.models import Venda  
from django.utils.timezone import now
from django.utils.timezone import make_aware, localtime
from datetime import datetime, timedelta




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
                produto = Produto.objects.get(id=product_id)

                if not quantity_str.isdigit() or int(quantity_str) < 0:
                    error_messages.append(f"Quantidade inválida inserida para o produto {produto.nome} ({produto.marca}). Apenas números inteiros são permitidos.")
                    continue

                quantity = int(quantity_str)

                if quantity > produto.quantidade:
                    error_messages.append(f"Estoque insuficiente para o produto {produto.nome} ({produto.marca}).")
                    continue

                produto.quantidade -= quantity
                produto.save()

                # Registrar a venda
                Venda.objects.create(produto=produto, quantidade_vendida=quantity, data_venda=now())

            except Produto.DoesNotExist:
                error_messages.append(f"Produto com ID {product_id} não encontrado.")
                continue

        if error_messages:
            return render(request, "sell.html", {"db": Produto.objects.all(), "error_messages": error_messages})

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


def generate_report(request):
    # Capturar os dados do formulário
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    order_by_faturamento = request.GET.get('order_by_faturamento')  # Ordenar por maior faturamento
    order_by_newest = request.GET.get('order_by_newest')  # Ordenar do mais novo para o mais antigo

    # Data atual para exibição
    data_geracao = datetime.now().strftime('%d/%m/%Y')

    vendas = []
    total_faturamento = 0
    no_data_message = None

    try:
        # Configurar um intervalo padrão caso as datas sejam omitidas
        if not start_date:
            start_date = "1900-01-01"  # Data inicial padrão
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')  # Data final padrão

        # Converter strings de datas para datetime com timezone
        start_date_local = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date_local = make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59))

        # Converter para UTC (caso o banco de dados exija)
        start_date_utc = localtime(start_date_local).astimezone()
        end_date_utc = localtime(end_date_local).astimezone()

        # Filtrar vendas dentro do intervalo de datas
        vendas = Venda.objects.filter(data_venda__range=[start_date_utc, end_date_utc]).annotate(
            produto_nome=F('produto__nome'),
            produto_marca=F('produto__marca'),
            quantidade_total=Sum('quantidade_vendida'),
            faturamento_total=F('quantidade_vendida') * F('produto__valor')
        ).exclude(quantidade_total=0)  # Excluir vendas com quantidade zero


        # Calcular o total de faturamento (independente do agrupamento)
        total_faturamento = vendas.aggregate(total=Sum('faturamento_total'))['total'] or 0

        # Caso nenhuma venda seja encontrada
        if not vendas.exists():
            no_data_message = "Nenhum dado encontrado para o intervalo informado."

    except Exception as e:
        print(f"Erro ao processar os dados: {e}")
        no_data_message = "Erro ao processar as informações do relatório."

    return render(request, 'report.html', {
        'vendas': vendas,
        'total_faturamento': total_faturamento,
        'no_data_message': no_data_message,
        'data_geracao': data_geracao,
    })



def generate_report(request):
    # Capturar as datas do formulário
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    order_by_faturamento = request.GET.get('order_by_faturamento')  # Ordenar por maior faturamento
    order_by_newest = request.GET.get('order_by_newest')  # Ordenar do mais novo para o mais antigo
    group_products = request.GET.get('group_products')  # Agrupar produtos iguais

    # Data atual formatada (para exibição no relatório)
    data_geracao = datetime.now().strftime('%d/%m/%Y')

    vendas = []
    total_faturamento = 0
    start_date_local = None
    end_date_local = None
    no_data_message = None

    if start_date and end_date:
        try:
            # Converter strings para objetos datetime (timezone-aware local)
            start_date_local = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end_date_local = make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59))

            # Verificar se o intervalo é inválido
            if start_date_local > end_date_local:
                no_data_message = "A data inicial não pode ser maior que a data final. Por favor, corrija o intervalo."
            else:
                # Converter para UTC
                start_date_utc = localtime(start_date_local).astimezone()
                end_date_utc = localtime(end_date_local).astimezone()

                # Filtrar vendas no intervalo UTC
                vendas = Venda.objects.filter(data_venda__range=[start_date_utc, end_date_utc]).annotate(
                    produto_nome=F('produto__nome'),
                    produto_marca=F('produto__marca'),
                    quantidade_total=Sum('quantidade_vendida'),
                    faturamento_total=F('quantidade_vendida') * F('produto__valor')
                ).exclude(quantidade_total=0)

                # Aplicar ordenação do mais novo para o mais antigo, se solicitado
                if order_by_newest:
                    vendas = vendas.order_by('-data_venda')  # Ordena pela data decrescente
                if order_by_faturamento:
                    vendas = vendas.order_by('-faturamento_total')  # Ordena por maior faturamento

                # Aplicar agrupamento por produtos iguais, se solicitado
                if group_products:
                    vendas = vendas.values('produto_nome', 'produto_marca').annotate(
                        quantidade_total=Sum('quantidade_vendida'),
                        faturamento_total=Sum(F('quantidade_vendida') * F('produto__valor'))
                    ).order_by('-faturamento_total')  # Ordena os grupos por maior faturamento
                
                    # Adicionar valores padrão para agrupamento
                    for venda in vendas:
                        venda['data_venda'] = "-"
                else:
                    # Formatar a data para DD/MM/AAAA
                    for venda in vendas:
                        venda.data_venda = venda.data_venda.strftime('%d/%m/%Y')  # Ajusta o formato da data

                # Calcular o faturamento total diretamente do conjunto 'vendas'
                total_faturamento = vendas.aggregate(
                    total=Sum('faturamento_total') if group_products else Sum(F('quantidade_vendida') * F('produto__valor'))
                )['total'] or 0

                # Mensagem de erro se não houver vendas no período
                if not vendas.exists():
                    no_data_message = f"Nenhum dado encontrado para o período de {start_date_local.date().strftime('%d/%m/%Y')} a {end_date_local.date().strftime('%d/%m/%Y')}."
        except Exception as e:
            print(f"Erro ao processar o intervalo de datas: {e}")
            no_data_message = "Erro ao processar as datas fornecidas."
    elif request.GET:
        # Se o formulário foi enviado sem datas completas
        no_data_message = "Por favor, insira um intervalo de datas válido para gerar o relatório."

    return render(request, 'report.html', {
        'vendas': vendas,
        'total_faturamento': total_faturamento,
        'start_date': start_date_local.date().strftime('%d/%m/%Y') if start_date_local else None,
        'end_date': end_date_local.date().strftime('%d/%m/%Y') if end_date_local else None,
        'no_data_message': no_data_message,
        'data_geracao': data_geracao,
        'total_vendas': f"Tipos de produtos vendidos: {len(vendas)}" if group_products else f"Total de vendas no período: {len(vendas) if isinstance(vendas, list) else vendas.count()}"
    })