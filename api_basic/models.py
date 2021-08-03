from django.db import models

# Create your models here.
class Ticket(models.Model):
    ticker_id = models.CharField(max_length=20)
    ticker_name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.ticker_id