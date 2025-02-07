from database.account_repository import AccountRepository


def main():
    """
    Lists all accounts with their balances.
    :return: prints all accounts with their balances
    """
    account_repo = AccountRepository()

    accounts = account_repo.get_all_accounts()

    if accounts:
        print("List of all accounts:")
        print("-" * 40)
        for account in accounts:
            print(f"Account: {account['account_number']} | Balance: {account['balance']}")
        print("-" * 40)
    else:
        print("No accounts found in the database.")


if __name__ == "__main__":
    main()
