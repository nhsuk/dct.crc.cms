from django.conf import settings


def verify_pubtoken(request):
    """Verify that the request is coming from the correct pubtoken"""
    pubtoken = getattr(settings, "PUBTOKEN", None)

    validAdminToken = request.headers.get("AdminToken", "") == str(pubtoken)
    validAuth = request.headers.get("Authorization", "") == "Bearer " + str(pubtoken)
    if validAdminToken or validAuth:
        return True
    return False
