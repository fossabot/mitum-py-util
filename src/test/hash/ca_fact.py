import mitum.hint as HINT
from mitum.common import Hint, Text, Int
from mitum.constant import VERSION
from mitum.operation import Amount, Address
from mitum.operation.create_accounts import CreateAccountsItem, CreateAccountsFactBody, CreateAccountsFact
from mitum.key.base import BaseKey, Key, Keys, KeysBody

import base58


EXPECTED_KEYS_HASH = "4UM4CN8MZNyv26TK84486CX5X8bu9EUYbsWz5ovRsp1M"
EXPECTED_FACT_HASH = "DB9AKEj6BKDpBeTnDGBrewECW7CYmYkJPU24VEdypinQ"

print()

k = "rd89GxTnMP91bZ1VepbkBrvB77BSQyQbquEVBy2fN1tV"

single_key = Key(
    Hint(HINT.MC_KEY, VERSION),
    BaseKey(Hint(HINT.BTC_PBLCKEY, VERSION), k),
    Int(100),
)
key_list = list()
key_list.append(single_key)

keys_body = KeysBody(
    Hint(HINT.MC_KEYS, VERSION),
    Int(100),
    key_list,
)

keys = Keys(
    keys_body.generate_hash(),
    keys_body,
)

single_amount = Amount(
    Hint(HINT.MC_AMOUNT, VERSION),
    Int(1000),
    Text("MCC"),
)

amount_list = list()
amount_list.append(single_amount)

single_item = CreateAccountsItem(
    Hint(HINT.MC_CREATE_ACCOUNTS_SINGLE_AMOUNT, VERSION),
    keys,
    amount_list,
)

item_list = list()
item_list.append(single_item)

fact_body = CreateAccountsFactBody(
    Hint(HINT.MC_CREATE_ACCOUNTS_OP_FACT, VERSION),
    Text("MjAyMS0wNS0xMlQwNzo1MTowNC40NDI0NTRa"),
    Address(Hint(HINT.MC_ADDRESS, VERSION), Text("8PdeEpvqfyL3uZFHRZG5PS3JngYUzFFUGPvCg29C2dBn")),
    item_list,
)


fact = CreateAccountsFact(
    fact_body.generate_hash(),
    fact_body,
)

print('[CHECK] KEYS_HASH: ' + str(EXPECTED_KEYS_HASH == base58.b58encode(keys.hash()).decode()))
print('[CHECK] FACT_HASH: ' + str(EXPECTED_FACT_HASH == base58.b58encode(fact.hash()).decode()))