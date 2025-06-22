from django.contrib import admin
from .models import Guard, Visitor

class GuardAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'user', 'delete_button')

    def delete_button(self, obj):
        return f'<a href="/admin/gateapp/guard/{obj.id}/delete/" class="button">Delete</a>'
    
    delete_button.allow_tags = True
    delete_button.short_description = 'Actions'

admin.site.register(Guard, GuardAdmin)
admin.site.register(Visitor)