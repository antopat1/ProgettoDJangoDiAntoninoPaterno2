from web3 import Web3

def sendTransaction (message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/ab69f53ad93a4ba7bf63485df2a338d9'))
    address='0xA08f2a96B57A6048d3425CD54179300Ead9B8EC5'
    privateKey='0x6225d1e806a7ae47f455883dd630ee7bcc7a438baaa4c72a7b14b1063ad6644b'
    nonce=w3.eth.getTransactionCount(address)
    gasPrice=w3.eth.gasPrice
    value=w3.toWei(0,'ether')
    signedTx=w3.eth.account.signTransaction(dict(nonce=nonce,gasPrice=gasPrice,gas=100000,to='0x0000000000000000000000000000000000000000',value=value,data=message.encode('utf-8')),privateKey)
    tx=w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId=w3.toHex(tx)
    return txId