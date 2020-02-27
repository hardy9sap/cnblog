
from django import template
from blog.models import *
from django.db.models.functions import TruncMonth
from django.db.models import Count

register = template.Library()


@register.inclusion_tag("blog/classification.html")
def get_classification_style(sitename):
    user = UserInfo.objects.all().filter(username=sitename).first()

    blog = user.blog

    cate_ls = Category.objects.all().filter(blog=blog).values('pk').annotate(c=Count('article__category')).values('title', 'c')

    tag_ls = Tag.objects.all().filter(blog=blog).values('pk').annotate(c=Count('article__pk')).values('title', 'c')  # Count('article') == Count('article__pk')等字段

    date_ls = Article.objects.\
        all().\
        filter(user=user).\
        annotate(month=TruncMonth('create_time')).\
        values('month').\
        annotate(c=Count('nid')).values('month', 'c')
    return dict(user=user, blog=blog, cate_ls=cate_ls, tag_ls=tag_ls, date_ls=date_ls)
