from django.urls import path

from products.views import ProductsView, ProductView

urlpatterns = [
    path('', ProductsView.as_view()),
    path('/<int:product_id>', ProductView.as_view())
]
