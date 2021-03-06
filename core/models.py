from datetime import date, timedelta

from django.db import models
from django.conf import settings
from django.db.models.functions import datetime
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)
LOCATION = (
    ('AR', 'Arusha'),
    ('DA', 'Dar es salaam'),
)
RELIGION = (
    ('MU', 'Muslims'),
    ('CH', 'Christianity'),
)
TRIBE = (
    ('HY', 'Haya'),
    ('SK', 'Sukluma'),
)
LABEL = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'default'),
    ('Da', 'danger'),

)
PAYMENT_OPTIONS = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

"""
CREATE TABLE TABALENAME (  username, firstname

"""


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=100, null=True, choices=LOCATION)
    phone_number = models.CharField(max_length=13, null=True)
    is_worker = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'User profile'

    def __str__(self):
        return self.user.username


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


class Tribe(models.Model):
    name = models.CharField(max_length=39, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Tribe'

    def __str__(self):
        return self.name


class Work(models.Model):
    name = models.CharField(max_length=39, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Work'

    def __str__(self):
        return str(self.name)


class Religion(models.Model):
    name = models.CharField(max_length=39, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Religion'

    def __str__(self):
        return str(self.name)


class LaboursProfile(models.Model):
    Full_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.FileField(upload_to='profile_pic', null=True)
    dob = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    label = models.CharField(max_length=20, choices=LABEL, null=True)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, null=True, blank=True)
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE, null=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, null=True, blank=True)
    taken = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    update_on = models.DateTimeField(default=timezone.now)
    charges = models.IntegerField(default=100)
    phone_number = models.CharField(max_length=13, null=True)
    location = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name_plural = 'labours'

    def __str__(self):
        return str(self.Full_name)

    def get_absolute_url(self):
        title = self.work.name.replace(" ", "-")
        return reverse('core:details', args=[str(self.pk)])

    def get_add_to_selected_list(self):
        return reverse('core:add_to_selected_list', args=[str(self.pk)])

    def convert_charges_tzsh(self):
        return int(self.charges) * 2316

    def get_age(self):
        today = date.today()
        y = today.year - self.dob.year
        if today.month < self.dob.month or today.month == self.dob.month and today.day < self.dob.day:
            y -= 1
        return f'{y} year old'


class labourOfficialDoc(models.Model):
    nida = models.FileField(upload_to='doc')
    labour = models.ForeignKey(LaboursProfile, on_delete=models.CASCADE)
    created = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Labour doc'

    def __str__(self):
        return str(self.labour.user)


class selectedLabour(models.Model):
    selected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    labour = models.ForeignKey(LaboursProfile, on_delete=models.CASCADE)
    taken = models.BooleanField(default=False)
    selected_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Selected labour'

    def __str__(self):
        return str(self.labour)

    def get_labour_price(self):
        return self.labour.charges

    def get_full_name(self):
        return str(self.labour.Full_name)


class LabourSelectedList(models.Model):
    ref_code = models.CharField(max_length=30, null=True, blank=True)
    selected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    labours = models.ManyToManyField(selectedLabour)
    taken = models.BooleanField(default=False)
    selected_on = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField("comments")
    employer_address = models.ForeignKey("Address", on_delete=models.SET_NULL, null=True, blank=True)
    charges = models.FloatField(default=100, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(default=False)
    payment_option = models.CharField(max_length=200, null=True, blank=True, choices=PAYMENT_OPTIONS)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Selected list'

    def __str__(self):
        return str(self.selected_by)

    def get_total(self):
        total = 0
        for order_item in self.labours.all():
            total += order_item.get_labour_price()
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False, null=True)
    zip_code = models.CharField(max_length=200)
    payment_option = models.CharField(max_length=200, null=True, blank=True, choices=PAYMENT_OPTIONS)

    class Meta:
        verbose_name_plural = "Employer addresses"

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_created=True)

    class Meta:
        verbose_name_plural = "Payments"

    def __str__(self):
        return self.user.username


class comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    labour = models.ForeignKey(LaboursProfile, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    content = models.TextField()

    class Meta:
        verbose_name_plural = ' System blog'

    def __str__(self):
        return self.title


class Refund(models.Model):
    ref_code = models.CharField(max_length=200, null=True, blank=True)
    made_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, null=True)

    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.ref_code}"


class Contract(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    contract = models.TextField()
    signed_at = models.DateTimeField(default=timezone.now)
    agree = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Contract'

    def __str__(self):
        return str(self.user)


class ContactModel(models.Model):
    contact_name = models.CharField(max_length=23, null=True)
    contact_email = models.CharField(max_length=30, null=True)
    contact_phone = models.CharField(max_length=30, null=True, )
    contact_company = models.CharField(max_length=20, null=True)
    contact_message = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Contact'

    def __str__(self):
        return self.contact_name
