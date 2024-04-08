from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .models import Mestre, Lutador, Chaveamento
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):
    return render(request, 'home.html')

def cadastro(request):
    return render(request, 'usuarios/cadastro.html')
    
@login_required
def sucesso(request):
    # Verifica se o usuário logado é um mestre
    tipo_usuario = request.POST.get('tipo')

    if tipo_usuario == 'mestre':
        novo_usuario = Mestre()
    elif tipo_usuario == 'lutador':
        if not request.user.is_authenticated or not request.user.email in Mestre.objects.values_list('email', flat=True):
            messages.error(request, 'Você não tem permissão para realizar esta ação.')
            return render(request, 'usuarios/cadastro.html')
        novo_usuario = Lutador()
    else:
        messages.error(request, 'Tipo de usuário inválido.')
        return redirect('cadastro')

    novo_usuario.nome = request.POST.get('nome')
    novo_usuario.genero = request.POST.get('genero')
    novo_usuario.data_nascimento = request.POST.get('data_nascimento')
    novo_usuario.email = request.POST.get('email')
    novo_usuario.telefone = request.POST.get('telefone')
    novo_usuario.endereco = request.POST.get('endereco')
    novo_usuario.categoria = request.POST.get('categoria')

    if tipo_usuario == 'mestre':
        novo_usuario.certificado = request.POST.get('certificado')
        novo_usuario.faixa = request.POST.get('faixa_mestre')
    else:
        novo_usuario.faixa = request.POST.get('faixa')
    # Verifique a senha do usuário logado antes de prosseguir
    senha_confirmacao = request.POST.get('senha', '')

    if not request.user.check_password(senha_confirmacao):
        messages.error(request, 'Senha incorreta. Tente novamente.')
        return render(request, 'usuarios/cadastro.html', {'tipo_usuario': tipo_usuario, 'usuario': novo_usuario})

    # Senha correta, prossiga com o processamento do formulário
    novo_usuario.save()

    return render(request, 'usuarios/sucessoCadastro.html')

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')  # Substitua pelo nome da página desejada após o logout
    else:
        return redirect('/')

def chaveamento(request):
    # Verifica se todas as lutas já têm um vencedor
    if Chaveamento.objects.filter(vencedor__isnull=True).exists():
        print('Algumas lutas ainda não têm um vencedor.')
    else:
        # Todas as lutas têm um vencedor, então podemos criar novas lutas
        criar_novas_lutas()

    # Verifica se já existem partidas
    if not Chaveamento.objects.exists():
        # Se não existir, crie as partidas iniciais
        criar_partidas_iniciais()

    # Obtém todas as partidas restantes
    partidas_restantes = Chaveamento.objects.filter(Q(vencedor=None) | Q(vencedor__isnull=True))

    # Há mais de uma partida restante ou nenhum lutador restante
    return render(request, 'chaveamento.html', {'partidas': partidas_restantes})

def criar_novas_lutas():
    # Obtém todos os lutadores vencedores das lutas anteriores
    vencedores_ids = list(Chaveamento.objects.exclude(vencedor__isnull=True).values_list('vencedor_id', flat=True))
    vencedores = Lutador.objects.filter(id__in=vencedores_ids)

    # Verifica se há pelo menos dois vencedores para criar pares
    if len(vencedores) < 2:
        print('Número insuficiente de vencedores para criar novas lutas.')
        return

    # Agrupa os vencedores em pares para criar as novas lutas
    pares_vencedores = [(vencedores_ids[i], vencedores_ids[i + 1]) for i in range(0, len(vencedores_ids) - 1, 2)]

    # Se não houver um número par de vencedores, defina o último como vencedor final
    if len(vencedores_ids) % 2 != 0:
        ultima_luta = Chaveamento.objects.latest('id')
        vencedor_final_id = ultima_luta.vencedor_id
        vencedor_final = Lutador.objects.get(pk=vencedor_final_id)
        print(f'{vencedor_final.nome} é o vencedor final!')
        return vencedor_final.nome  # Retorna o nome do vencedor final

    # Cria as novas lutas com os pares de vencedores
    for par in pares_vencedores:
        lutador_1 = Lutador.objects.get(pk=par[0])
        lutador_2 = Lutador.objects.get(pk=par[1])
        Chaveamento.objects.create(lutador_1=lutador_1, lutador_2=lutador_2)

    # Verifica se sobrou apenas um lutador
    if len(vencedores) % 2 != 0:
        lutador_restante = vencedores.last()
        Chaveamento.objects.create(lutador_1=lutador_restante, lutador_2=None)


# Adicione esta função para redirecionar para vencedor_final.html com o nome do vencedor final
def vencedor_final(nome_vencedor):
    return redirect('vencedor_final', vencedor_nome=nome_vencedor)

def criar_partidas_iniciais():
    # Verificar se há lutadores suficientes para criar partidas iniciais
    lutadores = Lutador.objects.all()
    if lutadores.count() < 2:
        messages.error("Número insuficiente de lutadores para criar partidas.")
        return

    # Criar partidas iniciais com pares de lutadores
    for i in range(0, lutadores.count(), 2):
        lutador_1 = lutadores[i]
        lutador_2 = lutadores[i + 1] if i + 1 < lutadores.count() else None
        Chaveamento.objects.create(lutador_1=lutador_1, lutador_2=lutador_2)

def registrar_resultado(request, partida_id):
    partida = Chaveamento.objects.get(pk=partida_id)

    if request.method == 'POST':
        vencedor_id = request.POST.get('vencedor')

        if str(partida.lutador_1.id) == vencedor_id:
            vencedor = partida.lutador_1
        elif str(partida.lutador_2.id) == vencedor_id:
            vencedor = partida.lutador_2
        else:
            messages.error(request, 'O vencedor selecionado não é válido.')
            return render(request, 'registrar_resultado.html', {'partida': partida})

        partida.registrar_vencedor(vencedor.id)

        # Verifica se todas as lutas já têm um vencedor
        if Chaveamento.objects.filter(vencedor__isnull=True).exists():
            print(request, 'Algumas lutas ainda não têm um vencedor.')
        else:
            # Todas as lutas têm um vencedor, então podemos criar novas lutas
            criar_novas_lutas()

        return redirect('chaveamento')

    return render(request, 'registrar_resultado.html', {'partida': partida})

