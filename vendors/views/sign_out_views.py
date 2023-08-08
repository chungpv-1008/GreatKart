from django.contrib.auth.views import LogoutView


class SignOutView(LogoutView):
    template_name = 'vendor/sign_out.html'

    def get_next_page(self):
        # Custom logic to determine the redirect URL based on user attributes or other conditions.
        return '/vendor/sign-in'