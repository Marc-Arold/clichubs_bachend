from django.db import models
from companies_accounts.models import CompanyProfile

class OfferType(models.Model):
    """
        A class representing the type of offer.
    """ 
      
    offer_type_name = models.CharField(max_length=255,unique=True,help_text="The type of offer we provide.",verbose_name="Offer Type Name")

    def __str__(self):
        """
        Returns a string representation of the offer type.
        """
        return self.offer_type_name


class LaunchedOffer(models.Model):

    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, to_field='company_id')
    price_offer_min = models.FloatField()
    gain_offer_max = models.FloatField()
    offer_type = models.ForeignKey(OfferType, on_delete=models.CASCADE)
    offer_launched_status = models.CharField(max_length=100)

    def __str__(self):
        return f"Offer from company {self.company_id} for {self.offer_type}"
