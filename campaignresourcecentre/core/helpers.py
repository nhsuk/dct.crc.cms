from django.conf import settings


def verify_pubtoken(request):
    """Verify that the request is coming from the correct pubtoken"""
    pubtoken = getattr(settings, "PUBTOKEN", None)

    if request.headers.get("Authorization", "") == "Bearer " + str(pubtoken):
        return True
    return False
