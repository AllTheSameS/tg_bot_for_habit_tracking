import contextlib
from database.database import Base, engine


@contextlib.asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()





