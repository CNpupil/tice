from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.cache import cache

from main.models import User
from main import tools
from tice import settings

import jwt


class CheckTokenMiddleware(MiddlewareMixin):
    def process_request(self,request):
        try:
            # return None
            path = request.path_info[1:]
            if path in ['login', 'scorestandard', 'changepassword', 'register']:
                return None
            
            auth_header = request.headers.get('Authorization', '').split()
            if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
                raise jwt.InvalidTokenError('Invalid token format')
            token = auth_header[1]

            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
            expire_time = cache.get(token)
            if expire_time is None or expire_time < tools.getNowTimeStamp():
                raise jwt.InvalidTokenError('token already expired')
                
            print(payload['auth'], path)
            if payload['auth'] == 2:
                if path not in ['taskbyteacher', 'studentfromtaskbyteacher', 'studentfromtaskbyteacher']:
                    raise jwt.InvalidTokenError('Permission denied')
            elif payload['auth'] == 3:
                if path not in ['scoreonstudent']:
                    raise jwt.InvalidTokenError('Permission denied')

        except (jwt.InvalidTokenError, User.DoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=401)