import sys
import time
import tkinter


from battle_lobby_frame.controller.battle_lobby_frame_controller_impl import BattleLobbyFrameControllerImpl
from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl
from battle_lobby_frame.service.request.request_deck_name_list_for_battle import RequestDeckNameListForBattle
from lobby_frame.repository.lobby_menu_frame_repository_impl import LobbyMenuFrameRepositoryImpl
from lobby_frame.service.lobby_menu_frame_service import LobbyMenuFrameService
from lobby_frame.service.request.card_list_request import CardListRequest
from lobby_frame.service.request.check_game_money_request import CheckGameMoneyRequest
from matching_window.controller.matching_window_controller_impl import MatchingWindowControllerImpl
from lobby_frame.service.request.exit_request import ExitRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl


imageWidth = 256
imageHeight = 256


class LobbyMenuFrameServiceImpl(LobbyMenuFrameService):
    __instance = None
    __switchFrameWithMenuName = None
    __rootWindow = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__lobbyMenuFrameRepository = LobbyMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            cls.__instance.__battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()
            cls.__instance.__battleLobbyFrameController = BattleLobbyFrameControllerImpl.getInstance()
            cls.__instance.__matchingWindowController = MatchingWindowControllerImpl.getInstance()
            cls.__instance.__cardShopFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.card_data_list = []

    def createLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        self.__switchFrameWithMenuName = switchFrameWithMenuName
        self.__rootWindow = rootWindow

        lobbyMenuFrame = self.__lobbyMenuFrameRepository.createLobbyMenuFrame(rootWindow)


        label_text = "EDDI TCG Card Battle"
        label = tkinter.Label(lobbyMenuFrame, text=label_text, font=("Helvetica", 72), bg="black", fg="white",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")  # 가운데 정렬

        battle_entrance_button = tkinter.Button(lobbyMenuFrame, text="대전 입장", bg="#2E2BE2", fg="white",
                                                width=36, height=2)
        battle_entrance_button.place(relx=0.5, rely=0.35, anchor="center")

        def onClickEntrance(event):
            #rootWindow.after(3000, self.__waitForPrepareBattle)
            self.__matchingWindowController.makeMatchingWindow(rootWindow)
            self.__matchingWindowController.matching(rootWindow)



        battle_entrance_button.bind("<Button-1>", onClickEntrance)

        my_card_button = tkinter.Button(lobbyMenuFrame, text="내 카드", bg="#2E2BE2", fg="white", width=36,
                                        height=2)
        my_card_button.place(relx=0.5, rely=0.5, anchor="center")

        card_shop_button = tkinter.Button(lobbyMenuFrame, text="상점", bg="#2E2BE2", fg="white",
                                          width=36, height=2)
        card_shop_button.place(relx=0.5, rely=0.65, anchor="center")

        exit_button = tkinter.Button(lobbyMenuFrame, text="종료", bg="#C62828", fg="white", width=36, height=2)
        exit_button.place(relx=0.5, rely=0.8, anchor="center")

        battle_field_button = tkinter.Button(lobbyMenuFrame, text="전장", bg="#2E2BE2", fg="white",
                                          command=lambda: switchFrameWithMenuName("battle-field"), width=36,
                                          height=2)
        battle_field_button.place(relx=0.2, rely=0.65, anchor="center")

        def onClickExit(event):
            try:
                responseData = self.__lobbyMenuFrameRepository.requestProgramExit(
                    ExitRequest())

                print(f"responseData: {responseData}")

                if responseData and responseData.get("does_client_exit_success") is True:
                    rootWindow.destroy()
                    sys.exit()
                else:
                    print("응답이 잘못 되었음")
            except Exception as e:
                print(f"An error occurred: {e}")

        exit_button.bind("<Button-1>", onClickExit)

        def onClickMyCard(event):
            try:
                session_info = self.__sessionRepository.get_session_info()
                if session_info is not None:
                    responseData = self.__lobbyMenuFrameRepository.requestAccountCardList(
                        CardListRequest(session_info))

                    print(f"responseData: {responseData}")

                    if responseData is not None:
                        server_data = responseData.get("card_id_list")

                        for i, number in enumerate(server_data):
                            for key in server_data[i].keys():
                                self.card_data_list.append(int(key))
                                print(f"서버로 부터 카드 정보 잘 받았니?:{self.card_data_list}")

                        switchFrameWithMenuName("my-card-main")

                    else:
                        print("Invalid or missing response data.")

            except Exception as e:
                print(f"An error occurred: {e}")

        my_card_button.bind("<Button-1>", onClickMyCard)

        def onClickCardShop(event):
            try:
                responseData = self.__lobbyMenuFrameRepository.requestCheckGameMoney(CheckGameMoneyRequest
                                                                                     (self.__sessionRepository.get_session_info()))

                print(f"responseData: {responseData}")

                if responseData:
                    self.__cardShopFrameRepository.setMyMoney(responseData.get("account_point"))
                    from card_shop_frame.service.card_shop_service_impl import CardShopMenuFrameServiceImpl
                    CardShopMenuFrameServiceImpl.getInstance().findMyMoney()
                    switchFrameWithMenuName("card-shop-menu")
                else:
                    print("checkGameMoney responseData not found")

            except Exception as e:
                print(f"An error occurred: {e}")

        card_shop_button.bind("<Button-1>", onClickCardShop)

        return lobbyMenuFrame


    def get_card_data_list(self):
        return self.card_data_list

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        self.__lobbyMenuFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        self.__lobbyMenuFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)

    def switchToBattleLobby(self, windowToDestroy):
        windowToDestroy.destroy()
        try:
            deckNameResponse = self.__battleLobbyFrameRepository.requestDeckNameList(
                RequestDeckNameListForBattle(
                    self.__sessionRepository.get_session_info()
                )
            )
            if deckNameResponse is not None and deckNameResponse != "":
                print(f"switchToBattleLobby : 호출됨 {deckNameResponse}")
                self.__battleLobbyFrameController.startCheckTime()
                self.__battleLobbyFrameController.createDeckButtons(deckNameResponse, self.__switchFrameWithMenuName)
                self.__switchFrameWithMenuName("battle-lobby")
        except Exception as e:
            print(f"switchToBattleLobby Error: {e}")
