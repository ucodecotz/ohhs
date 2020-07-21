from django.contrib import admin
from .models import *


class selectedListAdmin(admin.ModelAdmin):
    list_display = ['selected_by',
                    'taken',

                    ]
    list_display_links = [
        'selected_by',

    ]


class selectedLabourAdmin(admin.ModelAdmin):
    list_display = ['selected_by',
                    'labour',
                    'taken',
                    'selected_on',

                    ]
    list_display_links = [
        'selected_by',
        'labour',

    ]


admin.site.register(LaboursProfile)
admin.site.register(comments)
admin.site.register(UserProfile)
admin.site.register(selectedLabour, selectedLabourAdmin)
admin.site.register(selectedList, selectedListAdmin)
admin.site.register(Address)
