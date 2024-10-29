from web3 import Web3
import time
import urllib3

# Kucingdao
print("\033[96m")
print("// _ __ _ ")
print("// | |/ / (_) ")
print("// | ' / ___ _ __ ___ _ _ ___ _ _ __ __ _ ")
print("// | < / _ \\| '_ ` _ \\| | | |/ __| | '_ \\ / _` |")
print("// | . \\ (_) | | | | | | |_| | (__| | | | | (_| |")
print("// |_|\_\___/|_| |_| |_|\__,_|\___|_|_| |_|\__, |")
print("// __/ |")
print("// |___/ ")
print("== Komunitas Kucing Terbang @komucing == ")
print("\033[0m")


# Connect to Base Sepolia testnet
base_rpc_url = "https://sepolia.base.org"  # Base Sepolia testnet RPC URL
http = urllib3.PoolManager()
web3 = Web3(Web3.HTTPProvider(base_rpc_url, request_kwargs={'timeout': 60}))

if web3.is_connected():
    print("Connected to Base Network")
else:
    print("Failed to connect")
    exit()

# Define wallet addresses and private key
monitor_wallet_address = Web3.to_checksum_address("xxx")  # Your wallet address
private_key = "xxx"  # Your private key
claim_contract_address = Web3.to_checksum_address("0x219BA210Ef31613390df886763099D0eD35aa6B8")  # Contract address to write claim
target_contract_address = Web3.to_checksum_address("0x66b43eF7f5316fA62CbEB2D9C2a66c57d8d74792")  # Token contract address
contract_abi = '[{"constant":false,"inputs":[],"name":"claimTokens","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'  # ABI for claimTokens method

# Instantiate the contract
contract = web3.eth.contract(address=claim_contract_address, abi=contract_abi)

def get_eth_balance():
    balance_wei = web3.eth.get_balance(monitor_wallet_address)
    balance_eth = web3.from_wei(balance_wei, 'ether')
    return balance_eth

def claim_tokens():
    try:
        nonce = web3.eth.get_transaction_count(monitor_wallet_address)
        txn = contract.functions.claimTokens().build_transaction({
            'chainId': web3.eth.chain_id,
            'gas': 200000,
            'maxFeePerGas': web3.to_wei('20', 'gwei'),
            'maxPriorityFeePerGas': web3.to_wei('2', 'gwei'),
            'nonce': nonce,
            'type': 2  # EIP-1559 transaction type
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f"Claim successful: {web3.to_hex(txn_hash)}")
        return True
    except Exception as e:
        print(f"Claim failed: {e}")
        return False

while True:
    eth_balance = get_eth_balance()
    print(f"Current ETH Balance: {eth_balance} ETH")
    if claim_tokens():
        print("Claim function executed successfully, waiting for 1 hour...")
    else:
        print("Claim function failed, trying again in 1 hour...")
    time.sleep(3600)
