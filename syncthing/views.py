from django.http import HttpResponse
from syncthing.tasks import fetch_youtube_videos
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Video


def fetch_videos(request):
    res = fetch_youtube_videos.delay()
    # res = test.delay(2,3)
    return HttpResponse("Fetching videos in background."+str(res))

def home(request):
    video_list = Video.objects.all().order_by("-publishing_datetime")
    paginator = Paginator(video_list, 10)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", {"page_obj": page_obj})