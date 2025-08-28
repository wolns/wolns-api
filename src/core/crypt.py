import asyncio

from passlib.context import CryptContext

password_crypt_context = CryptContext(schemes=["argon2"], deprecated="auto")


async def get_password_hash(password: str | bytes) -> str:
    return await asyncio.get_running_loop().run_in_executor(
        None, password_crypt_context.hash, password
    )


async def verify_password(plain_password: str | bytes, hashed_password: str) -> bool:
    valid, _ = await asyncio.get_running_loop().run_in_executor(
        None,
        password_crypt_context.verify_and_update,
        plain_password,
        hashed_password,
    )
    return bool(valid)
