import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView, DetailView

from mainapp.models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        item_id = self.kwargs["pk"]
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        if 'item' in request.META.get('HTTP_REFERER'):
            item = Item.objects.get(id=item_id)
            YOUR_DOMAIN = "http://127.0.0.1:8000"
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': item.price,
                            'product_data': {
                                'name': item.name
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                },
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        else:
            order = Order.objects.get(id=item_id)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': order.get_total_cost(),
                            'product_data': {
                                'name': f'заказ №{order.pk}'
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                },
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
            return JsonResponse({
                'id': checkout_session.id
            })


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class ItemLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        item = get_object_or_404(Item, pk=self.kwargs.get('pk'))
        context = super(ItemLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "item": item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class OrderDetail(DetailView):
    model = Order
    template_name = 'order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context
