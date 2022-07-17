import logging

from django.shortcuts import render

from cutdown_ui.helpers import get_shorten_url

log = logging.getLogger("django")


def home(request):
    if request.method == "POST" and request.POST.get("target_url"):

        target_url = request.POST.get("target_url")
        response_data = get_shorten_url(url=target_url)
        log.info(f"Response {response_data}")

        return render(
            request,
            "home.html",
            context=response_data,
        )

    return render(request, "home.html")
