from litestar import Controller


class TrackController(Controller):
    path = "/tracks"
    tags = ["Tracks"]
