import os
import uuid
import secrets
import urllib.parse
from typing import Optional
import httpx
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
import models
from redis_client import set_session, redis_client

router = APIRouter()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "mock_id")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "mock_secret")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_EMAILS_URL = "https://api.github.com/user/emails"

@router.get("/login")
async def login(request: Request):
    if GITHUB_CLIENT_ID == "mock_id":
        # Mock auth flow for testing without real credentials
        return RedirectResponse(url="/auth/mock_callback")
    
    state = secrets.token_urlsafe(32)
    await redis_client.set(f"oauth_state:{state}", "1", ex=600)
    
    redirect_uri = str(request.url_for('auth_callback'))
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": "read:user user:email",
        "state": state,
    }
    auth_url = f"{GITHUB_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url=auth_url)

@router.get("/callback")
async def auth_callback(
    request: Request,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    error_description: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    if error:
        err_msg = error_description or error
        return RedirectResponse(url=f"{FRONTEND_URL}/?error={urllib.parse.quote(err_msg)}")
    
    if not code:
        return RedirectResponse(url=f"{FRONTEND_URL}/?error={urllib.parse.quote('Authorization code missing')}")
    
    if state:
        is_valid = await redis_client.get(f"oauth_state:{state}")
        if not is_valid:
            return RedirectResponse(url=f"{FRONTEND_URL}/?error={urllib.parse.quote('Invalid or expired OAuth state')}")
        await redis_client.delete(f"oauth_state:{state}")
    
    try:
        redirect_uri = str(request.url_for('auth_callback'))
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                GITHUB_TOKEN_URL,
                headers={"Accept": "application/json"},
                data={
                    "client_id": GITHUB_CLIENT_ID,
                    "client_secret": GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": redirect_uri,
                }
            )
            token_data = token_resp.json()
            access_token = token_data.get("access_token")
            if not access_token:
                err = token_data.get("error_description", token_data.get("error", "Failed to retrieve access token from GitHub"))
                return RedirectResponse(url=f"{FRONTEND_URL}/?error={urllib.parse.quote(err)}")
            
            user_resp = await client.get(
                GITHUB_USER_URL,
                headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
            )
            if user_resp.status_code != 200:
                return RedirectResponse(url=f"{FRONTEND_URL}/?error={urllib.parse.quote('Failed to fetch user profile from GitHub')}")
            user_info = user_resp.json()
            
            # Fetch emails if email is not visible in public profile
            if not user_info.get("email"):
                emails_resp = await client.get(
                    GITHUB_EMAILS_URL,
                    headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
                )
                if emails_resp.status_code == 200:
                    for em in emails_resp.json():
                        if em.get("primary") and em.get("verified"):
                            user_info["email"] = em.get("email")
                            break
                        elif em.get("primary"):
                            user_info["email"] = em.get("email")
    except Exception as e:
        return RedirectResponse(url=f"{FRONTEND_URL}/?error={urllib.parse.quote(str(e))}")
    
    return await _process_user(user_info, db)

@router.get("/mock_callback")
async def mock_callback(db: AsyncSession = Depends(get_db)):
    user_info = {
        "id": "mock_github_123",
        "login": "mock_user",
        "email": "mock@example.com"
    }
    return await _process_user(user_info, db)

async def _process_user(user_info: dict, db: AsyncSession):
    github_id = str(user_info.get("id"))
    username = user_info.get("login")
    email = user_info.get("email")
    
    # Check if user exists
    result = await db.execute(select(models.User).filter(models.User.github_id == github_id))
    user = result.scalars().first()
    
    if not user:
        user = models.User(github_id=github_id, username=username, email=email)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Initialize User State
        user_state = models.UserState(user_id=user.id, target_role="ML Engineer", fatigue=0.0)
        db.add(user_state)
        await db.commit()
    else:
        if email and user.email != email:
            user.email = email
            await db.commit()
        
    session_id = str(uuid.uuid4())
    await set_session(session_id, user.id)
    
    # Redirect to frontend with token
    return RedirectResponse(url=f"{FRONTEND_URL}/?token={session_id}")

