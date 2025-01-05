from  time import sleep
import os
import json
import uuid

cores = {'vermelho':'\033[31m',
         'amarelo':'\033[33m',
         'verde':'\033[32m',
         'limpar':'\033[m'}

arquivo = os.path.join(os.path.dirname(__file__), 'database', 'agilstore.json')

def carregar_dados():
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as file:
            return json.load(file)
    else:
        return []

def salvar_dados(dados):
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    with open(arquivo, 'w') as file:
        json.dump(dados, file, indent=4)

def exibir_menu():
    os.system('cls')
    print('''
░█▀▀█ █▀▀▀ ░▀░ █░░ ▒█▀▀▀█ ▀▀█▀▀ █▀▀█ █▀▀█ █▀▀ 
▒█▄▄█ █░▀█ ▀█▀ █░░ ░▀▀▀▄▄ ░░█░░ █░░█ █▄▄▀ █▀▀ 
▒█░▒█ ▀▀▀▀ ▀▀▀ ▀▀▀ ▒█▄▄▄█ ░░▀░░ ▀▀▀▀ ▀░▀▀ ▀▀▀ 
''')
    print('''
       |  [1] Adicionar Produto    |
       |  [2] Listar Produtos      |
       |  [3] Atualizar Produto    |
       |  [4] Excluir Produto      |
       |  [5] Buscar Produto       |
       |  [6] Encerrar Programa    |
    ''')

def subtitulo(texto):
    os.system('cls')
    linha = '-'*(len(texto))
    print(linha)
    print(texto)
    print(linha)
    print()

def adicionar():
    lista_de_produtos = carregar_dados()
    subtitulo('Adicionar Produto')
    nome = input('Digite o nome do produto: ')
    categoria = input('Digite a categoria do produto: ')
    estoque = input('Digite a quantidade em estoque: ')
    preco = input('Digite o preço do produto: ')

    produto_id = str(uuid.uuid4().hex[:5])

    lista_de_produtos.append({'ID': produto_id ,'NOME': nome, 'CATEGORIA': categoria, 'ESTOQUE': estoque, 'PRECO': preco})
    salvar_dados(lista_de_produtos)
    print(f'Produto {nome} com ID: {produto_id}, {cores["verde"]} adicionado com sucesso! {cores["limpar"]}')
    voltar_menu()

def listar():
    lista_de_produtos = carregar_dados()
    if lista_de_produtos:
        subtitulo('Lista de Produtos')
        print(f'  {cores["amarelo"]}{'ID'.ljust(10)} | {'NOME'.ljust(20)} | {'CATEGORIA'.ljust(20)} | {'ESTOQUE'.ljust(10)} | {'PREÇO'.ljust(10)}{cores["limpar"]}\n')

        for produto in lista_de_produtos:
            produto_id = produto['ID']
            nome = produto['NOME']
            categoria = produto['CATEGORIA']
            estoque = produto['ESTOQUE']
            preco = produto['PRECO']
            print(f'- {produto_id.ljust(10)} | {nome.ljust(20)} | {categoria.ljust(20)} | {estoque.ljust(10)} | {preco.ljust(10)}')
    voltar_menu()

def atualizar():
    lista_de_produtos = carregar_dados()
    subtitulo('Atualizar Produto')
    id_atualizacao = input('Digite o ID do produto que deseja atualizar: ')
    produto_encontrado = None

    for produto in lista_de_produtos:
        if produto['ID'] == id_atualizacao:
            produto_encontrado = produto
            break

    if produto_encontrado:
        while True:
            print('''[1] Nome
[2] Categoria
[3] Estoque
[4] Preço''')
            opcao_atualizar = input('Digite o campo que deseja atualizar: ')

            match opcao_atualizar:
                case "1":
                    produto_encontrado['NOME'] = input("Digite o novo nome do produto: ")
                case "2":
                    produto_encontrado['CATEGORIA'] = input('Digite a nova categoria: ')
                case "3":
                    produto_encontrado['ESTOQUE'] = input('Digite a nova quantidade de estoque: ')
                case "4":
                    produto_encontrado['PRECO'] = input('Digite o novo valor do produto: ')
                case _:
                    print(f'{cores["vermelho"]}Opção inválida!{cores["limpar"]}')
                    continue

            salvar_dados(lista_de_produtos)
            print(f'{cores["verde"]}Atualização feita com sucesso!{cores["limpar"]}')

            pergunta_atualizacao = input('Deseja atualizar algo mais [S/N]? ')
            if pergunta_atualizacao in 'Ss':
                continue 
            else:
                break 

        voltar_menu() 
    else:
        print(f"{cores['vermelho']}Produto não encontrado!{cores['limpar']}")
        voltar_menu()
                    
def deletar():
    lista_de_produtos = carregar_dados()
    subtitulo('Remover Produto')
    id_deletar = input('Digite o ID do produto que deseja remover: ')
    
    deletar = [
        produto for produto in lista_de_produtos 
        if produto['ID'].strip() == id_deletar.strip()
    ]
    if deletar:
        print(f"{cores['verde']}Produto encontrado:{cores['limpar']}")
        for produto in deletar:
            print(f"- ID: {produto['ID']}\n- Nome: {produto['NOME']}\n- Categoria: {produto['CATEGORIA']}\n- Estoque: {produto['ESTOQUE']}\n- Preço: {produto['PRECO']} ")
            
            pergunta = input('Você comfirma a exclusão deste item [S/N] ? ')
            if pergunta in 'Ss':

                lista_de_produtos.remove(produto)  
                
                print("-" *25)
                print("Excluindo Produto...")
                sleep(2)
                print(f"{cores['verde']}Produto deletado com sucesso. ✨{cores['limpar']}")
                salvar_dados(lista_de_produtos)
                voltar_menu()
            else:
                print('Os dados deste produto sarão mantidos!')
                voltar_menu()
    else:
        print(f"😒 {cores['vermelho']}Nenhuma ONG encontrada com esse CNPJ.{cores['limpar']}")
        voltar_menu()

def buscar():
    lista_de_produtos = carregar_dados()
    subtitulo("Buscar Produto")
    buscando_produto = input("Digite o nome ou ID da ONG: ")

    busca = [
        produto for produto in lista_de_produtos 
        if produto['NOME'].lower() == buscando_produto.lower() or produto['ID'].strip() == buscando_produto.strip()
    ]

    if busca:
        print(f"{cores['verde']}Produto encontrado:{cores['limpar']}")
        for produto in busca:
            print(f"- ID: {produto['ID']}\n- Nome: {produto['NOME']}\n- Categoria: {produto['CATEGORIA']}\n- Estoque: {produto['ESTOQUE']}\n- Preço: {produto['PRECO']} ")
    else:
        print(f"😒 {cores['vermelho']}Nenhum produto encontrado com esse nome ou ID.{cores['limpar']}")

    voltar_menu()

def voltar_menu():
    input("\n--> Digite uma tecla para voltar ao menu: ")
    print("Voltando...")
    sleep(2)
    os.system('cls')
    exibir_opcoes()

def opcao_invalida():
    os.system('cls')
    print(f"{cores['vermelho']}Opção inválida! {cores['limpar']}Voltando ao menu...")
    sleep(2)
    voltar_menu()

def exibir_opcoes():
    try:
        exibir_menu()
        opcao = int(input("Informe uma opção: "))
    
        match(opcao):
            case 1:
                adicionar()
            case 2:
                listar()
            case 3:
                atualizar()
            case 4:
                deletar()
            case 5:
                buscar()
            case 6:
                print("Encerrando o Programa...")
                sleep(2)
            case _:
                opcao_invalida()
    except:
            opcao_invalida() 