from django.contrib import admin
from .models import *


def make_request_refund_accepted(modeladmin, request, querytset):
    querytset.update(refund_requested=False, refund_granted=True, taken=True)


make_request_refund_accepted.short_description = 'Update orders to refund granted'


class selectedListAdmin(admin.ModelAdmin):
    list_display = ['selected_by',
                    'taken',
                    'refund_requested',
                    'refund_granted',]
    list_display_links = [
                    'selected_by',]
    list_filter = [
                    'taken',
                    'selected_on',]
    actions = [make_request_refund_accepted]


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
admin.site.register(LabourSelectedList, selectedListAdmin)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Work)
admin.site.register(Tribe)
admin.site.register(Religion)
admin.site.register(Refund)
admin.site.register(labourOfficialDoc)
admin.site.register(Contract)
admin.site.register(ContactModel)
