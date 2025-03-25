from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group


class CategoriesViewTests(APITestCase):
    def setUp(self):
        # Create a test category
        Category.objects.create(title="Test Category")

    def test_get_categories(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_unauthenticated(self):
        data = {"title": "New Category"}
        response = self.client.post(reverse('categories'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_authenticated(self):
        self.client.force_authenticate(user=User.objects.create_user(username="testuser"))
        data = {"title": "New Category"}
        response = self.client.post(reverse('categories'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class MenuItemsViewTests(APITestCase):
    def setUp(self):
        # Create a test menu item
        self.menu_item = MenuItem.objects.create(title="Test Menu Item", price=10, inventory=5)

    def test_get_menu_items(self):
        response = self.client.get(reverse('menu-items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_menu_item_unauthenticated(self):
        data = {"title": "New Item", "price": 15, "inventory": 10}
        response = self.client.post(reverse('menu-items'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_menu_item_authenticated(self):
        self.client.force_authenticate(user=User.objects.create_user(username="testuser"))
        data = {"title": "New Item", "price": 15, "inventory": 10}
        response = self.client.post(reverse('menu-items'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CartViewTests(APITestCase):
    def setUp(self):
        # Create a test user and cart
        self.user = User.objects.create_user(username="testuser")
        self.cart = Cart.objects.create(user=self.user)

    def test_get_cart_unauthenticated(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_cart_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cart_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderViewTests(APITestCase):
    def setUp(self):
        # Create a test user, cart, and order
        self.user = User.objects.create_user(username="testuser")
        self.cart = Cart.objects.create(user=self.user)
        self.order = Order.objects.create(user=self.user, total=100)

    def test_get_orders_unauthenticated(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_orders_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        data = {"cart": self.cart.id}
        response = self.client.post(reverse('orders'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GroupViewSetTests(APITestCase):
    def setUp(self):
        # Create a test user and admin group
        self.admin_user = User.objects.create_superuser(username="admin", password="password")
        self.user = User.objects.create_user(username="testuser")
        self.manager_group = Group.objects.create(name="Manager")

    def test_add_user_to_manager_group(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"username": self.user.username}
        response = self.client.post(reverse('add-manager'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_user_from_manager_group(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"username": self.user.username}
        response = self.client.delete(reverse('remove-manager'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeliveryCrewViewSetTests(APITestCase):
    def setUp(self):
        # Create a test user, manager, and delivery crew group
        self.admin_user = User.objects.create_superuser(username="admin", password="password")
        self.user = User.objects.create_user(username="testuser")
        self.manager_group = Group.objects.create(name="Manager")
        self.delivery_group = Group.objects.create(name="Delivery Crew")

    def test_add_user_to_delivery_crew(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"username": self.user.username}
        response = self.client.post(reverse('add-delivery-crew'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_user_from_delivery_crew(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"username": self.user.username}
        response = self.client.delete(reverse('remove-delivery-crew'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
