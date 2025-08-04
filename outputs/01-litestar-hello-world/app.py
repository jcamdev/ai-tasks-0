from litestar import Litestar, get


@get("/")
async def hello_world() -> dict[str, str]:
    return {"message": "Hello, World!"}


@get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}


app = Litestar(route_handlers=[hello_world, health_check])