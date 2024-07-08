import os
from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from pytube import YouTube

def home(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            output_path = 'downloads/'
            file_path = stream.download(output_path=output_path)
            return redirect('download', file_name=os.path.basename(file_path))
        except Exception as e:
            return render(request, 'downloader/index.html', {'error': str(e)})
    return render(request, 'downloader/index.html')

def download(request, file_name):
    file_path = os.path.join('downloads', file_name)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    raise Http404("File does not exist")
