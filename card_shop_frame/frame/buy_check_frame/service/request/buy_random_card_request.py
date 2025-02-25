from common.protocol import CustomProtocol


class BuyRandomCardRequest:
    def __init__(self, sessionInfo, race):
        self.__protocolNumber = CustomProtocol.BUY_CARD.value
        self.__sessionInfo = sessionInfo
        self.__race = race

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "race": self.__race
        }

    def __str__(self):
        return f"BuyRandomCardRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo}race={self.__race})"
