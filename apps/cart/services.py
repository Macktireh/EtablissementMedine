from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from apps.cart.models import Cart, OrderItem
from apps.products.models import Product


class CartService:
    @staticmethod
    def add_to_cart(request: HttpRequest, product_public_id: str) -> None:
        """
        Add a product to the user's cart.

        Args:
            request (HttpRequest): The HTTP request object.
            product_public_id (str): The public ID of the product to be added to the cart.

        Returns:
            None
        """
        product = get_object_or_404(Product, public_id=product_public_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = OrderItem.objects.get_or_create(user=request.user, product=product, ordered=False)

        if created:
            cart.orders_items.add(item)
            cart.save()
        else:
            item.quantity += 1
            item.save()

    @staticmethod
    def update_order_item_quantity(order_item_public_id: str, quantity: int) -> None:
        """
        Update the quantity of an order item.

        Args:
            order_item_public_id (str): The public ID of the order item.
            quantity (int): The new quantity.

        Returns:
            None
        """
        item = get_object_or_404(OrderItem, public_id=order_item_public_id)
        item.quantity = quantity
        item.save()

    @staticmethod
    def order_item_increment_quantity(order_item_public_id: str) -> None:
        """
        Increment the quantity of an order item by 1.

        Args:
            order_item_public_id (str): The public ID of the order item.

        Returns:
            None
        """
        item = get_object_or_404(OrderItem, public_id=order_item_public_id)
        item.quantity += 1
        item.save()

    @staticmethod
    def order_item_decrement_quantity(order_item_public_id: str) -> None:
        """
        Decrement the quantity of an order item by 1.

        Args:
            order_item_public_id (str): The public ID of the order item.

        Returns:
            None
        """
        item = get_object_or_404(OrderItem, public_id=order_item_public_id)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()

    @staticmethod
    def delete_to_cart(request: HttpRequest, order_item_public_id: str) -> None:
        """
        Delete an order item from the user's cart.

        Args:
            request (HttpRequest): The HTTP request object.
            order_item_public_id (str): The public ID of the order item.

        Returns:
            None
        """
        item = get_object_or_404(OrderItem, public_id=order_item_public_id)
        item.delete()

    @staticmethod
    def clear_cart(request: HttpRequest) -> None:
        """
        Clear all items the cart for the given user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            None
        """
        cart = get_object_or_404(Cart, user=request.user)
        cart.clear()
