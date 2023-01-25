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
