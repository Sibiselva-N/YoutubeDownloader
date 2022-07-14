from wsgiref.util import FileWrapper
from django import views
from django.shortcuts import render, HttpResponse
from pytube import YouTube
import os
import mimetypes

# Create your views here.


def home(request):
    if request.method == "POST":
        muxed = []
        onlyAudio = []
        onlyVideo = []
        url = request.POST['url']
        yt = YouTube(url)
        streams_ = yt.streams
        title = yt.title
        thumbnail = yt.thumbnail_url
        for i in streams_.filter(progressive=True, file_extension="mp4"):
            data = {"url": i.url, "res": i.resolution,
                    "size": round(((i.filesize / 1024)/1024), 2)}
            muxed.append(data)
        for i in streams_.filter(only_audio=True, file_extension="mp4"):
            data = {"url": i.url, "res": i.abr,
                    "size": round(((i.filesize / 1024)/1024), 2)}
            onlyAudio.append(data)
        for i in streams_.filter(adaptive=True, file_extension="mp4"):
            if i.mime_type == "video/mp4":
                data = {"url": i.url, "res": i.resolution,
                        "size": round(((i.filesize / 1024)/1024), 2)}
                onlyVideo.append(data)
        datas = {"title": title, "thum": thumbnail,
                 "muxed": muxed, "video": onlyVideo, "audio": onlyAudio}
        return render(request, 'home.html', datas)
    return render(request, 'home.html')
