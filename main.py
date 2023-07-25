import textwrap

def menu():
    menu = """\n
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tCriar conta
    [5]\tMostrar contas
    [6]\tCriar Usuário
    [7]\tSair
    =>"""
    return input(textwrap.dedent(menu))


def deposit(balance, amount, extract, /):
    if amount > 0:
        balance += amount
        extract += f"Depósito: R$ {amount:.2f}\n"
        print("\nDepósito realizado!")
    else:
        print("\nValor inválido.")

    return balance, extract


def withdraw(*, balance, amount, extract, limit, withdraws, withdraw_amount):
    exceeded_amount = amount > balance
    exceeded_limit = amount > limit
    exceeded_withdraws = withdraw_amount >= withdraws

    if exceeded_amount:
        print("\nSaldo insuficiente.")

    elif exceeded_limit:
        print("\nLimite de saque excedido.")

    elif exceeded_withdraws:
        print("\nLimite de saques atingido.")

    elif amount > 0:
        balance -= amount
        extract += f"Saque: R$ {amount:.2f}\n"
        withdraw_amount += 1
        print("\nSaque realizado!")

    else:
        print("\nValor inválido.")

    return balance, extract


def show_extract(balance, /, *, extract):
    print("\n==============EXTRACT==============")
    print("Sem movimentações" if not extract else extract)
    print(f"\nSaldo: R${balance:.2f}")
    print("=====================================")


def create_user(users):
    cpf = input("Informe o CPF (somente números): ")
    user = filter_user(cpf, users)

    if user:
        print("\nUsuário já cadastrado!")

    name = input("Informe o nome completo: ")
    birthdate = input("Informe a data de nascimento: ")
    address = input("Informe o endereço (logradouro, nr, bairro, cidade/estado): ")

    users.append({"name":name, "birthdate":birthdate, "cpf":cpf, "address":address})

    print("Usuário criado com sucesso!")


def filter_user(cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None


def create_account(agency, acc_num, users):
    cpf = input("Informe o CPF do usuário: ")
    user = filter_user(cpf, users)

    if user:
        print("Conta criada com sucesso!")
        return {"agency":agency, "acc_number":acc_num, "user":user}

    print("Usuário não encontrado!")


def list_acc(accs):
    for acc in accs:
        line = f"""
        Agência: {acc['agency']}
        C/C: {acc['acc_number']}
        Titular: {acc['user']['name']}
        """
    print("=" * 100)
    print(textwrap.dedent(line))


def main():
    WITHDRAWS = 3
    AGENCY = "0001"

    balance = 0
    limit = 500
    extract = ""
    withdraw_amount = 0
    users = []
    accs = []

    while True:
        option = menu()

        if option == "1":
            amount = float(input("Informe o valor do depósito: "))

            balance, extract = deposit(balance, amount, extract)

        elif option == "2":
            amount = float(input("Informe o valor do saque: "))

            balance, extract = withdraw(
                balance=balance,
                amount=amount,
                extract=extract,
                limit=limit,
                withdraws=WITHDRAWS,
                withdraw_amount=withdraw_amount,
            )

        elif option == "3":
            show_extract(balance, extract=extract)

        elif option == "4":
            acc_number = len(accs) + 1
            acc = create_account(AGENCY, acc_number, users)

            if acc:
                accs.append(acc)

        elif option == "5":
            list_acc(accs)

        elif option == "6":
            create_user(users)

        elif option == "7":
            break

        else:
            print("Operação inválida, selecione novamente.")


main()
