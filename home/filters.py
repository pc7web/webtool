from django.contrib import admin


class ActiveUser(admin.SimpleListFilter):

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "Active User"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "active"

    def lookups(self, request, model_admin):
        return (
            ("active", 'Active'),
            ("inactive", 'Inactive'),
        )

    def queryset(self, request, queryset):
        if self.value() == "active":
            return queryset.filter(user__is_active=True)

        elif self.value() == "inactive":
            return queryset.filter(user__is_active=False)

        return queryset.filter()


class ActiveTag(admin.SimpleListFilter):

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "Active Tag"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "active"

    def lookups(self, request, model_admin):
        return (
            ("active", 'Active'),
            ("inactive", 'Inactive'),
        )

    def queryset(self, request, queryset):
        if self.value() == "active":
            return queryset.filter(tags__active=True)

        elif self.value() == "inactive":
            return queryset.filter(tags__active=False)

        return queryset.filter()


class ProfileType(admin.SimpleListFilter):

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "Profile Type"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "type"

    def lookups(self, request, model_admin):
        return (
            ("admin", 'Admin'),
            ("user", 'User'),
            ("staff", 'Staff'),
        )

    def queryset(self, request, queryset):

        if self.value() == None:
            if request.user.is_superuser:
                return queryset.filter()

            return queryset.filter(user__is_superuser=False)

        if self.value() == "user":
            return queryset.filter(user__is_staff=False,
                                   user__is_superuser=False)

        elif self.value() == "staff":
            return queryset.filter(user__is_staff=True,
                                   user__is_superuser=False)

        if request.user.is_superuser:
            if self.value() == "admin":
                return queryset.filter(user__is_superuser=True)
