def create_account_data_from_response(response):
    k = "accountInformation"
    account_info = dict()

    chosen_name = response[k]["chosenName"]
    account_info["account_name"] = chosen_name if chosen_name != "" else response[k]["accountName"]

    account_info["account_number"] = f'{response[k]["clearingNumber"]}-{response[k]["accountNumber"]}'

    account_info["available_amount"] = response[k]["availableAmount"]

    account_info["transactions"] = \
    [
        {
            "date": t["transactionDate"],
            "ledger_date": t["ledgerDate"],
            "text": t["transactionText"],
            "amount": t["transactionAmount"]
        } for t in response["inlaAccountTransactions"]
    ]

    return account_info


if __name__ == '__main__':
    import pickle
    import json

    with open('tmp/txns.pickle', 'rb') as f:
        loaded_object = pickle.load(f)

    pass
    test_account_info = create_account_data_from_response(loaded_object)

    pass

    print(json.dumps(test_account_info, indent=2))
