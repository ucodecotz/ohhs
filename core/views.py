from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
import stripe
from .filters import *
from .forms import *

# from .models import *

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    labours_qs = LaboursProfile.objects.filter(taken=False)[:8]
    labours_qs1 = LaboursProfile.objects.filter(taken=False)[8:]

    labour_filter = laboursFilterForm(request.GET, queryset=labours_qs)

    context = {
        'filter': labour_filter,
        'moreLabour': labours_qs1
    }
    return render(request, "home.html", context)


class laboursDetails(DetailView):
    model = LaboursProfile
    template_name = 'labourdetails.html'

    def get_context_data(self, *args, **kwargs):
        context = super(laboursDetails, self).get_context_data(**kwargs)
        form_class = commentForm()
        context.update({
            'form': form_class
        })
        return context


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form,
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            selected_labour_List = selectedList.objects.filter(
                selected_by=self.request.user, taken=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                # TODO add functionality to this advance field
                # same_contact_address = form.cleaned_data('same_contact_address')
                # save_info = form.cleaned_data('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                address = Address(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip_code=zip_code,
                    # payment_option=payment_option
                )
                address.save()
                # TODO add redirect to the select view
                messages.success(self.request, "your contact form has been submitted successfully")
                return redirect('core:checkout')
            else:
                messages.warning(self.request, "Form is invalid, try again")
                return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.warning(self.request, "Form is invalid")
            return redirect('core:checkout')


class LabourSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            form = commentForm()
            selected_list = selectedList.objects.get(user=self.request.user, taken=False)
            context = {
                'selected_list': selected_list,
                'form': form
            }
            return render(self.request, 'labour_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


def Add_to_selectedList(request, pk=None):
    labour = get_object_or_404(LaboursProfile, pk=pk)
    selected_Date = timezone.now()
    selected_labour, created = selectedLabour.objects.get_or_create(
        selected_by=request.user,
        labour=labour,
        taken=False,

    )
    selected_list_qs = selectedList.objects.filter(selected_by=request.user, taken=False)
    if selected_list_qs.exists():
        selected_list = selected_list_qs[0]
        if selected_list.labours.filter(labour__pk=labour.pk).exists():
            messages.info(request, "Try to add your home address")
            return redirect("core:checkout", )  # pk = labour.pk
        else:
            selected_list.labours.add(selected_labour)
            messages.info(request, "This labour was added to your labour list.")
            return redirect("core:checkout")
    else:
        selected_list = selectedList.objects.get_or_create(
            selected_by=request.user, selected_on=selected_Date)
        selected_list.selected_labours.add(selected_labour)
        messages.info(request, "This labour was added to your labour list")
        return redirect("core:details", pk=labour.pk)


class Payment(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')

    def post(self, *args, **kwargs):
        selected_labour = selectedList.objects.get(selected_by=self.request.user, taken=False)
        token = self.request.POST['stripeToken']

        charge = stripe.Charge.create(
            amount=1000,
            currency='usd',
            description='A Django charge',
            source=token
        )


def add_comment_to_selected_labour(request, pk=None):
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            labour = get_object_or_404(LaboursProfile, pk=pk)

            new_comment = comments(
                content=content,
                labour=labour,
                user=request.user

            )
            new_comment.save()
            messages.success(request, 'Your comment is submitted successfully')
            redirect('core:details', pk=pk)
        messages.success(request, 'form is not valid')
        redirect('core:details', pk=pk)

    messages.success(request, ' it is get request')
    redirect('core:details', pk=pk)