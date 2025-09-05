"""
CORS中间件 - 专门处理跨域请求和OPTIONS预检请求
"""
from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from settings.config import settings


class CORSHandlerMiddleware(BaseHTTPMiddleware):
    """CORS处理中间件，确保OPTIONS请求得到正确处理"""
    
    async def dispatch(self, request: Request, call_next):
        # 处理OPTIONS预检请求
        if request.method == "OPTIONS":
            origin = request.headers.get("origin")
            allow_origin = "*"  # 默认允许所有
            if origin and self._is_origin_allowed(origin):
                allow_origin = origin
            elif "*" in settings.CORS_ORIGINS_LIST:
                allow_origin = "*"
            
            response = Response(
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": allow_origin,
                    "Access-Control-Allow-Methods": ", ".join(settings.CORS_ALLOW_METHODS),
                    "Access-Control-Allow-Headers": ", ".join(settings.CORS_ALLOW_HEADERS),
                    "Access-Control-Allow-Credentials": "true" if settings.CORS_ALLOW_CREDENTIALS else "false",
                    "Access-Control-Max-Age": "86400",  # 24小时缓存
                    "Access-Control-Expose-Headers": "*",
                }
            )
            return response
        
        # 处理其他请求
        response = await call_next(request)
        
        # 添加CORS响应头
        origin = request.headers.get("origin")
        print(f"DEBUG: Adding CORS headers for origin: {origin}")
        print(f"DEBUG: Allowed origins: {settings.CORS_ORIGINS_LIST}")
        
        if origin and self._is_origin_allowed(origin):
            print(f"DEBUG: Setting Access-Control-Allow-Origin to: {origin}")
            response.headers["Access-Control-Allow-Origin"] = origin
        elif "*" in settings.CORS_ORIGINS_LIST:
            print("DEBUG: Setting Access-Control-Allow-Origin to: *")
            response.headers["Access-Control-Allow-Origin"] = "*"
        elif origin:
            # 如果origin存在但不在允许列表中，不设置CORS头
            print(f"DEBUG: Origin {origin} not in allowed list, not setting CORS header")
        else:
            # 如果没有origin头，设置默认的CORS头
            print("DEBUG: No origin header, setting default CORS header")
            response.headers["Access-Control-Allow-Origin"] = settings.CORS_ORIGINS_LIST[0] if settings.CORS_ORIGINS_LIST else "*"
        
        if settings.CORS_ALLOW_CREDENTIALS:
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        response.headers["Access-Control-Expose-Headers"] = "*"
        
        return response
    
    def _is_origin_allowed(self, origin: str) -> bool:
        """检查origin是否被允许"""
        for allowed_origin in settings.CORS_ORIGINS_LIST:
            if allowed_origin == origin:
                return True
            elif allowed_origin.endswith("*"):
                # 支持通配符模式，如 http://localhost:*
                pattern = allowed_origin[:-1]  # 移除 *
                if origin.startswith(pattern):
                    return True
        return False
    
    def _get_allow_origin(self, request: Request) -> str:
        """获取允许的Origin"""
        origin = request.headers.get("origin")
        print(f"DEBUG: Request origin: {origin}")
        print(f"DEBUG: Allowed origins: {settings.CORS_ORIGINS_LIST}")
        if origin and self._is_origin_allowed(origin):
            print(f"DEBUG: Origin {origin} found in allowed list")
            return origin
        elif "*" in settings.CORS_ORIGINS_LIST:
            print("DEBUG: Using wildcard origin")
            return "*"
        else:
            # 如果没有匹配的origin，返回第一个允许的origin
            fallback = settings.CORS_ORIGINS_LIST[0] if settings.CORS_ORIGINS_LIST else "*"
            print(f"DEBUG: Using fallback origin: {fallback}")
            return fallback
