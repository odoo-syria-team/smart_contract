from flask import Flask, render_template, request
from web3 import Web3

app = Flask(__name__)

# Connect to the local Ganache instance
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Replace with the deployed contract address

contract_address='0x5B38Da6a701c568545dCfcB03FcB875f56beddC4'
contract_abi = [
	{
		"inputs": [],
		"name": "getMessage",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_message",
				"type": "string"
			}
		],
		"name": "setMessage",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]  

simple_storage_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_message', methods=['POST'])
def set_message():
    
    message = request.form['message']
    simple_storage_contract.functions.setMessage(message).transact({'from': web3.eth.accounts[0]})
    return render_template('Dapp.html', message='Message set successfully!')

@app.route('/get_message')
def get_message():
    message = simple_storage_contract.functions.getMessage().call()
    return f'Message: {message}'
    

@app.route('/get_last_block_number',methods=['POST'])
def get_last_block_number():
    print()
    rpc_url = request.form['rpc_url']
    usdt_address=request.form['usdt_address']
    rpc_url = 'https://mainnet.infura.io/v3/391b8fdade8f48db9260d59c9564cf59'
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    # USDT token contract address and ABI
    usdt_address = '0xdac17f958d2ee523a2206206994597c13d831ec7'
    usdt_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        }
    ]

    # Convert the USDT address to checksum address
    usdt_address = Web3.to_checksum_address(usdt_address)

    usdt_contract = web3.eth.contract(address=usdt_address, abi=usdt_abi)
    

    # Address for which to check USDT balance
    address_to_check = '0x1234567890123456789012345678901234567890'

    def get_last_block_number():
        block_number = web3.eth.block_number
        return block_number
        

    def get_usdt_balance(address):
        balance = usdt_contract.functions.balanceOf(address).call()
        return balance
    
    return render_template('last_block_number.html', message={'number':get_last_block_number(),'usdt':get_usdt_balance(address_to_check)})


if __name__ == '__main__':
    app.run(debug=True)