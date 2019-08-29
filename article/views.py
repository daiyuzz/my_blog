import markdown
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
# 导入数据模型
from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

# 视图函数
def article_list(request):
    # 取出所有博客
    article_list = ArticlePost.objects.all()
    # 每页显示1篇文章
    paginator = Paginator(article_list,1)
    # 获取url中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给articles
    articles = paginator.get_page(page)
    # 需要传递给模板的对象
    context = {'articles': articles}
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    # 取出响应文章
    article = ArticlePost.objects.get(id=id)
    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    # 需要传递给模板对象
    context = {'article': article}
    return render(request, 'article/detail.html', context)


# 写文章的视图
# 检查登录
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            # 将文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect('article:article_list')
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_from': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


# 删除文章
@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    # 根据id获取要删除的文章
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你没有权限修改这篇文章")
    # 调用 delete()方法删除文章
    article.delete()
    # 删除后返回文章列表
    return redirect('article:article_list')


# 更新文章
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方式提交表单，更新title、body字段
    GET方法进入初始表单页
    """
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 验证是否为作者本人
    if request.user != article.author:
        return HttpResponse("抱歉，你没有权限修改这篇文章！")
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型要求
        if article_post_form.is_valid():
            # 保存新写入的title、body数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需要传入文章的id值
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写")
    # 如果是GET请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
