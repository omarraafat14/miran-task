from django.utils.crypto import get_random_string


class UserOtp:
    def send_otp(self, phone=None):
        phone = self.phone if phone is None else phone
        self.set_otp()
        text = f"Your one time password (OTP) for Business Meal is {self.verification_code}"
        self.send_sms(phone, text)

    def set_otp(self):
        self.verification_code = self.generate_otp()
        self.save()

    def generate_otp(self):
        return get_random_string(length=4, allowed_chars="0123456789")

    def send_sms(self, phone, text):
        pass


class UserMixin(UserOtp):
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def soft_delete(self):
        self.is_deleted = True
        user_email = self.email
        random = get_random_string(10)
        self.email = user_email + random
        self.save()
        return self

    @classmethod
    def create_user_or_login(cls, validated_data):
        user, _ = cls.objects.get_or_create(phone=validated_data["phone"])
        user.send_otp()
        return user
