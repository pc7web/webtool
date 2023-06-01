import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# from gdstorage.storage import GoogleDriveStorage
from phonenumber_field.modelfields import PhoneNumberField

# gd_storage = GoogleDriveStorage()
# Create your models here.


class SiteData(models.Model):
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=50)
    data = models.JSONField(default=dict)
    time = models.DateTimeField(auto_now_add=True, verbose_name="Time (Added)")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Time (Updated)")

    class Meta:
        verbose_name_plural = "Site Data"
        unique_together = ('name', 'category')


class ContactUs(models.Model):
    CONTACT_TYPE = (
        ("contact", "Contact"),
        ("report_user", "Report User"),
        ("report_page", "Report Page"),
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
    user = models.ForeignKey(User, to_field="username",
                             on_delete=models.PROTECT,
                             null=True,
                             blank=True)
    email = models.EmailField(max_length=100)
    phone = PhoneNumberField(blank=True, null=True)
    data = models.JSONField(
        default=dict, help_text='{"for":"","url": "","desc":""}')
    time = models.DateTimeField(auto_now_add=True, verbose_name="Time (Added)")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Time (Updated)")

    def __str__(self) -> str:
        return f"{self.title} | {self.email}"

    class Meta:
        verbose_name_plural = "Contact Us"


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True, verbose_name="Time (Added)")

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
        ("job", "Job"),
        ("tool", "Tool"),
        ("exam", "Exam"),
        ("article", "Article"),
        ("material", "Material"),
        ("route", "Route"),
        ("other", "Other"),
    )

    page_type = models.CharField(
        max_length=20,
        verbose_name="Type",
        default="page",
        choices=PAGE_TYPE
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, to_field="username", related_name="pages", verbose_name="Author")
    title = models.CharField(max_length=150)
    slug = models.CharField(
        max_length=150,
        unique=True,
        default="auto",
        help_text="'auto' will be replaced by slug generated using title field",
    )

    data = models.JSONField(verbose_name="Addition Data",
                            default=dict, help_text='like: {"company": "", "role": "", "salary": "", "experience": "", "location": "", "website": "", "applyLink": "", "lastDate": ""}')
    content = models.TextField(verbose_name="Page Content",
                               help_text="Click on the top EDITOR button to open HTML Editor.")
    is_markup = models.BooleanField(
        default=False, verbose_name="Is a Markdown", help_text="like: # heading")

    is_indexed = models.BooleanField(
        default=False, verbose_name="Index", help_text="List with all pages.")
    is_published = models.BooleanField(
        default=False, verbose_name="Publish", help_text="saved as draft if unchecked.")

    time = models.DateTimeField(auto_now_add=True, verbose_name="Time (Added)")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Time (Updated)")

    description = models.CharField(
        max_length=250, help_text="Meta description(SEO)")
    categories = models.CharField(max_length=50)
    tags = models.CharField(
        max_length=150, help_text="Meta keywords(SEO), (, saparated)", verbose_name="Keywords", blank=True)

    class Meta:
        ordering = ["page_type", "is_indexed",
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

    def __str__(self):
        return self.shortTitle

    class Meta:
        verbose_name_plural = "Site Pages"


class Profile(models.Model):
    USER_TYPE = (
        ("user", "user"),
        ("staff", "staff"),
        ("admin", "admin"),
    )

    uuid = models.UUIDField(
        help_text="Don't modify! (Foreign key for supabase's auth.users [id: UUID])", null=True)
    user = models.OneToOneField(User, null=True, to_field="username",
                                on_delete=models.RESTRICT)
    isa = models.CharField(choices=USER_TYPE, default="user", max_length=20,
                           help_text="Represent user type in frontend(sync with the supabase's auth.users's user_meta_data's[: Jsonb] isa property).")
    data = models.JSONField(
        default=dict, help_text="{data} property will be sync with the supabase's auth.users's user_meta_data's[: Jsonb] data property.")
    joined_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} * {self.email}"

    @property
    def full_name(self) -> str:
        return self.user.get_full_name()

    @property
    def public(self) -> dict[any]:
        try:
            default = SiteData.objects.filter(name='profile-init-data').first()
            if self.data.get("isprivate", True):
                return default.data.get("public", {})
            return self.data.get("public", default.data.get("public", {}))
        except:
            return {}

    @property
    def privateData(self) -> dict[any]:
        try:
            return self.data.get("private", {})
        except:
            return {}

    @property
    def getState(self) -> dict[any]:
        try:
            return self.data.state
        except:
            self.data.set('state', {})
            return {}

    @property
    def is_email_verified(self) -> bool:
        return self.data.get("state", {}).get("email_verified", True)

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def email(self) -> str:
        return self.user.email

    def setIsa(self, isa=None) -> str:
        if isa == None:
            isa = self.user
        self.isa = Profile.getIsa(isa)
        return self.isa

    @classmethod
    def getUserTypes(cls) -> set[str]:
        return {"admin", "staff", "user"}

    @classmethod
    def getIsa(cls, user) -> str:
        types = cls.getUserTypes()

        if type(user) == str and user in types:
            return user

        elif type(user) == User:
            if user.groups.first():
                name = user.groups.first().name
                if name in types:
                    return name

            if user.is_superuser:
                return "admin"
            elif user.is_staff:
                return "staff"

        return "user"

    # Create object with initial data for profile's data
    @classmethod
    def create(cls, **kwargs):
        siteData = SiteData.objects.filter(name="profile-init-data").first()
        data = siteData.data if siteData != None else {}
        return cls.objects.create(data=data, **kwargs)


class FileUpload(models.Model):
    title = models.CharField(max_length=250)
    time = models.TimeField(auto_now_add=True)
    data = models.JSONField(verbose_name='File Data', default=dict)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "File Uploads"
        ordering = (
            "title",
            "-time",
            "-active",
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.create(user=instance, isa=Profile.getIsa(instance))
        if instance.is_superuser or instance.is_staff:
            pass
    else:
        instance.profile.setIsa(instance)
        instance.profile.save()


# signal for create slug field while new creating Topic's object/row
@receiver(pre_save, sender=SitePage)
def create_sitepage_slug(sender, instance, **kwargs):
    if instance.slug == "auto" or instance.slug == '':
        instance.slug = SitePage.create_slug(instance.title)
