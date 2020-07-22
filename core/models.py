from django.db import models
from django.conf import settings
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
    user = models.ForeignKey(UserProfile,
                             on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to='profile_pic', null=True)
    dob = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    label = models.CharField(max_length=20, choices=LABEL, null=True)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, null=True, blank=True)
    tribe = models.ForeignKey(Tribe,  on_delete=models.CASCADE, null=True)
    work = models.ForeignKey(Work,  on_delete=models.CASCADE, null=True, blank=True)

    # religion = models.CharField(max_length=29,  null=True, blank=True)
    # tribe = models.CharField(max_length=29,  null=True, blank=True)
    # work = models.CharField(max_length=29,  null=True, blank=True)
    taken = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    update_on = models.DateTimeField(default=timezone.now)
    charges = models.FloatField(default=100)

    class Meta:
        verbose_name_plural = 'labours'

    def __str__(self):
        return str(self.user.user)

    def get_absolute_url(self):
        title = self.work.name.replace(" ", "-")
        return reverse('core:details', args=[str(self.pk)])

    def get_add_to_selected_list(self):
        return reverse('core:add_to_selected_list', args=[str(self.pk)])

    def convert_charges_tzsh(self):
        return self.charges * 2316


class selectedLabour(models.Model):
    selected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    labour = models.ForeignKey(LaboursProfile, on_delete=models.CASCADE)
    taken = models.BooleanField(default=False)
    selected_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Selected labour'

    def __str__(self):
        return str(self.labour)


class selectedList(models.Model):
    selected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    labours = models.ManyToManyField(selectedLabour)
    taken = models.BooleanField(default=False)
    selected_on = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField("comments")
    employer_address = models.ForeignKey("Address", on_delete=models.SET_NULL, null=True, blank=True)
    charges = models.FloatField(default=100, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Selected list'

    def __str__(self):
        return str(self.selected_by)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False, null=True)
    zip_code = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Employer addresses"

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Payments"

    def __str__(self):
        return self.user.username


class comments(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, null=True)
    labour = models.ForeignKey(LaboursProfile, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.user.username
