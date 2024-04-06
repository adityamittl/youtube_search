from celery import shared_task
from googleapiclient.discovery import build
from datetime import datetime
from syncthing.models import Video
from django.conf import settings
from datetime import datetime
import json

@shared_task
def fetch_youtube_videos():

    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=settings.YOUTUBE_SEARCH_QUERY,
        part='snippet',
        type='video',
        maxResults=10,
        order='date',
        publishedAfter="2024-04-06T16:45:00Z"
    )
    response = request.execute()
    for item in response['items']:
        # return str(item['snippet']['thumbnails']['default']['url']).split("/")[4]
        if Video.objects.filter(video_id = str(item['snippet']['thumbnails']['default']['url']).split("/")[4]).count() == 0:
            video = Video.objects.create(
                title=item['snippet']['title'],
                description=item['snippet']['description'],
                publishing_datetime = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
                thumbnail_url=item['snippet']['thumbnails']['default']['url'],
                video_id = str(item['snippet']['thumbnails']['default']['url']).split("/")[4]
            )
            video.save()
    return "Done"




