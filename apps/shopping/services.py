from django.shortcuts import get_object_or_404

from apps.auth.models import User
from apps.product.models import Product
from apps.shopping.models import Cart, Order, OrderStatusChoices


class ShoppingService:
    
    @staticmethod
    def add_to_cart(user: User, productPublicId: str) -> None:
        product = get_object_or_404(Product, public_id=productPublicId)
        cart, _ = Cart.objects.get_or_create(user=user, order_status=OrderStatusChoices.PENDINGG)
        order, created = Order.objects.get_or_create(user=user, product=product, ordered=False)

        if created:
            cart.orders.add(order)
            cart.save()
        else:
            order.quantity += 1
            order.save()
