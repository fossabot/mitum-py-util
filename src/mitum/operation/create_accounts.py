import mitum.log as log
import rlp
from mitum.common import Hash, Hint, Text, bconcat
from mitum.hash import sha
from mitum.key.base import Keys
from mitum.operation import (Address, Amount, FactSign, Memo, Operation,
                             OperationBody, OperationFact, OperationFactBody)
from rlp.sedes import List


class CreateAccountsItem(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('ks', Keys),
        ('amounts', List((Amount,), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        amounts = d['amounts']

        bamounts = bytearray()
        for amount in amounts:
            bamounts += bytearray(amount.to_bytes())

        bkeys = d['ks'].to_bytes()
        bamounts = bytes(bamounts)

        log.rlog('CreateAccountsItem', log.LOG_TO_BYTES, '')
        return bconcat(bkeys, bamounts)


class CreateAccountsFactBody(OperationFactBody):
    fields = (
        ('h', Hint),
        ('token', Text),
        ('sender', Address),
        ('items', List((CreateAccountsItem,), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        items = d['items']

        bitems = bytearray()
        for i in items:
            bitems += bytearray(i.to_bytes())
        
        btoken = d['token'].to_bytes()
        bsender = d['sender'].to_bytes_hinted()
        bitems = bytes(bitems)

        log.rlog('CreateAccountsFactBody', log.LOG_TO_BYTES, '')
        return bconcat(btoken, bsender, bitems)

    def generate_hash(self):
        return sha.sha256(self.to_bytes())


class CreateAccountsFact(OperationFact):
    fields = (
        ('hs', Hash),
        ('body', CreateAccountsFactBody),
    )

    def hash(self):
        return self.as_dict()['hs']


class CreateAccountsBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', CreateAccountsFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        bfact_hs = d['fact'].hash().digest()
        bmemo = d['memo'].to_bytes()

        fact_sg = d['fact_sg']
        bfact_sg = bytearray()
        for sg in fact_sg:
            bfact_sg += bytearray(sg.to_bytes())
        bfact_sg = bytes(bfact_sg)

        log.rlog('CreateAccountsBody', log.LOG_TO_BYTES, '')
        return bconcat(bfact_hs, bfact_sg, bmemo)

    def generate_hash(self):
        return sha.sha256(self.to_bytes())


class CreateAccounts(Operation):
    fields = (
        ('hs', Hash),
        ('body', CreateAccountsBody),
    )

    def hash(self):
        return self.as_dict()['hs']

