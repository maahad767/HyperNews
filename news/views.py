from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import settings
from django.http import Http404, HttpResponseBadRequest

import datetime
import json
import random

class MainView(View):

    def get(self, request):
        return redirect('all_news')


class SingleNews(View):
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        all_news = json.load(json_file)

    def get(self, request, link):
        for news in self.all_news:
            if news['link'] == link:
                return render(request, 'news/news.html', context=news)

        raise Http404("Sorry, the news of link doesn't exists")


class News(View):
    def get(self, request):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            all_news = json.load(json_file)
        query = request.GET.get('q')

        all_news = sorted(all_news, key=lambda k: k['created'], reverse=True)
        filtered_news = []
        if query is not None:
            for news in all_news:
                if query in news['title']:
                    filtered_news.append(news)
            all_news = filtered_news

        return render(request,'news/news_list.html', context={'news_list': all_news})


class CreateNews(View):

    def get(self, request):
        return render(request, 'news/create_news.html')

    def post(self, request):
        title = request.POST.get('title')
        text = request.POST.get('text')
        if title is not None and text is not None:
            with open(settings.NEWS_JSON_PATH, 'r') as json_file:
                all_news = json.load(json_file)
            with open(settings.NEWS_JSON_PATH, 'w') as json_file:
                news = {
                    "created": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    "text": text,
                    "title": title,
                    "link": random.randint(100000, 999999)
                }
                all_news.append(news)
                json.dump(all_news, json_file)
            return redirect('all_news')
        return HttpResponseBadRequest()

