import time


def authorise_bank_account(data):
    return True, str(int(time.time()*10000))[2:14]


def money_transfer(bank_reference, amount):
    return True, str(int(time.time()*10000))[2:14]