# 内置模块
import os
import json
import threading
# 第三方模块
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.http import JsonResponse
from django.db.models import Count, F
from django.db.models.functions import TruncMonth
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .geetest import GeetestLib
from bs4 import BeautifulSoup
# 自制模块
from .models import UserInfo, Article, Category, Tag, ArticleUpDown, Comment, Blog
from .myform import UserForm
from .utils.check_code import get_check_code
from cnblog import settings

# Create your views here.

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"  # 滑动验证码id
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"  # 滑动验证码key


def get_index(request):
    """
    index页面  http://127.0.0.1:8080/
    :param request: 请求体
    :return:
    """
    article_ls = Article.objects.all()
    return render(request=request, template_name='blog/index.html', context=locals())


def register(request, protocol):
    """
    register页面  http://127.0.0.1:8080/register/
                 http://127.0.0.1:8080/register/protocol/
    :param request:
    :return:

    extra points:
    # print(protocol)  # None，如果没有匹配的，为None
    """
    if request.method == 'POST':  # is_ajax()
        form = UserForm(data=request.POST)
        errors_response = dict(status=False)
        if not form.is_valid():
            global_errors = form.errors.get('__all__')
            for key in form.errors:  # 拿到所有的错误信息
                if key == '__all__':
                    continue
                errors_response[key] = form.errors.get(key)
            if global_errors:
                errors_response['confirmpwd'] = global_errors[0]
            return JsonResponse(data=errors_response)
        else:
            # 注册用户
            loginname = request.POST.get('loginname')
            nickname = request.POST.get('nickname')
            pwd = request.POST.get('pwd')
            tel = request.POST.get('tel')
            email = request.POST.get('email')
            avatar_obj = request.FILES.get('file')
            blog = Blog.objects.create(title=nickname, site_name=loginname, theme=f'{loginname}.css')
            extra_fields = dict()
            if avatar_obj:
                extra_fields['avatar'] = avatar_obj  # avatar字段必须接受一个文件对象
                # Django做的事情
                # 会把文件下载到avatar字段upload_to参数指定的值的位置，如果文件夹不存在，自动创建；avatar字段存放的是文件的相对路径
                # 如果没有指定upload_to，则会把文件下载到项目根目录下

                # 如果配置了media
                # 那么会把文件下载到media_root对应的文件夹中
            new_user = UserInfo.objects.create_user(
                username=loginname,
                password=pwd,
                telephone=tel,
                email=email,
                blog=blog,
                **extra_fields
            )
            new_user.save()
            errors_response['status'] = True
            errors_response['msg'] = '/login/'
            return JsonResponse(data=errors_response)
    else:
        form = UserForm(data=None)
        if protocol:
            return render(request=request, template_name='blog/register/protocol.html', context={})
        return render(request=request, template_name='blog/register.html', context=locals())


def login(request):
    """
    login页面  http://127.0.0.1:8080/login/
              http://127.0.0.1:8080/login/get-check-code/
    :param request:
    :return:
    """
    if request.method == 'POST':
        gt = GeetestLib(captcha_id=pc_geetest_id, private_key=pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        login_name = request.POST.get('loginName')
        password = request.POST.get('password')
        check_code = request.POST.get('checkCode')
        response = {'user': None, 'status': None, 'check_code_status': None, 'auth_status': None, 'msg': None}

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        if result:
            response['status'] = True
            # 首先校验验证码
            if check_code.upper() != request.session['cur_check_code'].upper():
                response['msg'] = '验证码错误'
                response['check_code_status'] = False
                return JsonResponse(data=response)
            else:
                response['check_code_status'] = True
                user = auth.authenticate(username=login_name, password=password)
                if not user:
                    response['msg'] = '&lowast;&nbsp;用户名或密码错误'
                    response['auth_status'] = False
                    return JsonResponse(data=response)
                else:
                    auth.login(request=request, user=user)
                    response['user'] = login_name
                    response['msg'] = request.GET.get('next', '/')
                    response['auth_status'] = True
                    return JsonResponse(data=response)  # 自动序列化和反序列化
        else:
            response['status'] = False
            response['msg'] = '/get-404-page/'
            return JsonResponse(data=response)
    else:
        # http://127.0.0.1:8080/login/get-check-code/
        path = os.path.basename(os.path.dirname(request.path))
        if path == 'get-check-code':
            img_data = get_check_code(request=request)
            return HttpResponse(content=img_data)
        print(2)
        # login页面  http://127.0.0.1:8080/login/
        return render(request=request, template_name='blog/login.html', context={})


def pcgetcaptcha(request):
    """
    滑动验证码第一次校验
    :param request:
    :return:
    """
    user_id = 'geetest'
    gt = GeetestLib(captcha_id=pc_geetest_id, private_key=pc_geetest_key)
    status = gt.pre_process(user_id=user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session['user_id'] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(content=response_str)


def get_404_page(request):
    """
    404page
    :param request:
    :return:
    """
    return render(request=request, template_name='blog/page404.html', context={})


def logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    auth.logout(request=request)
    return redirect(to='/')


def get_homesite(request, sitename, **kwargs):
    """
    个人站点视图
    :param request:
    :param sitename:
    :param kwargs:
    :return:
    """
    # query_set = get_classification_data(sitename=sitename)
    # user = query_set.get('user')
    user = UserInfo.objects.all().filter(username=sitename).first()

    # 判断用户是否存在
    if not user:
        return get_404_page(request=request)

    # 获取当前站点对象
    # blog = user.blog
    # 获取当前用户或者当前站点对应的所有文章
    article_ls = Article.objects.all().filter(user=user)
    if kwargs:
        if kwargs['condition'] == 'tag':
            article_ls = article_ls.filter(tags__title=kwargs['param'])
        elif kwargs['condition'] == 'category':
            article_ls = article_ls.filter(category__title=kwargs['param'])
        else:
            year, month = kwargs['param'].split(sep='-')
            article_ls = article_ls.filter(create_time__year=year, create_time__month=month)
    # query_set['article_ls'] = article_ls
    # 获取当前用户或者站点对应的分类以及文章数
    # cate_ls = Category.objects.all().filter(blog=blog).values('pk').annotate(c=Count('article__category')).values('title', 'c')

    # 获取当前用户或者站点对应的标签以及文章数
    # tag_ls = Tag.objects.all().filter(blog=blog).values('pk').annotate(c=Count('article__pk')).values('title', 'c')  # Count('article') == Count('article__pk')等字段

    # 获取月份
    # 方式一
    # date_ls = Article.objects.all().filter(user=user).extra(select={'y_m': 'date_format(create_time, "%%Y-%%m")'}).values('y_m').annotate(c=Count('nid')).values('y_m', 'c')
    # extra会在原表的基础上新增一个字段
    # print(date_ls)

    # 方式二
    # date_ls = Article.objects.\
    #     all().\
    #     filter(user=user).\
    #     annotate(month=TruncMonth('create_time')).\
    #     values('month').\
    #     annotate(c=Count('nid')).values('month', 'c')
    return render(request=request, template_name='blog/homesite.html', context=locals())


def get_classification_data(sitename):
    user = UserInfo.objects.all().filter(username=sitename).first()

    blog = user.blog

    cate_ls = Category.objects.all().filter(blog=blog).values('pk').annotate(c=Count('article__category')).values(
        'title', 'c')

    tag_ls = Tag.objects.all().filter(blog=blog).values('pk').annotate(c=Count('article__pk')).values('title',
                                                                                                      'c')  # Count('article') == Count('article__pk')等字段

    date_ls = Article.objects. \
        all(). \
        filter(user=user). \
        annotate(month=TruncMonth('create_time')). \
        values('month'). \
        annotate(c=Count('nid')).values('month', 'c')
    return dict(user=user, blog=blog, cate_ls=cate_ls, tag_ls=tag_ls, date_ls=date_ls)


def get_article_detail(request, sitename, article, article_id):
    """
    文章详情页
    :param request: 请求体
    :param sitename: 站点名
    :param article: 文章固定格式字符串
    :param article_id: 文章id
    :return:
    """
    user = UserInfo.objects.all().filter(username=sitename).first()
    article_obj = Article.objects.all().get(nid=article_id)
    comment_ls = Comment.objects.all().filter(article_id=article_id)
    return render(request=request, template_name='blog/articledetail.html', context=locals())


def test(request):
    """
    测试视图
    :param request:
    :return:
    """
    return render(request=request, template_name='blog/test.html', context={})


def diggit(requset):
    """
    点赞和反对视图
    :param requset:
    :return:
    """
    article_id = requset.POST.get('article_id')
    is_up = json.loads(requset.POST.get('is_up'))  # 原来单个值也可以JSON啊
    response = dict(status=True)
    up_down_obj = ArticleUpDown. \
        objects.all(). \
        filter(user_id=requset.user.pk, article_id=article_id). \
        first()
    if not up_down_obj:
        ArticleUpDown.objects.create(user_id=requset.user.pk, article_id=article_id, is_up=is_up)
        article = Article.objects.all().filter(nid=article_id)
        if is_up:
            article.update(up_count=F('up_count') + 1)
        else:
            article.update(down_count=F('down_count') + 1)
    else:
        response['status'] = False
        response['handled'] = up_down_obj.is_up
    return JsonResponse(data=response)


def comment(request):
    """
    评论视图
    :param request:
    :return:
    """
    content = request.POST.get('content')
    article_id = request.POST.get('article_id')
    user_id = request.user.pk
    parent_comment_id = request.POST.get('pid')  # null=True, 传空字符串也可以
    with transaction.atomic():  # 事务操作
        comment = Comment.objects.create(article_id=article_id, user_id=user_id, content=content,
                                         parent_comment_id=parent_comment_id)
        Article.objects.all().filter(pk=article_id).update(comment_count=F('comment_count') + 1)
    article_obj = Article.objects.all().filter(pk=article_id).first()
    parent_comment_content = {}
    if parent_comment_id:
        parent_comment_content['parent_comment'] = comment.parent_comment.content
    response = {'status': True,
                'content': content,
                'user': UserInfo.objects.all().filter(nid=user_id).first().username,
                'create_time': comment.create_time.strftime('%Y-%m-%d %X'),
                'comment_id': comment.nid
                }
    response.update(parent_comment_content)

    # 发送邮件
    subject = '您的文章%s在博客园新增了一条评论' % article_obj.title
    message = content
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["1361722162@qq.com"]
    # send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
    email_threading = threading.Thread(target=send_mail,
                                       kwargs=dict(subject=subject,
                                                   message=message,
                                                   from_email=from_email,
                                                   recipient_list=recipient_list
                                                   )
                                       )
    email_threading.start()
    # from django.core.mail import send_mass_mail
    return JsonResponse(data=response)


def get_comment_tree(request):
    """
    评论树
    :param request:
    :return:
    """
    article_id = request.GET.get('article_id')
    with transaction.atomic():
        comment = list(
            Comment.objects.all().filter(article_id=article_id).order_by('pk').values('pk', 'content',
                                                                                      'parent_comment_id'))
        Article.objects.all().filter(pk=article_id).update(comment_count=F('comment_count') + 1)
    return JsonResponse(data=comment, safe=False)


@login_required
def manage_backend(request):
    """
    后台管理
    :param request:
    :return:
    """
    article_list = Article.objects.filter(user=request.user)
    return render(request=request, template_name='blog/backend/backend.html', context=locals())


@login_required
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        soup = BeautifulSoup(markup=content, features='html.parser')
        for tag in soup.find_all():
            if tag.name == 'script':
                tag.decompose()
        desc = soup.text[0:150] + '...'
        Article.objects.create(title=title, desc=desc, content=str(soup), user=request.user)
        return redirect(to='/cnblog-backend/')
    return render(request=request, template_name='blog/backend/add-article.html', context={})


def upload(request):
    """
    文本编辑器文本上传
    :param request:
    :return:
    """
    file = request.FILES.get('upload_img')
    path = os.path.join(settings.MEDIA_ROOT, 'addarticle', file.name)
    with open(file=path, mode='wb') as fp:
        for line in file:
            fp.write(line)
    response = {
        'error': 0,
        'url': '/media/addarticle/%s' % file.name
    }
    return HttpResponse(content=json.dumps(response))


def simplemde(request):

    return render(request, 'blog/backend/markdown-editor.html')
