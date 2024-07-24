from rest_framework.throttling import UserRateThrottle


class DailyUserRatingThrottle(UserRateThrottle):
    rate = '10/day'

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': request.user.pk
        }
