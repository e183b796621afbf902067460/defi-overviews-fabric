from overviews.protocols.aave.overview import (
    AaveV2LendingPoolOverview, AaveV2LendingPoolAllocationOverview, AaveV2LendingPoolBorrowOverview,
    AaveV2LendingPoolIncentiveOverview
)

from defi.protocols.sturdy.contracts.LendingPool import SturdyLendingPoolContract
from defi.protocols.sturdy.contracts.StakedTokenIncentivesController import SturdyStakedTokenIncentivesControllerContract

from head.bridge.configurator import BridgeConfigurator

from providers.abstracts.fabric import providerAbstractFabric


class SturdyLendingPoolOverview(SturdyLendingPoolContract, AaveV2LendingPoolOverview):
    pass


class SturdyLendingPoolAllocationOverview(SturdyLendingPoolContract, AaveV2LendingPoolAllocationOverview):
    pass


class SturdyLendingPoolBorrowOverview(SturdyLendingPoolContract, AaveV2LendingPoolBorrowOverview):
    pass


class SturdyLendingPoolIncentiveOverview(SturdyLendingPoolContract, AaveV2LendingPoolIncentiveOverview):
    _controllerContract: SturdyStakedTokenIncentivesControllerContract = SturdyStakedTokenIncentivesControllerContract()

    _providers: dict = {
        'eth': {
            'provider': BridgeConfigurator(
                abstractFabric=providerAbstractFabric,
                fabricKey='http',
                productKey='eth')\
                .produceProduct()
        }
    }

    _controllerAddresses: dict = {
        _providers['eth']['provider']:
            {
                'controller': '0xA3e9B5e1dc6B24F296FfCF9c085E2546A466b883'
            }
    }
