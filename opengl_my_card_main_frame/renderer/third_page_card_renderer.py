from OpenGL import GL

class ThirdPageCardRenderer:
    def __init__(self, scene, window):
        self.scene = scene
        self.window = window

    def render(self):
        print("3번 째 페이지 렌더러 호출")
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # 배경 및 사이드에 있는 나의 덱 화면
        for image_element in self.scene.my_card_background:
            print(f"이미지 그리기: {image_element}")
            self._render_shape(image_element)

        # 나의 카드 텍스트
        # for text in self.scene.text_list:
        #     self._render_shape(text)

        # 버튼 도형
        for button in self.scene.button_list:
            print(f"버튼 그리기: {button}")
            self._render_shape(button)

        for card in self.scene.card_list[16:24]:
            attached_tool_card = card.get_tool_card()
            attached_tool_card.draw()

            pickable_card_base = card.get_pickable_card_base()
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()
            for attached_shape in attached_shape_list:
                attached_shape.draw()

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()