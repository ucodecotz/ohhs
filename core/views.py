import random
import string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView

from .filters import laboursFilterForm
from .models import *
import stripe
from paypal.standard.forms import PayPalPaymentsForm
from .forms import commentForm, CheckoutForm, Payment_form, RequestRefundForm, ContractForm, UnknownUserContactForm

# from .models import *
stripe.api_key = 'sk_test_49wnT6UBUcbntz1gaaugRs8u00dEtnmXa3'


# stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    labours_qs = LaboursProfile.objects.filter(taken=False)[:8]

    labour_filter = laboursFilterForm(request.GET, queryset=labours_qs)

    context = {
        'Labour_list': labours_qs,

        'worklist': Work.objects.filter(laboursprofile__taken=False),
        'tribelist': Tribe.objects.filter(laboursprofile__taken=False),
        'religionklist': Religion.objects.filter(laboursprofile__taken=False),

    }
    return render(request, "home.html", context)


class ContactView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'contact.html')

    def post(self, *args, **kwargs):
        form = UnknownUserContactForm(self.request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data.get('contact_name')
            contact_email = form.cleaned_data.get('contact_email')
            contact_phone = form.cleaned_data.get('contact_phone')
            contact_company = form.cleaned_data.get('contact_company')
            contact_message = form.cleaned_data.get('contact_message')

            new_contact = ContactModel()
            new_contact.contact_name = contact_name
            new_contact.contact_email = contact_email
            new_contact.contact_phone = contact_phone
            new_contact.contact_company = contact_company
            new_contact.contact_message = contact_message
            new_contact.save()
            messages.success(self.request, 'Thanks for contact us')
            return redirect('/')
        else:
            messages.success(self.request, 'Form is not fully complete')
            return redirect('/')


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
            selected_labour_List = LabourSelectedList.objects.filter(
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
                    payment_option=payment_option
                )
                address.save()
                for labour_list in selected_labour_List:
                    labour_list.payment_option = payment_option
                    labour_list.save()

                # TODO add redirect to the select view
                # if payment_option == 'S':
                #     messages.success(self.request, "Thanks for choosing stripe")
                #     return redirect('core:payment', payment_option='stripe')
                # elif payment_option == 'P':
                #     messages.success(self.request, "Thanks for choosing Airtell")
                #     return redirect('core:paypal')
                # else:
                #     messages.warning(
                #         self.request, "Invalid payment option selected")
                #     return redirect('core:checkout')
                messages.success(self.request, "Thanks for choosing stripe")
                return redirect('core:contract')
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
            selected_list = LabourSelectedList.objects.get(user=self.request.user, taken=False)
            context = {
                'selected_list': selected_list,
                'form': form
            }
            return render(self.request, 'labour_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def Add_to_selectedList(request, pk=None):
    labour = get_object_or_404(LaboursProfile, pk=pk)
    selected_Date = timezone.now()

    selected_labour, created = selectedLabour.objects.get_or_create(
        selected_by=request.user,
        labour=labour,
        taken=False,
    )

    selected_list_qs = LabourSelectedList.objects.filter(selected_by=request.user, taken=False)
    if selected_list_qs.exists():
        selected_list = selected_list_qs[0]
        if selected_list.labours.filter(labour__pk=labour.pk).exists():
            messages.info(request, "You already requested this worker, Continue to Contact form")
            return redirect("core:details", pk=labour.pk)  # pk = labour.pk
        else:
            selected_list.labours.add(selected_labour)
            messages.success(request, "This labour was added to your labour list.")
            return redirect("core:checkout")
    else:
        selected_list = LabourSelectedList.objects.create(
            selected_by=request.user, selected_on=selected_Date)
        selected_list.labours.add(selected_labour)
        messages.success(request, "This labour was added to your labour list")
        return redirect("core:details", pk=labour.pk)


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class PaymentView(View):
    def get(self, *args, **kwargs):
        labour_list = LabourSelectedList.objects.filter(
            selected_by=self.request.user,
            taken=False
        )
        context = {
            'payment': labour_list
        }
        return render(self.request, 'payment.html', context)

    def post(self, *args, **kwargs):
        selected_list = LabourSelectedList.objects.get(selected_by=self.request.user, taken=False)
        token = self.request.POST.get('stripeToken')
        amount = int(selected_list.get_total() * 100)
        form = Payment_form(self.request.POST)
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )
            payment = Payment()
            payment.user = self.request.user
            payment.stripe_charge_id = charge['id']
            payment.amount = selected_list.get_total()
            payment.timestamp = timezone.now()
            payment.save()

            # update the selected worker
            labour_selected = selected_list.labours.all()
            labour_selected.update(taken=True)
            for my_labour in labour_selected:
                if my_labour.labour.id == selected_list.id:
                    my_labour.labour.taken = True
                my_labour.save()

            # update the selected labour details
            selected_list.taken = True
            selected_list.is_paid = True
            selected_list.ref_code = create_ref_code()
            selected_list.payment = payment
            selected_list.save()

            labours_qset = LaboursProfile.objects.filter(selectedlabour__taken=True)
            for labour in labours_qset:
                labour.taken = True
                labour.save()

            #  update the labour for taken in selected_labour.
            messages.info(self.request, 'your request was successfully')
            return redirect('/')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.warning(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")


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
            return redirect('core:details', pk=pk)
        else:
            messages.success(request, 'Form is not valid')
            return redirect('core:details', pk)

    messages.success(request, ' it is get request')
    return redirect('core:details', pk=pk)


class MyAccount(View):
    def get(self, *args, **kwargs):
        contract = Contract.objects.filter(user=self.request.user)
        refund = Refund.objects.filter(made_by=self.request.user, accepted=True)
        payment = Payment.objects.filter(user=self.request.user)
        requests_made = LabourSelectedList.objects.filter(selected_by=self.request.user, taken=True)
        context = {
            'contract': contract,
            'refund': refund,
            'payment': payment,
            'request_made': requests_made
        }
        return render(self.request, 'account.html', context)


def contract_view(request):
    contract = Contract.objects.filter(user=request.user, agree=True)
    context = {
        'contract': contract
    }
    return render(request, 'contract_agreed.html', context)


def refund_view(request):
    refund = Refund.objects.filter(made_by=request.user, )
    context = {
        'refund': refund
    }
    return render(request, 'refund accepted.html', context)


def payments_view(request):
    contract = Contract.objects.filter(user=request.user)
    context = {
        'contract': contract
    }
    return render(request, 'payments.html')


# TODO complete this future
def LabourYourSelected(request, pk=None):
    try:
        queryset = LabourSelectedList.objects.get(selected_by=request.user or None, taken=True, pk=pk or None)
        context = {
            'selected_list': queryset
        }
        return render(request, 'selected_labour.html', context)
    except ObjectDoesNotExist:
        messages.info(request, 'No requests for now')
        return redirect('core:myaccount')


def view_that_asks_for_money(request):
    # What you want the button to do.
    selected_list = selectedLabour.objects.get(selected_by=request.user, taken=False)
    amount = int(selected_list.get_total() * 100)
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount,
        "item_name": selected_list.id,
        "invoice": selected_list.id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('core:payment_done')),
        "cancel_return": request.build_absolute_uri(reverse('core:payment_cancelled')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "paypal_payment.html", context)


def payment_done(request):
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')


class RequestFund(View):
    def get(self, *args, **kwargs):
        form = RequestRefundForm()
        context = {
            'refund_form': form
        }
        return render(self.request, 'refund.html', context)

    def post(self, *args, **kwargs):
        form = RequestRefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                selected_labour = LabourSelectedList.objects.get(ref_code=ref_code)
                selected_labour.refund_requested = True
                selected_labour.save()

                refund = Refund()
                refund.ref_code = ref_code
                refund.made_by = self.request.user
                refund.reason = message
                refund.email = email
                refund.save()
                messages.info(self.request, 'your request was received')
                return redirect('core:myaccount')
            except ObjectDoesNotExist:
                messages.info(self.request, "No refund made")
                return redirect('core:myaccount')
        return redirect('core:myaccount')

class ContractView(View):
    def get(self, *args, **kwargs):
        queryset = selectedLabour.objects.filter(selected_by=self.request.user, taken=False)
        context = {
            'contract': queryset
        }
        return render(self.request, 'contract.html', context)

    def post(self, *args, **kwargs):
        form = ContractForm(self.request.POST)
        if form.is_valid():
            agree = form.cleaned_data.get('agree')
            queryset = selectedLabour.objects.filter(selected_by=self.request.user, taken=False)

            contracts = f"""
            THIS AGREEMENT made between {str(self.request.user)} as employer and 'Got to your labour list'  as 
employee on [date of contract], 
            WHEREAS the Employer desires to obtain the benefit of the services of the Employee, and the Employee 
desires to render such services on the terms and conditions set forth. 
            IN CONSIDERATION of the promises and other good and valuable consideration Employer should agree as follows:
            • Payments
            Here Employer should make first payment as commission fee as charges from a company. Employee Salary 
should be agreed between Employee and His/her Employer according to different facts such as size of the family, 
type of work/s etc. 
            • Employment
            The Employee agrees that he will at all times faithfully, and to the best of his skill, ability, 
experience and talents, perform all of the duties required of his position. In carrying out these duties and 
responsibilities, the Employee shall comply with all Employer policies, procedures, rules and regulations, 
both written and oral, as are announced by the Employer from time to time. It is also understood and agreed to by the 
Employee that his assignment, duties and responsibilities and reporting arrangements may be changed by the Employer 
in its sole discretion without causing termination of this agreement. 
            • Termination
            A. The Employee may at any time terminate this agreement and his employment by giving not less than two 
weeks written notice to the Employer. 
            B. The Employer may terminate this Agreement and the Employee’s employment at any time, without notice or 
payment in lieu of notice, for sufficient cause. 
            C. The Employer may terminate the employment of the Employee at any time without the requirement to show 
sufficient cause pursuant to (b) above, provided the Employer pays to the Employee an amount as required by the 
Employment Standards Act 2000 or other such legislation as may be in effect at the time of termination. This payment 
shall constitute the employees entire entitlement arising from said termination. 
            D.  The employee agrees to return any property of Employer at the time of termination.
            """
            contract = Contract()
            contract.user = self.request.user
            contract.contract = contracts
            contract.agree = agree
            contract.save()
            messages.info(self.request, 'Thanks for submitting a signed contract, Continue to payment')
            return redirect('core:payment', payment_option='stripe')
        else:
            messages.info(self.request, 'Try to fill all fields')
            return redirect('core:contract')
