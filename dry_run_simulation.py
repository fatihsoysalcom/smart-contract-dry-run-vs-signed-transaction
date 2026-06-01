import json

# --- Mock Blockchain/Smart Contract Environment ---
# In a real scenario, this would be an actual blockchain node or a testing framework.

class MockContract:
    def __init__(self):
        self.balance = 1000
        self.owner = "0x123"

    def transfer(self, from_addr, to_addr, amount):
        if amount > self.balance:
            raise Exception("Insufficient balance")
        self.balance -= amount
        print(f"[Contract] Transferred {amount} from {from_addr} to {to_addr}. New balance: {self.balance}")
        return True

class MockBlockchain:
    def __init__(self):
        self.contracts = {"0xContractAddr": MockContract()}

    def get_contract(self, address):
        return self.contracts.get(address)

# --- Simulation Logic ---

def simulate_transaction(transaction_details, blockchain):
    """Simulates a transaction without actually altering the blockchain state."""
    print("\n--- Simulating Transaction (Dry Run) ---")
    try:
        contract = blockchain.get_contract(transaction_details['to'])
        if not contract:
            print("[Simulation] Contract not found.")
            return False

        # Simulate the contract's internal logic based on the call
        # This is where the 'dry run' happens. We don't commit state changes.
        if transaction_details['method'] == 'transfer':
            # We can *check* if it would succeed, but not *actually* change the balance here.
            # For this mock, we'll just print what *would* happen.
            required_amount = transaction_details['params'][2]
            if required_amount > contract.balance: # Check against current mock state
                print(f"[Simulation] Transaction would fail: Insufficient balance (requires {required_amount}, has {contract.balance})")
                return False
            else:
                print(f"[Simulation] Transaction would succeed. Would transfer {required_amount}.")
                # IMPORTANT: We do NOT modify contract.balance here in a dry run.
                return True
        else:
            print("[Simulation] Unknown method.")
            return False

    except Exception as e:
        print(f"[Simulation] Transaction simulation failed: {e}")
        return False

def execute_signed_transaction(transaction_details, blockchain):
    """Executes a transaction, altering the blockchain state."""
    print("\n--- Executing Signed Transaction ---")
    try:
        contract = blockchain.get_contract(transaction_details['to'])
        if not contract:
            print("[Execution] Contract not found.")
            return False

        # Actual execution of the contract method
        if transaction_details['method'] == 'transfer':
            from_addr = transaction_details['from']
            to_addr = transaction_details['params'][1] # Assuming 'to' in params is recipient
            amount = transaction_details['params'][2]
            contract.transfer(from_addr, to_addr, amount) # This modifies state
            return True
        else:
            print("[Execution] Unknown method.")
            return False

    except Exception as e:
        print(f"[Execution] Transaction execution failed: {e}")
        return False

# --- Main Execution ---

if __name__ == "__main__":
    # Initialize a mock blockchain with a contract
    mock_blockchain = MockBlockchain()
    initial_contract_balance = mock_blockchain.get_contract("0xContractAddr").balance
    print(f"Initial contract balance: {initial_contract_balance}")

    # Transaction details for a transfer operation
    # In a real scenario, 'from' would be a signed address, and 'nonce' would be managed.
    transfer_tx = {
        "from": "0xSenderAddr",
        "to": "0xContractAddr",
        "method": "transfer",
        "params": ["0xSenderAddr", "0xRecipientAddr", 500] # from, to, amount
    }

    # 1. Dry Run Simulation
    simulation_success = simulate_transaction(transfer_tx, mock_blockchain)
    print(f"Dry run result: {'Success' if simulation_success else 'Failure'}")
    # Verify that the contract balance has NOT changed after dry run
    print(f"Contract balance after dry run: {mock_blockchain.get_contract('0xContractAddr').balance} (Should be unchanged)")

    # 2. Execute the 'signed' transaction (simulating it being sent and processed)
    # This is where the actual state change occurs.
    execution_success = execute_signed_transaction(transfer_tx, mock_blockchain)
    print(f"Execution result: {'Success' if execution_success else 'Failure'}")
    # Verify that the contract balance HAS changed after execution
    print(f"Contract balance after execution: {mock_blockchain.get_contract('0xContractAddr').balance} (Should be reduced)")

    # Example of a transaction that would fail in simulation and execution
    print("\n--- Testing a failing transaction ---")
    failing_transfer_tx = {
        "from": "0xSenderAddr",
        "to": "0xContractAddr",
        "method": "transfer",
        "params": ["0xSenderAddr", "0xRecipientAddr", 2000] # Amount exceeds balance
    }

    # Dry Run for failing tx
    simulation_success_fail = simulate_transaction(failing_transfer_tx, mock_blockchain)
    print(f"Dry run result for failing tx: {'Success' if simulation_success_fail else 'Failure'}")
    print(f"Contract balance after failing dry run: {mock_blockchain.get_contract('0xContractAddr').balance} (Should be unchanged)")

    # Execution for failing tx
    execution_success_fail = execute_signed_transaction(failing_transfer_tx, mock_blockchain)
    print(f"Execution result for failing tx: {'Success' if execution_success_fail else 'Failure'}")
    print(f"Contract balance after failing execution: {mock_blockchain.get_contract('0xContractAddr').balance} (Should be unchanged)")
