from .models import ErrorModel
from django.contrib import admin
from .settings import APP_ERROR_USE_DJANGO_ADMIN_SITE

if APP_ERROR_USE_DJANGO_ADMIN_SITE:
    @admin.register(ErrorModel)
    class ErrorModelAdmin(admin.ModelAdmin):
        def has_add_permission(self, request):
            return False

        date_hierarchy = 'last_seen'
        list_display = (
            'host',
            'path',
            'method',
            'exception_name',
            'count',
            'created_on',
            'last_seen',
            'notification_sent',
            'ticket_raised',
        )
        list_filter = (
            'host',
            'notification_sent',
            'ticket_raised',
        )
        search_fields = ('host', 'path', 'exception_name',)
        change_form_template = 'error_tracker/admin/change_form.html'

        def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
            if object_id:
                extra_context = {
                    'obj': ErrorModel.objects.get(pk=object_id)
                }
            return super(ErrorModelAdmin, self).changeform_view(request, object_id=object_id,
                                                                form_url=form_url, extra_context=extra_context)
