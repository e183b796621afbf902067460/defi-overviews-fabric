from web3.exceptions import BadFunctionCallOutput

from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod

from defi.protocols.aave.contracts.LendingPool import AaveLendingPoolV2Contract
from defi.protocols.aave.tokens.AToken import ATokenContract
from defi.protocols.aave.tokens.VariableDebtToken import VariableDebtTokenContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract


class AaveV2LendingPoolOverview(IInstrumentOverview, AaveLendingPoolV2Contract):
    _RAY: int = 10 ** 27
    _SECONDS_PER_YEAR: int = 31536000

    # @threadmethod
    def getOverview(self, *args, **kwargs):
        overview: list = list()

        reservesList: list = self.getReservesList()
        for reserveAddress in reservesList:
            try:
                reserveData: tuple = self.getReserveData(asset=reserveAddress)
            except BadFunctionCallOutput:
                continue

            liquidityRate, variableBorrowRate = reserveData[3], reserveData[4]
            depositAPR, variableBorrowAPR = liquidityRate / self._RAY, variableBorrowRate / self._RAY

            depositAPY = ((1 + (depositAPR / self._SECONDS_PER_YEAR)) ** self._SECONDS_PER_YEAR) - 1
            variableBorrowAPY = ((1 + (variableBorrowAPR / self._SECONDS_PER_YEAR)) ** self._SECONDS_PER_YEAR) - 1

            aTokenAddress, variableDebtTokenAddress = reserveData[7], reserveData[9]

            aToken: ATokenContract = ATokenContract()\
                .setAddress(address=aTokenAddress)\
                .setProvider(provider=self.provider)\
                .create()
            variableDebtToken: VariableDebtTokenContract = VariableDebtTokenContract()\
                .setAddress(address=variableDebtTokenAddress)\
                .setProvider(provider=self.provider)\
                .create()
            t: ERC20TokenContract = ERC20TokenContract()\
                .setAddress(address=reserveAddress)\
                .setProvider(provider=self.provider)\
                .create()

            try:
                tSymbol: str = t.symbol()
            except OverflowError:
                continue

            aTokenDecimals: int = aToken.decimals()
            variableDebtTokenDecimals: int = variableDebtToken.decimals()

            totalReserveSize: float = aToken.totalSupply() / 10 ** aTokenDecimals
            totalBorrowSize: float = variableDebtToken.totalSupply() / 10 ** variableDebtTokenDecimals

            tPrice: float = self.trader.getPrice(major=tSymbol, vs='USD')

            aOverview: dict = {
                'symbol': tSymbol,
                'reserve': totalReserveSize,
                'borrow': totalBorrowSize,
                'price': tPrice,
                'depositAPY': depositAPY * 100,
                'borrowAPY': variableBorrowAPY * 100
            }
            overview.append(aOverview)
        return overview


class AaveV2LendingPoolAllocationOverview(IInstrumentOverview, AaveLendingPoolV2Contract):

    @threadmethod
    def getOverview(self, address: str, *args, **kwargs):
        overview: list = list()

        userConfiguration: str = bin(self.getUserConfiguration(address=address)[0])[2:]
        reservesList: list = self.getReservesList()
        for i, mask in enumerate(userConfiguration[::-1]):
            reserveTokenAddress: str = reservesList[i // 2]
            try:
                reserveData: tuple = self.getReserveData(asset=reserveTokenAddress)
            except BadFunctionCallOutput:
                continue
            if mask == '1':
                if i % 2:
                    reserveToken: ERC20TokenContract = ERC20TokenContract()\
                                .setAddress(address=reserveTokenAddress)\
                                .setProvider(provider=self.provider)\
                                .create()
                    try:
                        reserveTokenSymbol: str = reserveToken.symbol()
                    except OverflowError:
                        continue
                    reserveTokenPrice: float = self.trader.getPrice(major=reserveTokenSymbol, vs='USD')

                    aTokenAddress: str = reserveData[7]
                    aToken: ERC20TokenContract = ERC20TokenContract()\
                                .setAddress(address=aTokenAddress)\
                                .setProvider(provider=self.provider)\
                                .create()
                    aTokenDecimals: int = aToken.decimals()
                    collateral: int = aToken.balanceOf(address=address) / 10 ** aTokenDecimals

                    aOverview: dict = {
                        'symbol': reserveTokenSymbol,
                        'amount': collateral,
                        'price': reserveTokenPrice
                    }
                    overview.append(aOverview)
        return overview
