from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, ContentType, Permission
from apps.news.models import News, NewsCategory, Comment, Banner
from apps.course.models import Course, CourseCategory, Teacher
from apps.payinfo.models import PayInfo, PayInfoOrder
from apps.course.models import CourseOrder


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 1. 编辑组（管理新闻/管理课程/管理评论/管理轮播图等）
        edit_content_type = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher),
            ContentType.objects.get_for_model(PayInfo),
        ]

        edit_permission = Permission.objects.filter(content_type__in=edit_content_type)
        edit_Group = Group.objects.create(name='编辑组')
        edit_Group.permissions.set(edit_permission)
        edit_Group.save()
        self.stdout.write(self.style.SUCCESS('编辑组创建完成'))

        # 2. 财务组（课程订Group单/付费资讯订单）
        finance_content_type = [
            ContentType.objects.get_for_model(CourseOrder),
            ContentType.objects.get_for_model(PayInfoOrder),
        ]

        finance_permission = Permission.objects.filter(content_type__in=finance_content_type)
        finance_group = Group.objects.create(name='财务组')
        finance_group.permissions.set(finance_permission)
        finance_group.save()
        self.stdout.write(self.style.SUCCESS('财务组创建完成！'))

        # 3.管理员组
        admin_permission = edit_permission.union(finance_permission)
        admin_group = Group.objects.create(name='管理员组')
        admin_group.permissions.set(admin_permission)
        admin_group.save()
        self.stdout.write(self.style.SUCCESS('管理员组创建完成！'))
