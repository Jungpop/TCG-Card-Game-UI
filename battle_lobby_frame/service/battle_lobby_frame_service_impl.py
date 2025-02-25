import tkinter

from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field_function.controller.battle_field_function_controller_impl import BattleFieldFunctionControllerImpl
from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl
from battle_lobby_frame.service.battle_lobby_frame_service import BattleLobbyFrameService
from battle_lobby_frame.service.request.request_deck_card_list import RequestDeckCardList
from session.repository.session_repository_impl import SessionRepositoryImpl
from utility.timer import Timer
from utility.image_generator import ImageGenerator

from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU, GLUT


# from discarded.battle_room_list_frame.repository import BattleRoomListFrameRepositoryImpl


class BattleLobbyFrameServiceImpl(BattleLobbyFrameService):
    __instance = None
    __battleLobbyFrame = None
    __onClickEventList = []
    __imageGenerator = None
    __deck_selection_time = 30
    __timer = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            cls.__instance.__battleFieldFunctionController = BattleFieldFunctionControllerImpl.getInstance()
            # cls.__instance.__battleFieldStateRepository = BattleFieldRepository.getInstance()
            cls.__instance.__yourHandRepository = YourHandRepository.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createBattleLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        self.__battleLobbyFrame = self.__battleLobbyFrameRepository.createBattleLobbyFrame(rootWindow)

        label = tkinter.Label(self.__battleLobbyFrame, text="WATING ROOM FOR BATTLE", font=("Helvetica", 50, "bold"),
                              fg="#FFFFFF", bg="#000000")
        label.place(relx=0.5, rely=0.15, anchor="center")

        enterButton = tkinter.Button(self.__battleLobbyFrame, text="입장", font=("Arial", 20))
        enterButton.place(relx=0.5, rely=0.85, anchor="center", width=180, height=60)

        def onClickEnter(event=None):
            try:
                response = self.__battleLobbyFrameRepository.requestCardList(
                    RequestDeckCardList(self.__battleLobbyFrameRepository.getCurrentDeckId(),
                                        self.__sessionRepository.get_session_info())
                )

                print(f"BattleLobbyFrameService response: {response}")
                if response is not None and 'hand_card_list' in response:
                    self.__battleLobbyFrameRepository.exitBattleLobby()

                    hand_card_list = response['hand_card_list']

                    print(f"hand_card_list: {hand_card_list}")
                    self.__yourHandRepository.save_current_hand_state(hand_card_list)

                    # opponentId = response.get("opponentSessionId")
                    # TODO : battleField 도메인을 호출하여 프레임을 전환해야합니다.
                    switchFrameWithMenuName('battle-field')
                    # TODO : 또한 opponentId를 넘겨주어 상대편 아이디가 표시되게 합니다.
                    # self.__battleFieldService.someFunction(opponentId)

            except Exception as e:
                print(e)

        enterButton.bind("<Button-1>", onClickEnter)

        self.__timer = Timer(rootWindow=self.__battleLobbyFrame, time=self.__deck_selection_time, relx=0.5, rely=0.25,
                             expiredEvent=onClickEnter)

        # exitButton = tkinter.Button(self.__battleLobbyFrame,
        #                             text="나가기", font=("Arial", 20))
        # exitButton.place(relx=0.8, rely=0.85, anchor="center", width=180, height=60)
        #
        # def onClickExit(event):
        #     self.__battleLobbyFrameRepository.exitBattleLobby()
        #     switchFrameWithMenuName('lobby-menu')
        #
        # exitButton.bind("<Button-1>", onClickExit)

        return self.__battleLobbyFrame

    # TODO : Controller가 호출해야함.
    def createBattleLobbyMyDeckButton(self, request: dict = None, switchFrameWithMenuName = None):
        # request의 형태는 {ACCOUNT_DECK_LIST:[{’1’:’ㅋㅋㅋ’}, {’2’: ‘아이고’], {’3’:’이것은 세 번째 덱 이름’}]}

        # request = {"ACCOUNT_DECK_LIST": [{"1": 'ㅋㅋㅋㅋ'}, {"23": "아이고"}, {'3': '이것은 세 번째 덱 이름'}]}
        #request = {"ACCOUNT_DECK_LIST": [{"1":{ 'ㅋㅋㅋㅋ':'True'}}, {"23": {"아이고":'True'}}, {'3': {'이것은 세 번째 덱 이름':'False'}}]}
        # request = {"ACCOUNT_DECK_LIST":[]}

        imageGenerator = ImageGenerator.getInstance()
        if request:
            def relX(j):
                return 0.3 if j % 2 == 0 else 0.7

            for deckDataList in request.values():
                if len(deckDataList) == 0:
                    # Todo: 사용 할 수 있는 덱이 없다면 즉시 항복을 하고 패배합니다.
                    self.__timer.editTimer(3, lambda : self.callSurrenderAndExitLobby(switchFrameWithMenuName))
                else:
                    for i, deckData in enumerate(deckDataList):
                        for deckId, deckName in deckData.items():
                                generatedImage = imageGenerator.getUnselectedDeckImage()
                                deck = tkinter.Canvas(self.__battleLobbyFrame, highlightthickness=0,
                                                      highlightbackground="#93FFE8")
                                deck.create_image(150, 40, image=generatedImage)
                                deck.create_text(150, 40, text=deckName, font=("Arial", 15))
                                deck.pack()
                                deck.place(relx=relX(i), rely=0.4 + (i // 2 * 0.15),
                                           anchor="center", width=300, height=80)

                                def onClick(event, _deck):
                                    self.__battleLobbyFrameRepository.selectDeck(_deck)

                                deck.bind("<Button-1>",
                                          lambda event, current_deck=deck: onClick(event, current_deck))
                                self.__battleLobbyFrameRepository.addDeckToDeckList(deck)
                                self.__battleLobbyFrameRepository.addDeckIdToDeckIdList(deckId)

    def checkTimeForDeckSelection(self):
        self.__timer.resetTimer()
        self.__timer.startTimer()

    def callSurrenderAndExitLobby(self, switchFrameWithMenuName):
        self.__battleFieldFunctionController.callSurrender(switchFrameWithMenuName)

        self.__battleLobbyFrameRepository.exitBattleLobby()

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        self.__battleLobbyFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        self.__battleLobbyFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)
