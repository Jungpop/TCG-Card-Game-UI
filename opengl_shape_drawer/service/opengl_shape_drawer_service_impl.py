from opengl_shape_drawer.repository.shape_repository_impl import ShapeRepositoryImpl
from opengl_shape_drawer.service.opengl_shape_drawer_service import OpenglShapeDrawerService


class OpenglShapeDrawerServiceImpl(OpenglShapeDrawerService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__shapeRepository = ShapeRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def create_rectangle(self, color, vertices):
        print("OpenglShapeDrawerServiceImpl: create_rectangle()")
        self.__shapeRepository.create_rectangle(color, vertices)

    def get_shape_drawer_scene(self):
        print("OpenglShapeDrawerServiceImpl: get_shape_drawer_scene()")
        return self.__shapeRepository.get_opengl_shape_drawer_scene()





