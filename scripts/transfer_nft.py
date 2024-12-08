from algosdk import account, mnemonic # type: ignore
from algosdk.v2client import algod # type: ignore
from algosdk.future.transaction import AssetTransferTxn # type: ignore
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

def transfer_nft(receiver_address):
    try:
        # Initialize Algod client
        algod_client = algod.AlgodClient(
            "",
            os.getenv('ALGOD_SERVER')
        )

        # Get creator account
        creator_mnemonic = os.getenv('CREATOR_MNEMONIC')
        private_key = mnemonic.to_private_key(creator_mnemonic)
        sender = account.address_from_private_key(private_key)
        
        # Get asset ID
        asset_id = int(os.getenv('NFT_ASSET_ID'))
        
        # Get network parameters
        params = algod_client.suggested_params()
        
        # Create transfer transaction
        txn = AssetTransferTxn(
            sender=sender,
            sp=params,
            receiver=receiver_address,
            amt=1,
            index=asset_id
        )
        
        # Sign transaction
        signed_txn = txn.sign(private_key)
        
        # Submit transaction
        tx_id = algod_client.send_transaction(signed_txn)
        print(f"Sent transaction: {tx_id}")
        
        # Wait for confirmation
        try:
            confirmed_txn = algod_client.pending_transaction_info(tx_id)
            print(f"Successfully transferred NFT to: {receiver_address}")
            print(f"Transaction ID: {tx_id}")
            print(f"View on AlgoExplorer: https://testnet.algoexplorer.io/tx/{tx_id}")
        except Exception as e:
            print(f"Error waiting for confirmation: {e}")
            
    except Exception as e:
        print(f"Error during transfer: {e}")

if __name__ == "__main__":
    # Replace with the receiver's address
    receiver_address = "ACTUAL_RECEIVER_ADDRESS_HERE"
    transfer_nft(receiver_address) 