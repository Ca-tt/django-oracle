from django.urls import path, include
from store.views import *

#! Add dedicated pages for category and subcategory

urlpatterns = [
    # pages
    path('', home, name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path("search/", search_results, name="search_results"),
    
    # store
    path("products/", products, name="products"),
    path("products/<slug:slug>/", single_product, name="product_single"),
    
    # auth
    path("account/profile/", ProfileView.as_view(), name="profile"),
    # path("account/3rdparty/signup/", GoogleSignupView.as_view(), name="google_signup"),
   
    # extra
    path("not-found-preview/", NotFoundPreview.as_view(), name="not_found_preview"),
    
]

