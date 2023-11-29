from django.db import models
from django.contrib.auth.models import User

from accounts.models import UserContactInformation


class Discount(models.Model):
    percentage_of_discount = models.IntegerField()


class PaymentOptions(models.Model):
    month_trial = models.IntegerField()
    price = models.FloatField()
    option_description = models.TextField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)


class PaymentStatus(models.Model):
    status = models.CharField(max_length=50)


class UserPaymentCard(models.Model):
    card_number = models.IntegerField()
    expiry_date = models.CharField(max_length=5)
    security_code = models.IntegerField()
    name_of_card = models.CharField(max_length=50)
    address = models.ForeignKey(UserContactInformation, on_delete=models.CASCADE, related_name='userpaymentcard_address')
    country = models.ForeignKey(UserContactInformation, on_delete=models.CASCADE, related_name='userpaymentcard_country')
    city = models.ForeignKey(UserContactInformation, on_delete=models.CASCADE, related_name='userpaymentcard_city')
    postal_code = models.ForeignKey(UserContactInformation, on_delete=models.CASCADE, related_name='userpaymentcard_postal_code')


class UserPaymentModel(models.Model):
    option = models.ForeignKey(PaymentOptions, on_delete=models.CASCADE)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=20, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
