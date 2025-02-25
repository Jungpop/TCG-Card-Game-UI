import os
import tkinter

from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU

from common.utility import get_project_root
from opengl_battle_field.entity.battle_field import BattleField
from opengl_battle_field.renderer.battle_field_frame_renderer import BattleFieldFrameRenderer
from opengl_battle_field_panel.battle_field_panel import BattleFieldPanel
from opengl_battle_field_unit.unit_card import UnitCard
from opengl_battle_field_pickable_card.pickable_card import PickableCard
from opengl_card_deck.card_deck import CardDeck
from opengl_energy_field.energy_field import EnergyField
from opengl_environment.environment import Environment
from opengl_field.field import Field
from opengl_hand_deck.hand_deck import HandDeck
from opengl_lost_zone.lost_zone import LostZone
from opengl_main_character.main_character import MainCharacter
from opengl_tomb.tomb import Tomb
from opengl_trap.trap import Trap


class BattleFieldFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.battle_field = BattleField()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.bind("<Configure>", self.on_resize)

        self.make_battle_field()

        project_root = get_project_root()
        print("프로젝트 최상위:", project_root)

        self.renderer = BattleFieldFrameRenderer(self.battle_field, self)

    def make_battle_field(self):
        project_root = get_project_root()

        battle_field_panel = BattleFieldPanel()
        battle_field_panel.init_shapes()
        self.battle_field.add_battle_field_panel(battle_field_panel)

        opponent_tomb = Tomb()
        opponent_tomb.init_shapes()
        self.battle_field.add_tomb(opponent_tomb)

        your_tomb = Tomb(local_translation=(1670, 780))
        your_tomb.init_shapes()
        self.battle_field.add_tomb(your_tomb)

        opponent_card_deck = CardDeck()
        opponent_card_deck.init_opponent_shapes()
        self.battle_field.add_card_deck(opponent_card_deck)

        your_card_deck = CardDeck()
        your_card_deck.init_your_shapes()
        self.battle_field.add_card_deck(your_card_deck)

        opponent_trap = Trap()
        opponent_trap.init_shapes()
        self.battle_field.add_trap(opponent_trap)

        your_trap = Trap(local_translation=(-1040, 480))
        your_trap.init_shapes()
        self.battle_field.add_trap(your_trap)

        opponent_lost_zone = LostZone()
        opponent_lost_zone.init_shapes()
        self.battle_field.add_lost_zone(opponent_lost_zone)

        your_lost_zone = LostZone(local_translation=(-1620, 300))
        your_lost_zone.init_shapes()
        self.battle_field.add_lost_zone(your_lost_zone)

        environment = Environment()
        environment.init_shapes()
        self.battle_field.add_environment(environment)

        energy_field = EnergyField()
        energy_field.init_shapes()
        self.battle_field.add_energy_field(energy_field)

        opponent_main_character = MainCharacter()
        opponent_main_character.init_opponent_main_character_shapes()
        self.battle_field.add_main_character(opponent_main_character)

        your_main_character = MainCharacter()
        your_main_character.init_your_main_character_shapes()
        self.battle_field.add_main_character(your_main_character)

        first_hand_deck = HandDeck(window=self, battle_field=self.battle_field)
        first_hand_deck.init_shapes(os.path.join(project_root, "local_storage", "card_images", "card1.png"))
        self.battle_field.add_pickable_hand_deck_base(first_hand_deck)

        your_field = Field()
        your_field.init_shapes()
        self.battle_field.add_pickable_field_base(your_field)

        # second_hand_deck = HandDeck(window=self, battle_field=self.battle_field)
        # second_hand_deck.init_shapes(os.path.join(project_root, "local_storage", "card_images", "card2.png"))
        # self.battle_field.add_pickable_hand_deck_base(second_hand_deck)

        # first_unit = UnitCard()
        # first_unit.init_shapes(os.path.join(project_root, "local_storage", "card_images", "card1.png"))
        #
        # second_unit = Card(local_translation=(500, 0))
        # second_unit.init_shapes(os.path.join(project_root, "local_storage", "card_images", "card2.png"), 2)
        #
        # self.battle_field.add_unit_card(first_unit)
        # self.battle_field.add_unit_card(second_unit)
    def apply_global_translation(self, translation):
        unit_card_list = self.battle_field.get_unit_card()
        for unit_card in unit_card_list:
            unit_shapes = unit_card.get_unit_shapes()
            for shape in unit_shapes:
                print("apply_global_translation")
                shape.global_translate(translation)

    def summon_units(self):
        project_root = get_project_root()
        unitList = self.battle_field.get_unit_card()
        unitCount = len(unitList)
        print(f"unitList : {unitList}")

        if unitCount > 2:
            placeX = 500 * (unitCount) * 3/(unitCount)
            #placeX = 1500.0
            self.resize_units()
            summon_unit = UnitCard(local_translation=(placeX, 0))
            summon_unit.init_shapes(
                os.path.join(project_root, "local_storage", "card_images", f"card{unitCount + 1}.png"))
            self.battle_field.add_unit_card(summon_unit)
            summon_unit.redraw_shapes_with_scale(unitCount)

        else:
            placeX = 500 * (unitCount)
            summon_unit = UnitCard(local_translation=(placeX, 0))
            summon_unit.init_shapes(
                os.path.join(project_root, "local_storage", "card_images", f"card{unitCount + 1}.png"))
            self.battle_field.add_unit_card(summon_unit)

    def draw_cards(self):
        project_root = get_project_root()
        handDeckList = self.battle_field.get_pickable_hand_deck_base()
        handDeckCount = len(handDeckList)

        if handDeckCount > 10:
            # placeX = 200 * (handDeckCount) * 3/(handDeckCount)
            placeX = 200 * (handDeckCount)
            draw_card = HandDeck(local_translation=(placeX, 0), window=self, battle_field=self.battle_field)
            draw_card.init_shapes(
                os.path.join(project_root, "local_storage", "card_images", f"card{handDeckCount + 1}.png"))
            self.battle_field.add_pickable_hand_deck_base(draw_card)
            print(f"{self.battle_field.add_pickable_hand_deck_base(draw_card)}")

        else:
            placeX = 200 * (handDeckCount)
            draw_card = HandDeck(local_translation=(placeX, 0), window=self, battle_field=self.battle_field)
            draw_card.init_shapes(
                os.path.join(project_root, "local_storage", "card_images", f"card{handDeckCount + 1}.png"))
            self.battle_field.add_pickable_hand_deck_base(draw_card)

    def resize_units(self):
        unitList = self.battle_field.get_unit_card()

        unitCount = len(unitList).__float__()
        print(f"unitCount : {unitCount}")

        for unit in unitList:
            unit.redraw_shapes_with_scale(unitCount)

    def initgl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glOrtho(0, self.width, self.height, 0, -1, 1)

    def toggle_visibility(self):
        unit_card_list = self.battle_field.get_unit_card()
        for unit_card in unit_card_list:
            unit_shapes = unit_card.get_unit_shapes()

            attached_tool_card = unit_shapes[0]
            attached_tool_card.set_visible(not attached_tool_card.get_visible())

            equipped_mark = unit_shapes[3]
            equipped_mark.set_visible(not equipped_mark.get_visible())

        self.redraw()

    def reshape(self, width, height):
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, width, height, 0)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def on_resize(self, event):
        self.reshape(event.width, event.height)

    def redraw(self):
        self.apply_global_translation((50, 50))
        self.tkSwapBuffers()
        self.after(100, self.renderer.render)
