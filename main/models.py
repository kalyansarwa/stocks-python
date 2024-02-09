from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Now
from django.core.exceptions import ValidationError


def validate_zero(value):
    if value <= 0:
        raise ValidationError(
            _("%(value)s cannot be less than or equal to 0"),
            params={"value": value},
        )


class Portfolio(models.Model):
    portfolioName = models.CharField("Portfolio Name", max_length = 20)
    portfolioDescription = models.TextField("Description")

    class Meta:
        verbose_name_plural = "Portfolios"


class Transaction(models.Model):
    class TransactionTypes(models.TextChoices):
        BUY = "B", "Buy"
        SELL = "S", "Sell"
        DIV = "D", "Dividend"

    portfolioId = models.ForeignKey(Portfolio, default='', on_delete=models.SET_DEFAULT)
    transaction_date = models.DateField("Transaction Date",auto_now=True)
    symbol = models.CharField("Symbol", max_length=20)
    type = models.CharField("Transaction Type", max_length=2, default=TransactionTypes.BUY)
    quantity = models.IntegerField("Quantity", default=1, validators=[validate_zero])
    price = models.DecimalField("Price", max_digits=10, decimal_places=2, default=0.0, validators=[validate_zero])
    cost = models.DecimalField("BrokerageCost", max_digits=10, decimal_places=2, default=0.0, validators=[validate_zero])

    class Meta:
        verbose_name_plural = "Transactions"
        ordering = ['-transaction_date']
        constraints = [
            models.CheckConstraint(
                check=Q(transaction_date__gt=Now()),
                name="Date cannot be in future!!"
            )
        ]

    def __str__(self):
        return str(self.transaction_date) + ':' + str(self.symbol) + ':' + str(self.type)

