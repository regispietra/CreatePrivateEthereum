# Create Private Ethereum Blockchain

Quickly set up and run a local private Ethereum blockchain.

Customizable Genesis block (difficulty, initial balance, ...)

Connected to Ethereum/Mist Wallet, where you can deploy and test your contracts.
Note : Open your wallet after starting your blockchain

## This script provides easy functions to pilot geth:

 * ./pgeth.py init: this function create the blockchain with an account. Use it the first time.
 * ./pgeth.py start: this function starts geth daemon and mining. Use it when you want to use geth.
 * ./pgeth.py stop: this functions stops geth. Use it not to burn your CPU on stupid blocks.
 * ./pgeth.py destroy: A function to delete quickly your private blockchain.

 ## Private key

Initial password set to "apasswordtochange" in mypassword.txt

## Contributors

Laurent MALLET
Regis PIETRASZEWSKI

