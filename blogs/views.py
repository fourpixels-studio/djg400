from .models import Blog
from django.shortcuts import render
from seo_management.models import SEO
from frontend.utils import update_views

blogs_seo = SEO.objects.get(pk=2)


def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    context = {
        "blog": blog,
        "meta_description": blog.summary,
        "meta_thumbnail": blog.get_thumbnail,
        "title_tag": f"{blog.category} | {blog.title}",
        "meta_keywords": f"{blog.category}, {blogs_seo.meta_keywords}",
        "recent_blogs": Blog.objects.order_by("-published_date").exclude(pk=blog.pk),
        "latest_articles": Blog.objects.filter(is_published=True).exclude(pk=blog.pk).order_by("-published_date")[:3],
        "trending_articles": Blog.objects.filter(is_published=True).exclude(pk=blog.pk).order_by('hit_count_generic')[:3],
    }
    update_views(request, blog)
    return render(request, "blog_detail.html", context)


def blog_list(request):
    context = {
        "title_tag": blogs_seo.title_tag,
        "meta_keywords": blogs_seo.meta_keywords,
        "meta_thumbnail": blogs_seo.get_thumbnail,
        "meta_description": blogs_seo.meta_description,
        "blogs": Blog.objects.order_by("-published_date"),
    }
    return render(request, "blog_list.html", context)
