from time import sleep
saldo = saqueQ = saldo_atual = 0
saques = []
while True:
    menu = '''
    ----------------------------
             BANCO DIO
    ----------------------------
    1 - DEPOSITO
    2 - SAQUE
    3 - EXTRATO
    4 - SAIR
    ---------------------------
    '''
    print(menu)
    opc = int(input('Qual sua opção?:'))


    if opc == 1:
        deposito = float(input('Qual o valor do deposito?:'))
        saldo += deposito
        if deposito > 0:
            print('Deposito corfimado!')
        else:
            print('valor invalido!')
    elif opc == 2:
        print(f'Saldo atual é de {saldo:.2f}R$')
        saque = float(input('Qual o valor do saque?:'))

        if saqueQ > 3:
            print('So é permitido 3 saques diarios!')
        elif saque > saldo:
            print('seu saldo e insuficiente!')
        elif saque < 0:
            print('valor do saque INVALIDO!')
        else:
            saldo -= saque
            saqueQ += 1
            saques.append(saque)
            print('Saque realizado com sucesso')
    elif opc == 3:
        print('\n ---EXTRATO---')
        if not saques:
            print('Nenhum saque realizado.')
        else:
            print('Saques realizados')
            for valor in saques:
                print(f'-R${valor:.2f}')
            print(f'Saldo atual é de R${saldo:.2f}')
            print('--------------')
    elif opc == 4:
        print('saindo...')
        sleep(1)
        break
    else:
        print('Opção INVALIDA!')
