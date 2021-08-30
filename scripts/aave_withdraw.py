from brownie import accounts, config, interface, network
from web3 import Web3
from scripts.get_weth import get_weth
from scripts.aave_borrow import get_account, approve_erc20, get_lending_pool

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth(account=account)
    lending_pool = get_lending_pool()
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    available_to_withdraw = get_withdrawable_data(lending_pool, account)
    print("Withdrawing...")
    lending_pool.withdraw(
        erc20_address, available_to_withdraw, account.address, {"from": account}
    )
    print("Withdrawed!")


def get_withdrawable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        tlv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    print(total_collateral_eth)

    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")

    return total_collateral_eth
