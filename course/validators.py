from rest_framework.serializers import ValidationError


class YouTubeValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = "http://youtube.com"
        if value.get('link'):
            if url not in value.get('link'):
                raise ValidationError("Need valid YouTube link")
        return None
