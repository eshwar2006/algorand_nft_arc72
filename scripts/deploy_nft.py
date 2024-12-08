from algosdk import account, mnemonic # type: ignore
from algosdk.v2client import algod # type: ignore
from algosdk.future.transaction import AssetConfigTxn # type: ignore
import os
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

def deploy_nft():
    try:
        # Initialize Algod client
        algod_client = algod.AlgodClient(
            "",  # No API key needed for AlgoNode
            os.getenv('ALGOD_SERVER'),
            headers={"User-Agent": "PyAlgorand"}
        )

        # Get account from mnemonic
        creator_mnemonic = os.getenv('CREATOR_MNEMONIC')
        private_key = mnemonic.to_private_key(creator_mnemonic)
        sender = account.address_from_private_key(private_key)
        
        print(f"Deploying from account: {sender}")

        # Get network parameters
        params = algod_client.suggested_params()
        
        # Create the Asset Creation Transaction
        txn = AssetConfigTxn(
            sender=sender,
            sp=params,
            total=int(os.getenv('NFT_TOTAL_SUPPLY')),
            default_frozen=False,
            unit_name=os.getenv('NFT_UNIT_NAME'),
            asset_name=os.getenv('NFT_NAME'),
            manager=sender,
            reserve=sender,
            freeze=sender,
            clawback=sender,
            url=os.getenv('NFT_METADATA_URL'),
            metadata_hash=b"",  # Optional: Add metadata hash if needed
            strict_empty_address_check=False,
            decimals=0  # NFTs should have 0 decimals
        )

        # Sign transaction
        signed_txn = txn.sign(private_key)

        # Submit transaction
        tx_id = algod_client.send_transaction(signed_txn)
        print(f"Submitted transaction: {tx_id}")

        # Wait for confirmation
        try:
            # Wait up to 4 rounds for confirmation
            rounds_to_wait = 4
            for i in range(rounds_to_wait):
                tx_info = algod_client.pending_transaction_info(tx_id)
                if "confirmed-round" in tx_info:
                    asset_id = tx_info['asset-index']
                    print(f"\nSuccess! Created NFT with Asset ID: {asset_id}")
                    print(f"View on AlgoExplorer: https://testnet.algoexplorer.io/asset/{asset_id}")
                    return asset_id
                algod_client.status_after_block(algod_client.status()["last-round"] + 1)
            print("Transaction not confirmed after 4 rounds")
            return None

        except Exception as e:
            print(f"Error waiting for confirmation: {e}")
            return None

    except Exception as e:
        print(f"Error during deployment: {e}")
        return None

if __name__ == "__main__":
    print("Deploying Pokemon NFT to Algorand TestNet...")
    asset_id = deploy_nft()
    
    if asset_id:
        print("\nNext steps:")
        print("1. Save your Asset ID in your .env file")
        print("2. View your NFT on AlgoExplorer")
        print("3. Opt-in to the asset before receiving it")
    else:
        print("\nDeployment failed. Please check the error messages above.") 