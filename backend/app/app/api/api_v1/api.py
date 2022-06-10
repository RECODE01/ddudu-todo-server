from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils, schedules, challenge, challenge_request, challenge_schedule_detail

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(challenge.router, prefix="/challenges", tags=["challenges"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["schedules"])
api_router.include_router(challenge_request.router,
                          prefix="/challenge-requests", tags=["challenge-requests"])
api_router.include_router(challenge_schedule_detail.router,
                          prefix="/challenge-schedules", tags=["challenge-schedules"])
