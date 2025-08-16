from litestar import Controller, get


class UserController(Controller):
    path = "/users"
    tags = ["Users"]

    @get("")
    async def g(
        self,
    ) -> dict[str, str]:
        return {"s": "s"}
