from battle_field.state.attached_energy_info import AttachedEnergyInfoState
from battle_field.state.current_field_unit import CurrentFieldUnitState
from battle_field_fixed_card.fixed_field_card import FixedFieldCard


class OpponentFieldUnitRepository:
    __instance = None

    attached_energy_info = AttachedEnergyInfoState()

    current_field_unit_state = CurrentFieldUnitState()
    current_field_unit_card_object_list = []
    current_field_unit_x_position = []

    x_base = 265

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def place_field_unit(self, field_unit_id):
        self.current_field_unit_state.place_unit_to_field(field_unit_id)
        # print(f"Saved current field_unit state: {field_unit_id}")

    def create_field_unit_card(self, field_unit_id):
        index = len(self.current_field_unit_card_object_list)
        self.place_field_unit(field_unit_id)

        new_card = FixedFieldCard(local_translation=self.get_next_card_position(index))
        new_card.init_card(field_unit_id)
        new_card.set_index(index)

        self.current_field_unit_card_object_list.append(new_card)

    def get_next_card_position(self, index):
        current_y = 270
        x_increment = 170
        next_x = self.x_base + x_increment * index
        return (next_x, current_y)

    def get_current_field_unit_card_object_list(self):
        return self.current_field_unit_card_object_list

    def remove_current_field_unit_card(self, unit_index):
        # TODO: 이 부분 Memory Leak 발생 우려 (카드 구성 객체 정리 방안 구성 필요)
        del self.current_field_unit_card_object_list[unit_index]
        self.current_field_unit_state.delete_current_field_unit_list(unit_index)

