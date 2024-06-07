""" Sample application file that shows the use of the user authetication 
    and authorization procedures and shows how to import them
"""

import logging  # only to handle a bcrypt / passlib levels incompatibility
from contextlib import asynccontextmanager  # to implement a FastAPI ligetime event

from fastapi import Depends, FastAPI

from isagog_userauth.database import init_db
from isagog_userauth.routers import user
from isagog_userauth.utils import get_current_user

logging.getLogger("passlib").setLevel(
    logging.ERROR
)  # to get around a bcrypt / passlib version problem


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=W0621,W0613
    """upon startup verify the database is created and populated"""
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)  # these are our /user/ routes


@app.get("/")
def read_root():
    """sample unprotected route"""
    return {"message": "This is an unprotected route"}


@app.get("/protected", dependencies=[Depends(get_current_user)])
def protected_route():
    """sample protected route"""
    return {"message": "You have access to this JWT protected resource."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
