from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl

from image_shape.circle_kinds import CircleKinds
from image_shape.circle_number_image import CircleNumberImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class SupportCardHandler:
    __instance = None

    __preDrawedImageInstance = PreDrawedImage.getInstance()
    __cardInfoRepository = CardInfoFromCsvRepositoryImpl.getInstance()

    # 에너지 부스트(2), 덱 드로우(20), 유닛 검색(30), 상대 필드 에너지 파괴(36)
    __supportCardHandlerTable = {}

    __yourDeckRepository = YourDeckRepository.getInstance()
    __yourFieldUnitRepository = YourFieldUnitRepository.getInstance()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__supportCardHandlerTable[2] = cls.__instance.energy_boost_from_deck_as_possible
            cls.__instance.__supportCardHandlerTable[20] = cls.__instance.draw_card_from_deck
            cls.__instance.__supportCardHandlerTable[30] = cls.__instance.search_unit_from_deck
            cls.__instance.__supportCardHandlerTable[36] = cls.__instance.destroy_opponent_field_energy
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def getSupportCardHandler(self, card_id):
        print(f"cardType을 찾아 옵니다 -> card_id: {card_id}")
        if self.__supportCardHandlerTable[card_id] is not None:
            return self.__supportCardHandlerTable[card_id]
        else:
            print(f"이 카드 타입({card_id}) 를 처리 할 수 있는 함수가 없습니다.")

    def energy_boost_from_deck_as_possible(self, target_unit_index):
        print("에너지 부스팅")

        print(f"deck state: {self.__yourDeckRepository.get_current_deck_state().get_current_deck()}")
        found_list = self.__yourDeckRepository.find_card_from_deck(93, 2)
        print(f"found_list: {found_list}")

        found_energy_count = len(found_list)
        self.__yourFieldUnitRepository.attach_energy(target_unit_index, found_energy_count)

        print(f"attached energy info: {self.__yourFieldUnitRepository.get_attached_energy_info().get_energy_at_index(target_unit_index)}")
        print(f"deck state: {self.__yourDeckRepository.get_current_deck_state().get_current_deck()}")

        if found_energy_count > 0:
            fixed_target_unit = self.__yourFieldUnitRepository.find_field_unit_by_index(target_unit_index)
            fixed_card_base = fixed_target_unit.get_fixed_card_base()
            fixed_card_attached_shape_list = fixed_card_base.get_attached_shapes()

            for fixed_card_attached_shape in fixed_card_attached_shape_list:
                if isinstance(fixed_card_attached_shape, CircleNumberImage):
                    if fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                        fixed_card_attached_shape.set_image_data(
                            self.__preDrawedImageInstance.get_pre_draw_number_image(len(found_list)))
                        print(f"changed energy: {fixed_card_attached_shape.get_circle_kinds()}")

            for index in range(found_energy_count):
                card_race_circle = fixed_target_unit.creat_fixed_card_energy_race_circle(
                    color=(0, 0, 0, 1),
                    vertices=(0, ((index + 1) * 10) + 20),
                    local_translation=fixed_card_base.get_local_translation())
                fixed_card_base.set_attached_shapes(card_race_circle)

    def draw_card_from_deck(self):
        print("덱에서 드로우")
        return 3

    def search_unit_from_deck(self):
        print("덱에서 유닛 검색")
        pass

    def destroy_opponent_field_energy(self):
        print("상대의 필드 에너지를 파괴합니다")
        pass
