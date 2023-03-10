# Bencu-dao

Vyper contracts used in the [Bencu](https://www.bencu.io/) Governance DAO.

## Overview

## Testing and Development

### Dependencies

- [python3](https://www.python.org/downloads/release/python-368/) version 3.6 or greater, python3-dev
- [vyper](https://github.com/vyperlang/vyper) version [0.2.12](https://github.com/vyperlang/vyper/releases/tag/v0.2.12)
- [brownie](https://github.com/iamdefinitelyahuman/brownie) - tested with version [1.14.6](https://github.com/eth-brownie/brownie/releases/tag/v1.14.6)
- [brownie-token-tester](https://github.com/iamdefinitelyahuman/brownie-token-tester) - tested with version [0.2.2](https://github.com/iamdefinitelyahuman/brownie-token-tester/releases/tag/v0.2.2)
- [ganache-cli](https://github.com/trufflesuite/ganache-cli) - tested with version [6.12.1](https://github.com/trufflesuite/ganache-cli/releases/tag/v6.12.1)

### Setup

To get started, first create and initialize a Python [virtual environment](https://docs.python.org/3/library/venv.html). Next, clone the repo and install the developer dependencies:

```bash
git clone https://github.com/bencufi/Bencu-dao.git
cd Bencu-dao
pip install -r requirements.txt
```

### Running the Tests

The test suite is split between [unit](tests/unitary) and [integration](tests/integration) tests. To run the entire suite:

```bash
brownie test
```

To run only the unit tests or integration tests:

```bash
brownie test tests/unitary
brownie test tests/integration
```

## Deployment

### 1. Initial Setup

[`deployment_config.py`](scripts/deployment_config.py) holds configurable / sensitive values related to the deployment. Before starting, you must set the following variables:

* Modify the `get_live_admin` function to return the primary admin [`Account`](https://eth-brownie.readthedocs.io/en/stable/api-network.html#brownie.network.account.Account) object. See the Brownie [account management](https://eth-brownie.readthedocs.io/en/stable/account-management.html) documentation for information on how to unlock local accounts.

### 2. Deploying the Bencu DAO

1. If you haven't already, install [Brownie](https://github.com/eth-brownie/brownie):

    ```bash
    pip install eth-brownie
    ```

2. Verify [`deploy_dao`](deploy_dao.py) by testing in on a forked mainnet:

    ```bash
    brownie run deploy_dao development --network mainnet-fork
    ```

3. Live deployment

    1. Create the new network folder under [./scripts](scripts) by copying one of the existing ones, the folder name is same as network id added to brownie.(example: brownie --network aribitrum-main, aribitrum-main is the network id)

    2. Modify deploy.py to add `DAO_TOKEN` and `POLICYMAKER_REWARD` addresses as well as define gauges to create by adding their lp token addresses and other settings

    3. Run the deploy.py script:

    ```bash
    brownie run aribitrum-main/deploy deploy --network aribitrum-main
    ```

    4. Once deployment done verify that a `deployment.json` file was created under the network folder, this file contains all contract addresses that have been deployed

    This deploys and links all of the core Bencu DAO contracts. **DO NOT MOVE OR DELETE THIS FILE**. It is required in later deployment stages.

### 3. Add new gauge

1. Bencu DAO contracts must be deployed, and the deployment.json must exist

2. In the network folder, modify `gauge.json`, set addresses and other parameters

3. Run the deploy.py script:

    ```bash
    brownie run aribitrum-main/deploy add_gauge --network aribitrum-main
    ```

4. Once deployment done the new gauge address added to `deployment.json` file.

## License

This project is licensed under the [MIT](LICENSE) license.
