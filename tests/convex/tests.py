from providers.abstracts.fabric import providerAbstractFabric
from overviews.abstracts.fabric import overviewAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


provider = BridgeConfigurator(
    abstractFabric=providerAbstractFabric,
    fabricKey='http',
    productKey='eth')\
    .produceProduct()

overviewContract = BridgeConfigurator(
    abstractFabric=overviewAbstractFabric,
    fabricKey='staking-pool-overview',
    productKey='convex')\
    .produceProduct()()\
    .setAddress(address='0x22eE18aca7F3Ee920D01F25dA85840D12d98E8Ca')\
    .setProvider(provider=provider)\
    .setTrader(trader=headTrader)\
    .create()


future = overviewContract.getOverview()
overview = future.result()

for aOverview in overview:
    assert isinstance(aOverview['symbol'], str)
    assert isinstance(aOverview['reserve'], (int, float))
    assert isinstance(aOverview['price'], (int, float))