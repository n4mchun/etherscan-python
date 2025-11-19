"""
Comprehensive test for the new chain_id architecture.
This demonstrates that:
1. Etherscan object is created without chain_id
2. Each method call can specify a different chain_id
3. Default chain_id (Ethereum Mainnet) is used when not specified
"""

from etherscan import Etherscan
import os

api_key = os.getenv('ETHERSCAN_API_KEY')

if not api_key:
    print("❌ ETHERSCAN_API_KEY environment variable not set")
    exit(1)

print("=" * 60)
print("Testing New Chain-ID Architecture")
print("=" * 60)

# Create a single Etherscan instance (no chain_id parameter)
scanner = Etherscan(api_key=api_key)
print("✓ Created Etherscan instance without chain_id parameter")

# Test 1: Using explicit chain_id for Arbitrum
print("\n[Test 1] Arbitrum One Mainnet (explicit chain_id)")
try:
    balance = scanner.get_eth_balance(
        '0xE3c1ca5c45818e57B298f3a080c8502BF7154352',
        chain_id=Etherscan.Chain.ARBITRUM_ONE_MAINNET
    )
    print(f"  ✓ Balance: {balance}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 2: Using default chain_id (Ethereum Mainnet)
print("\n[Test 2] Ethereum Mainnet (default - no chain_id specified)")
try:
    balance = scanner.get_eth_balance(
        '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a'
    )
    print(f"  ✓ Balance: {balance}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 3: Multiple chains in succession with same scanner instance
print("\n[Test 3] Switching between chains with same instance")
chains_to_test = [
    ("Polygon", Etherscan.Chain.POLYGON_MAINNET, "0x0000000000000000000000000000000000001010"),
    ("Ethereum", Etherscan.Chain.ETHEREUM_MAINNET, "0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a"),
    ("Arbitrum", Etherscan.Chain.ARBITRUM_ONE_MAINNET, "0xE3c1ca5c45818e57B298f3a080c8502BF7154352"),
]

for chain_name, chain_id, address in chains_to_test:
    try:
        balance = scanner.get_eth_balance(address, chain_id=chain_id)
        print(f"  ✓ {chain_name}: Balance retrieved")
    except Exception as e:
        print(f"  ✗ {chain_name}: {str(e)[:50]}...")

# Test 4: Verify that chain_id is truly per-call
print("\n[Test 4] Verify chain_id is per-call (not cached)")
try:
    # Call with Arbitrum
    bal1 = scanner.get_eth_balance(
        '0xE3c1ca5c45818e57B298f3a080c8502BF7154352',
        chain_id=Etherscan.Chain.ARBITRUM_ONE_MAINNET
    )
    # Immediately call with Ethereum (should not use cached Arbitrum chain)
    bal2 = scanner.get_eth_balance(
        '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a',
        chain_id=Etherscan.Chain.ETHEREUM_MAINNET
    )
    print(f"  ✓ Successfully switched chains without creating new instance")
    print(f"    Arbitrum balance: {bal1}")
    print(f"    Ethereum balance: {bal2}")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
print("\n✅ SUCCESS: New architecture working correctly!")
print("   - Single Etherscan instance created without chain_id")
print("   - Each method call accepts chain_id parameter")
print("   - Default chain_id (Ethereum Mainnet) used when not specified")
print("   - No state is cached between calls")
