from litestar import Controller


class SingerController(Controller):
    path = "/singers"
    tags = ["Singers"]
