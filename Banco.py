from time import sleep
from datetime import datetime, timezone, timedelta

# Configuração do fuso horário
tz = timezone(timedelta(hours=-3))



def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 0 if (soma % 11) < 2 else 11 - (soma % 11)

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 0 if (soma % 11) < 2 else 11 - (soma % 11)

    return cpf[-2:] == f"{digito1}{digito2}"


def obter_data_nascimento():
    while True:
        data_str = input("Data de nascimento (dd/mm/aaaa): ")
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y").date()
            if data > datetime.now().date():
                print("Data futura inválida!")
                continue
            return data.strftime("%d/%m/%Y")
        except ValueError:
            print("Formato inválido ou data inexistente!")


def validar_endereco(endereco):
    partes = endereco.split(',')
    if len(partes) != 4:
        return False
    cidade_estado = partes[3].strip().split('/')
    return len(cidade_estado) == 2 and len(cidade_estado[1].strip()) == 2


def cadastrar_cliente():
    cliente = {}

    # Nome
    while True:
        cliente['nome'] = input("Nome completo: ").strip()
        if len(cliente['nome'].split()) >= 2:
            break
        print("Insira nome e sobrenome!")

    # CPF
    while True:
        cpf = input("CPF (somente números): ").strip()
        if validar_cpf(cpf):
            cliente['cpf'] = ''.join(filter(str.isdigit, cpf))
            if cliente['cpf'] in usuarios:
                print("CPF já cadastrado!")
                continue
            break
        print("CPF inválido!")

    # Data de nascimento
    cliente['data_nascimento'] = obter_data_nascimento()

    # Endereço
    while True:
        endereco = input("Endereço (logradouro, numero, bairro, cidade/UF): ").strip()
        if validar_endereco(endereco):
            cliente['endereco'] = endereco
            break
        print("Formato inválido! Use: logradouro, numero, bairro, cidade/UF")

    return cliente


def listar_clientes():
    """Exibe todos os clientes cadastrados no sistema"""
    print('\n' + '-' * 40)
    print(f'{"CLIENTES CADASTRADOS".center(40)}')
    print('-' * 40)

    if not usuarios:
        print("Nenhum cliente cadastrado!")
        return

    for cpf, cliente in usuarios.items():
        print(f"\nCPF: {cpf}")
        print(f"Nome: {cliente['nome']}")
        print(f"Data de Nascimento: {cliente['data_nascimento']}")
        print(f"Endereço: {cliente['endereco']}")
        print('-' * 40)

    sleep(2)
def cadastrar_conta():
    if not usuarios:
        print("Nenhum cliente cadastrado!")
        return

    while True:
        cpf = input("CPF do titular (somente números): ").strip()
        cpf = ''.join(filter(str.isdigit, cpf))
        if cpf in usuarios:
            numero_conta = len(conta) + 1
            nova_conta = {
                'agencia': '0001',
                'numero_conta': numero_conta,
                'usuario': cpf
            }
            conta.append(nova_conta)
            print(f"Conta {numero_conta} criada com sucesso!")
            return
        print("CPF não encontrado! (Cadastre o cliente primeiro)")



def realizar_deposito(saldo, dep, saqueQ, depositos):
    if (dep + saqueQ) >= 10:
        print("\nLimite diário de transações atingido!")
        return saldo, dep

    valor = float(input("\nQual o valor do depósito?: "))
    sleep(1)

    if valor > 0:
        saldo += valor
        dep += 1
        hora_deposito = datetime.now(tz).strftime('%d/%m/%y %H:%M:%S')
        depositos.append((valor, hora_deposito))
        print("\nDepósito confirmado!")
    else:
        print("\nValor inválido! (Digite um valor positivo)")

    return saldo, dep


def realizar_saque(saldo, saqueQ, dep, saques):
    if (dep + saqueQ) >= 10:
        print("\nLimite diário de transações atingido!")
        return saldo, saqueQ

    print(f'\nSaldo atual: R$ {saldo:.2f}')
    valor = float(input('\nQual o valor do saque?: '))
    sleep(1)

    if valor <= 0:
        print('\nValor inválido! (Digite um valor positivo)')
    elif valor > saldo:
        print('\nSaldo insuficiente!')
    else:
        saldo -= valor
        saqueQ += 1
        hora_saque = datetime.now(tz).strftime('%d/%m/%y %H:%M:%S')
        saques.append((valor, hora_saque))
        print('\nSaque realizado com sucesso!')

    return saldo, saqueQ


def exibir_extrato(saques, saldo, dep, saqueQ, depositos):
    print('-' * 40)
    print(f'{"EXTRATO".center(40)}')
    print('-' * 40)
    data_extrato = datetime.now(tz).strftime('%d/%m/%y %H:%M:%S')
    print(f'Data do extrato: {data_extrato}')
    print(f'Saldo atual: R$ {saldo:.2f}')

    if not depositos:
        print('Nenhum deposito realizado')
    else:
        print('\nUltimos Depositos')
        for valor, data_hora in depositos[-3:]:  # Mostra últimos 3
            print(f'- R$ {valor:.2f} em {data_hora}')

    if not saques:
        print('Nenhum saque realizado.')
    else:
        print('\nÚltimos saques:')
        for valor, data_hora in saques[-3:]:  # Mostra últimos 3
            print(f'- R$ {valor:.2f} em {data_hora}')

    print(f'\nTotal de transações hoje: {dep + saqueQ}/10')
    print('-' * 40)
    sleep(5)


# ==============================================
# PROGRAMA PRINCIPAL
# ==============================================

saldo = saqueQ = dep = 0
saques = []
depositos = []
usuarios = {}  # Dicionário para clientes (CPF como chave)
conta = []  # Lista de contas bancárias
data_fim = None

while True:
    # Verificação de mudança de dia
    data = datetime.now(timezone.utc).astimezone(tz)
    data_atual = data.date()

    if data_fim is not None and data_atual > data_fim:
        saqueQ = 0
        dep = 0
        saques = []
        depositos = []
        print('\n--- Novo dia: contadores de transações zerados ---')
        sleep(1)

    data_fim = data_atual

    # Menu
    menu = '''
    ----------------------------
             BANCO DIO
    ----------------------------
    1 - DEPÓSITO
    2 - SAQUE
    3 - EXTRATO
    4 - CADASTRAR CLIENTE
    5 - CRIAR CONTA
    6 - LISTAR CLIENTES
    0 - SAIR
    ---------------------------
    '''
    print(menu)

    try:
        opc = int(input('Qual sua opção?: '))
    except ValueError:
        print('\nOpção inválida!')
        continue

    # Operações
    if opc == 1:
        saldo, dep = realizar_deposito(saldo, dep, saqueQ, depositos)

    elif opc == 2:
        saldo, saqueQ = realizar_saque(saldo, saqueQ, dep, saques)

    elif opc == 3:
        exibir_extrato(saques, saldo, dep, saqueQ, depositos)

    elif opc == 4:
        cliente = cadastrar_cliente()
        usuarios[cliente['cpf']] = cliente
        print("\nCliente cadastrado com sucesso!")
        sleep(1)

    elif opc == 5:
        cadastrar_conta()
        sleep(1)

    elif opc == 6:
        listar_clientes()

    elif opc == 0:
        print('\nSaindo...')
        sleep(1)
        break

    else:
        print('\nOpção inválida!')

    sleep(1)
