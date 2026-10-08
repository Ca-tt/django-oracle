from django.views.generic import TemplateView

# Static Pages
class AboutView(TemplateView):
    template_name = "store/pages/about.html"

class ContactView(TemplateView):
    template_name = "store/pages/contact.html"

class ProfileView(TemplateView):
    template_name = "store/account/profile.html"

class GoogleSignupView(TemplateView):
    template_name = "store/account/socialaccount/signup.html"