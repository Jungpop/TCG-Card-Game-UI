import abc


class MyGameMoneyFrameService(abc.ABC):
    @abc.abstractmethod
    def createMyGameMoneyUiFrame(self, rootWindow, getGameMoneyInfo):
        pass
