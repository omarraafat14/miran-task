from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse

from redis import Redis
from redis.exceptions import RedisError


def health_check(request):
    # Check database
    db_healthy = True
    try:
        connections["default"].cursor()
    except OperationalError:
        db_healthy = False
    # Check Redis
    redis_healthy = True
    try:
        redis_client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            socket_timeout=1,
        )
        redis_client.ping()
    except RedisError:
        redis_healthy = False

    status = 200 if (db_healthy and redis_healthy) else 503

    return JsonResponse(
        {
            "status": "healthy" if status == 200 else "unhealthy",
            "database": "up" if db_healthy else "down",
            "redis": "up" if redis_healthy else "down",
        },
        status=status,
    )
