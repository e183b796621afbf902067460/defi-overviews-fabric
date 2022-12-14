from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.curve.overview import CurveFarmingPoolOverview
from overviews.protocols.pancakeswap.overview import PancakeSwapFarmingPoolOverview
from overviews.protocols.sushiswap.overview import SushiSwapFarmingPoolOverview
from overviews.protocols.ellipsis.overview import EllipsisFarmingPoolOverview


class FarmingPoolOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Farming Overview handler for {protocol}')
        return overview


farmingPoolOverviewFabric = FarmingPoolOverviewFabric()

farmingPoolOverviewFabric.addProduct(protocol='curve', overview=CurveFarmingPoolOverview)
farmingPoolOverviewFabric.addProduct(protocol='pancakeswap', overview=PancakeSwapFarmingPoolOverview)
farmingPoolOverviewFabric.addProduct(protocol='sushiswap', overview=SushiSwapFarmingPoolOverview)
farmingPoolOverviewFabric.addProduct(protocol='ellipsis', overview=EllipsisFarmingPoolOverview)
