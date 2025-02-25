import math

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GLUT import glutSwapBuffers

from opengl_shape.circle import Circle
from opengl_shape.shape import Shape

from PIL import Image
from OpenGL import GL


# class CircleImage(Shape):
#     def __init__(self, image_data, center, radius, global_translation=(0, 0), local_translation=(0, 0)):
#         super().__init__([center], global_translation, local_translation)
#         self.image_data = image_data
#         self.center = center
#         self.radius = radius
#         self.is_visible = True
#         self.texture_id = None
#
#     def set_visible(self, visible):
#         self.is_visible = visible
#
#     def get_visible(self):
#         return self.is_visible
#
#     def draw(self):
#         if self.get_visible():
#             white_rect = Circle(color=(1.0, 1.0, 1.0, 1.0),
#                                 center=[self.vertices[0][0], self.vertices[0][1]],
#                                 radius=self.radius,
#                                 local_translation=self.local_translation,
#                                 global_translation=self.global_translation)
#             white_rect.draw()
#
#             image_info = self.image_data
#
#             if image_info is not None:
#                 width, height, image_data = image_info
#                 # image = image.convert("RGB")
#                 #image_data = image.tobytes("raw", "RGB", 0, 1)  # issue
#
#                 if self.texture_id is None:
#                     self.texture_id = glGenTextures(1)
#                     glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
#                     glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE,
#                                  image_data)
#                     glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
#                     glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
#
#             GL.glEnable(GL.GL_TEXTURE_2D)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
#
#
#             GL.glBegin(GL.GL_TRIANGLE_FAN)
#             glColor3f(1.0, 1.0, 1.0)
#
#             for i in range(360):
#                 theta = 2.0 * math.pi * i / 360
#                 x = self.radius * math.cos(theta) + self.vertices[0][0] + self.global_translation[0] + \
#                     self.local_translation[0] - 1
#                 y = self.radius * math.sin(theta) + self.vertices[0][1] + self.global_translation[1] + \
#                     self.local_translation[1] - 1
#
#                 GL.glTexCoord2f(0.5 + 0.5 * math.cos(theta), 0.5 + 0.5 * math.sin(theta))# issue
#                 glVertex2f(x, y)
#             GL.glEnd()
#
#             GL.glDisable(GL.GL_TEXTURE_2D)
#             glBindTexture(GL.GL_TEXTURE_2D, 0)

# class CircleImage(Shape):
#     def __init__(self, image_data, center, radius, global_translation=(0, 0), local_translation=(0, 0)):
#         super().__init__([center], global_translation, local_translation)
#         self.image_data = image_data
#         self.center = center
#         self.radius = radius
#         self.is_visible = True
#         self.texture_id = None
#
#     def set_visible(self, visible):
#         self.is_visible = visible
#
#     def get_visible(self):
#         return self.is_visible
#
#     def delete_texture(self):
#         if self.texture_id is not None:
#             GL.glDeleteTextures([self.texture_id])
#             self.texture_id = None
#
#     def draw(self):
#         if self.get_visible():
#             white_rect = Circle(color=(1.0, 1.0, 1.0, 1.0),
#                                 center=[self.vertices[0][0], self.vertices[0][1]],
#                                 radius=self.radius,
#                                 local_translation=self.local_translation,
#                                 global_translation=self.global_translation)
#             white_rect.draw()
#
#             image_info = self.image_data
#
#             if image_info is not None:
#                 width, height, image_data = image_info
#
#                 if self.texture_id is None:
#                     self.texture_id = glGenTextures(1)
#                     glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
#                     glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE,
#                                  image_data)
#                     glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
#                     glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
#
#             GL.glEnable(GL.GL_TEXTURE_2D)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
#
#             GL.glBegin(GL.GL_TRIANGLE_FAN)
#             glColor3f(1.0, 1.0, 1.0)
#
#             for i in range(360):
#                 theta = 2.0 * math.pi * i / 360
#                 x = self.radius * math.cos(theta) + self.vertices[0][0] + self.global_translation[0] + \
#                     self.local_translation[0] - 1
#                 y = self.radius * math.sin(theta) + self.vertices[0][1] + self.global_translation[1] + \
#                     self.local_translation[1] - 1
#
#                 GL.glTexCoord2f(0.5 + 0.5 * math.cos(theta), 0.5 + 0.5 * math.sin(theta))
#                 glVertex2f(x, y)
#
#             GL.glEnd()
#
#             GL.glDisable(GL.GL_TEXTURE_2D)
#             glBindTexture(GL.GL_TEXTURE_2D, 0)
#
#             self.delete_texture()  # 텍스처 삭제

class CircleImage(Shape):
    def __init__(self, image_data, center, radius, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__([center], global_translation, local_translation)
        self.radius = radius
        self.center = center
        # print("CircleImage -> center = ", self.center)
        self.initial_center = [center]

        # print(f"CircleImage vertices: {self.vertices}")
        self.image_data = image_data
        self.is_visible = True
        self.texture_id = None
        self.texture_initialized = False

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def update_circle_vertices(self, calculated_initial_vertices):
        # print(f"update_circle_vertices: {calculated_initial_vertices}")
        # print(f"update_circle_vertices[0]: {calculated_initial_vertices[0]}")
        # print(f"update_circle_vertices[0][0]: {calculated_initial_vertices[0][0]}")
        # print(f"update_circle_vertices[0][1]: {calculated_initial_vertices[0][1]}")
        self.center = calculated_initial_vertices
        self.vertices = [[calculated_initial_vertices[0], calculated_initial_vertices[1]]]
        # print(f"update_circle_vertices -> vertices: {self.vertices}")
        # print(f"update_circle_vertices -> vertices[0]: {self.vertices[0]}")

    def delete_texture(self):
        if self.texture_id is not None:
            GL.glDeleteTextures([self.texture_id])
            self.texture_id = None

    def draw(self):
        if self.get_visible():
            # x = self.radius * min(self.width_ratio, self.height_ratio) + \
            #     self.vertices[0][0] * self.width_ratio + \
            #     self.global_translation[0] + \
            #     self.local_translation[0] * self.width_ratio - 1
            #
            # y = self.radius * min(self.width_ratio, self.height_ratio) + \
            #     self.vertices[0][1] * self.height_ratio + \
            #     self.global_translation[1] + \
            #     self.local_translation[1] * self.height_ratio - 1

            # print(f"type(radius): {type(self.radius)}")
            self.vertices = self.get_vertices()

            white_circle = Circle(color=(1.0, 1.0, 1.0, 1.0),
                                  center=self.center,
                                  radius=self.radius,
                                  local_translation=self.local_translation,
                                  global_translation=self.global_translation)
            # print(f"circle_image -> radius: {self.radius}, "
            #       # f"convert_radius: {self.radius * min(self.width_ratio, self.height_ratio) * math.cos(2.0 * math.pi * 0 / 100)}, "
            #       # f"width_ratio: {self.width_ratio}, "
            #       # f"height_ratio: {self.height_ratio}, "
            #       f"local_translation: {self.local_translation}, "
            #       f"vertices[0][0]: {self.vertices[0][0]}, "
            #       f"vertices[0][1]: {self.vertices[0][1]}, "
            #       f"center: {self.center}")
            white_circle.set_width_ratio(self.width_ratio)
            white_circle.set_height_ratio(self.height_ratio)
            white_circle.draw()

            image_info = self.image_data

            if image_info is not None:
                width, height, image_data = image_info

                if self.texture_id is None:
                    self.texture_id = glGenTextures(1)

                glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
                if not self.texture_initialized:
                    glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE,
                                 image_data)
                    glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
                    glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
                    self.texture_initialized = True

                GL.glEnable(GL.GL_TEXTURE_2D)
                GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)

                GL.glBegin(GL.GL_TRIANGLE_FAN)
                glColor3f(1.0, 1.0, 1.0)

                # print(f"circle_image -> x: {self.radius * min(self.width_ratio, self.height_ratio) * math.cos(2.0 * math.pi * 0 / 360) + self.vertices[0][0] * self.width_ratio + self.global_translation[0] + self.local_translation[0] * self.width_ratio - 1}, y: {self.radius * min(self.width_ratio, self.height_ratio) * math.sin(2.0 * math.pi * 0 / 360) + self.vertices[0][1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio - 1}")

                for i in range(360):
                    theta = 2.0 * math.pi * i / 360
                    # x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + self.vertices[0][0] * self.width_ratio  + self.global_translation[0] + \
                    #     self.local_translation[0] * self.width_ratio  - 1
                    # y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + self.vertices[0][1] * self.height_ratio + self.global_translation[1] + \
                    #     self.local_translation[1] * self.height_ratio - 1

                    # x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + \
                    #     self.vertices[0][0] * self.width_ratio + \
                    #     self.global_translation[0] + \
                    #     self.local_translation[0] - 1
                    #
                    # y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + \
                    #     self.vertices[0][1] * self.height_ratio + \
                    #     self.global_translation[1] + \
                    #     self.local_translation[1] - 1

                    x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + \
                        self.vertices[0][0] * self.width_ratio + \
                        self.global_translation[0] + \
                        self.local_translation[0] * self.width_ratio - 1

                    y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + \
                        self.vertices[0][1] * self.height_ratio + \
                        self.global_translation[1] + \
                        self.local_translation[1] * self.height_ratio - 1

                    GL.glTexCoord2f(0.5 + 0.5 * math.cos(theta), 0.5 + 0.5 * math.sin(theta))
                    glVertex2f(x, y)

                GL.glEnd()

                GL.glDisable(GL.GL_TEXTURE_2D)
                glBindTexture(GL.GL_TEXTURE_2D, 0)

