from django.shortcuts import render,HttpResponse
from django.views import View
from .forms import *
from .models import *


class PostView(View):
    def get(self,request):
        obj = PostForm()
        return render(request,'post.html',{'obj':obj})

    def post(self,request):
        TagSheet.objects.get_or_create(tag=request.POST.get('tag'))
        data={
            'title':request.POST.get('title'),
            'content':request.POST.get('content'),
            'tag':request.POST.get('tag'),
            'type':request.POST.get('type'),
        }
        obj=PostForm(data)
        if obj.is_valid():
            obj.save()
            return HttpResponse('successful')
        else:
            TagSheet.objects.filter(tag=request.POST.get('tag')).delete()
            return HttpResponse('failed')

class ArticleView(View):
    def get(self,request,id):
        obj=ArticleSheet.objects.get(id=id)
        return render(request,'article.html',{'obj':obj})

    def post(self,request,id):
        if 'F1' in request.POST:
            pass
        return render(request,'article.html')


class ListView(View):
    def get(self,request,urltype,type,page):
        if urltype=='type':
            articles=ArticleSheet.objects.filter(type=type)[(page-1)*10:page*10]
        elif urltype=='tag':
            articles = ArticleSheet.objects.filter(tag=type)[(page - 1) * 10:page * 10]
        context={'articles':articles,'urltype':urltype,'type':type}
        return render(request, 'list.html',context)

class IndexView(View):
    def get(self,request):
        types=TypeSheet.objects.all()
        tags=TagSheet.objects.all()
        articles=ArticleSheet.objects.all()[:20]
        context={
            'types':types,
            'tags':tags,
            'articles':articles,
        }
        return render(request,'index.html',context)