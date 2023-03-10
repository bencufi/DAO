import json
import os

from .. import deployment_config as config
from .. import deploy_dao as dao

from brownie import (network, VotingEscrow)

DEPLOYMENTS_JSON = "scripts/" + network.main.show_active() + "/deployments.json"
GAUGE_JSON = "scripts/" + network.main.show_active() + "/gauge.json"

DAO_TOKEN = '0xFCCd4294BCd16c3959F2Eb94fb406632BfDE8b7E'
POLICYMAKER_REWARD = 10 ** 18

# name, type weight
GAUGE_TYPES = [
    ("Liquidity", 10 ** 18),
]

# lp token, default point rate, point proportion, reward token, reward rate, gauge weight
POOL_TOKENS = {
    "ETH": ("0x0F74Aa40B70c1555f34AB331720b6d8E9aBe90f8", 10 ** 22, 10 ** 17, "0x0000000000000000000000000000000000000000", 0, 0),
    "USDT": ("0xe27165c16EF606a5D1767aF558a7aEa58d15e443", 10 ** 22, 10 ** 17, "0x0000000000000000000000000000000000000000", 0, 0),
    "USDC": ("0x0a48A7b013b6B757963A44C1128C5C1B10281337", 10 ** 22, 10 ** 17, "0x0000000000000000000000000000000000000000", 0, 0),
}

def deploy():
    print(DEPLOYMENTS_JSON)
    admin = config.get_live_admin()
    print(f"admin {admin}")
    voting_escrow = dao.deploy_part_one(admin, DAO_TOKEN, config.REQUIRED_CONFIRMATIONS, DEPLOYMENTS_JSON)

    dao.deploy_part_two(
        admin, DAO_TOKEN, voting_escrow, POLICYMAKER_REWARD, GAUGE_TYPES, POOL_TOKENS, config.REQUIRED_CONFIRMATIONS, DEPLOYMENTS_JSON
    )

def add_gauge():
    admin = config.get_live_admin()

    with open(GAUGE_JSON) as fp:
        gauge_json = json.load(fp)

    with open(DEPLOYMENTS_JSON) as fp:
        deployments = json.load(fp)

    dao.add_gauge(admin, gauge_json["name"], deployments["Minter"], deployments["RewardPolicyMaker"],
            gauge_json["cToken"], eval(gauge_json["pointRate"]), eval(gauge_json["pointProportion"]),
            gauge_json["rewardToken"], eval(gauge_json["rewardRate"]), gauge_json["weight"],
            config.REQUIRED_CONFIRMATIONS, DEPLOYMENTS_JSON)

def deploy_helper():
    admin = config.get_live_admin()
    dao.deploy_reward_helper(admin, DEPLOYMENTS_JSON, config.REQUIRED_CONFIRMATIONS)

