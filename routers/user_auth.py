from fastapi import APIRouter, HTTPException, Response

from models.user_auth import Login, Register
from internal.auth import register_user, authenticate_user

user_auth = APIRouter()


@user_auth.post("/login")
async def user_login(login_details: Login, response: Response):
    try:
        login_details_dict = login_details.model_dump()
        user_token = await authenticate_user(login_details_dict)
        response.set_cookie("x-session-token", user_token)
        return "User Logged in Successfully"

    except HTTPException as http_execption:
        raise http_execption

    except Exception as e:
        raise HTTPException(500, e)


@user_auth.post("/register")
async def user_register(user_details: Register):
    try:
        user_details_dict = user_details.model_dump()
        await register_user(user_details_dict)
        return "User created successfully"

    except Exception as e:
        raise HTTPException(500, e)


@user_auth.get("/logout")
async def user_logout(response: Response):
    try:
        response.delete_cookie("x-session-token")
        return "User logged out successfully"
    except Exception as e:
        raise HTTPException(500, e)
