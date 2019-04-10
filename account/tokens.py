from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_vlaue(self, user, timestamp):
        return (str(user.pk)+str(timestamp)+str(user.is_active))

account_activation_token = TokenGenerator()