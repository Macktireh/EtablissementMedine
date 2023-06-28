from typing import cast

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from apps.orders.models import Order, OrderStatusChoices
from apps.orders.types import ActionOrderQuantity
from apps.products.models import Product
from apps.users.types import UserType

User = cast(UserType, get_user_model())


# class OerderService:
#     @staticmethod
#     def add_to_cart(user: User, productPublicId: str) -> None:
#         product = get_object_or_404(Product, public_id=productPublicId)
#         cart, _ = Cart.objects.get_or_create(user=user, order_status=OrderStatusChoices.PENDINGG)
#         order, created = Order.objects.get_or_create(user=user, product=product, ordered=False)

#         if created:
#             cart.orders.add(order)
#             cart.save()
#         else:
#             order.quantity += 1
#             order.save()

#     @staticmethod
#     def update_order_quantity(orderPublicId: str, actionQuantity: ActionOrderQuantity) -> None:
#         order = get_object_or_404(Order, public_id=orderPublicId)
#         if actionQuantity == ActionOrderQuantity.INCREASE:
#             order.quantity += 1
#         elif actionQuantity == ActionOrderQuantity.REDUCE:
#             order.quantity -= 1
#         order.save()

#     @staticmethod
#     def delete_order(orderPublicId: str) -> None:
#         order = get_object_or_404(Order, public_id=orderPublicId)
#         order.delete()
