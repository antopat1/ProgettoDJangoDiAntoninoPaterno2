from web3 import Web3
w3= Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/ab69f53ad93a4ba7bf63485df2a338d9'))
account=w3.eth.account.create()
privateKey=account.privateKey.hex()
address=account.address
print(f"Il tuo indirizzo è:{address}\n Questa invece è la tua chiave privata: {privateKey}")