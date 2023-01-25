import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from gdstorage.storage import GoogleDriveStorage
from phonenumber_field.modelfields import PhoneNumberField

# gd_storage = GoogleDriveStorage()
# Create your models here.


class SiteData(models.Model):
    name = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=50)
    data = models.JSONField(default=dict)
    time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Site Data"


class ContactUs(models.Model):
    CONTACT_TYPE = (
        ("contact", "Contact"),
        ("report_user", "Report User"),
        ("report_topic", "Report Topic"),
        ("report_comment", "Report Comment"),
        ("report_reply", "Report Reply"),
        ("report_error", "Report Error"),
    )

    title = models.CharField(max_length=150)
    contact_type = models.CharField(
        choices=CONTACT_TYPE,
        default="contact",
        max_length=20,
        verbose_name="Contact Type",
    )
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             null=True,
                             blank=True)
    email = models.EmailField(max_length=100)
    phone = PhoneNumberField(blank=True)
    desc = models.JSONField(default=dict)
    time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} | {self.email}"

    class Meta:
        verbose_name_plural = "Contact Us"


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def getCreate(cls, name: str):
        tag = cls.objects.filter(name=name.lower()).first()

        if tag == None:
            tag = cls.objects.create(name=name.lower())

        return tag

    @property
    def topics(self):
        return self.topic

    @property
    def topic_count(self):
        return len(self.topic.all())

    class Meta:
        verbose_name_plural = "Tags"
        ordering = (
            "name",
            "-time",
            "-active",
        )


# class FilesUpload(models.Model):
#     name = models.CharField(max_length=200, verbose_name="File Name")
#     data = models.FileField(upload_to='files', storage=gd_storage)


class SitePage(models.Model):
    PAGE_TYPE = (
        ("page", "Page"),
        ("tool", "Tool"),
        ("exam", "Exam"),
        ("blog", "Blog"),
        ("material", "Material"),
    )

    isa = models.CharField(
        max_length=20,
        verbose_name="Type",
        default="page",
        choices=PAGE_TYPE
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pages", verbose_name="Author")
    title = models.CharField(max_length=150)
    slug = models.CharField(
        max_length=150,
        unique=True,
        default="auto",
        help_text="'auto' will be replaced by slug generated using title field",
    )

    content = models.TextField()
    is_markup = models.BooleanField(default=False)

    is_approved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    description = models.CharField(
        max_length=250, help_text="Meta description")
    categories = models.CharField(max_length=50)
    tags = models.ManyToManyField(
        Tag, help_text="Meta keywords", verbose_name="Keywords")

    class Meta:
        ordering = ["isa", "is_approved",
                    "is_published", "-time", "-updated_at"]

    @classmethod
    def create_slug(cls, slug) -> str:
        slug = slug.lower().strip()
        slug = re.sub(r"[^\w\slug-]", "", slug)
        slug = re.sub(r"[\s_-]+", "-", slug)
        slug = re.sub(r"^-+|-+$", "", slug)
        return slug

    @property
    def shortContent(self) -> str:
        return self.content[:150]

    @property
    def shortTitle(self) -> str:
        return self.title[:50]

    @property
    def created(self):
        return self.time.date

    @property
    def updated(self):
        return self.updated_at.date

    @property
    def authorName(self) -> str:
        return self.user.get_full_name

    @property
    def is_edited(self) -> bool:
        return self.time != self.updated_at

    class Meta:
        verbose_name_plural = "Site Pages"

# signal for create slug field while new creating Topic's object/row


@receiver(pre_save, sender=SitePage)
def create_sitepage_slug(sender, instance, **kwargs):
    if instance.slug == "auto" or instance.slug == '':
        instance.slug = SitePage.create_slug(instance.title)
