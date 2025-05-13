from django.db import models
from django.utils import timezone
from users.models import Users
from django.core.exceptions import ValidationError

# Create your models here.
class Charity(models.Model):
    user = models.OneToOneField(Users, related_name="charity", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    bank_acc = models.IntegerField(unique=True)
    mission_statement = models.TextField(max_length=300)
    amount_needed = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()

    def clean(self):
        if self.deadline <= timezone.now().date():
            raise ValidationError({"error":"cannot set past date for deadline!!"})
        
        existing_charity = Charity.objects.filter(
            user = self.user,
            deadline__gt = timezone.now().date()
        ).exclude(pk = self.pk).first()

        if existing_charity:
            raise ValidationError({"error":"user can only have one active charity"})
        
        super().clean()

    def __str__(self):
        return self.name

class CharityUploads(models.Model):
    charity = models.OneToOneField(Charity, related_name="gvt_doc", on_delete=models.CASCADE)
    document = models.FileField(upload_to="gvt_docs/",)
    uploaded_date = models.DateField(default=timezone.now)
    # add label for the uploads (initial , phase achievement etc)

class CharityPhases(models.Model):
    charity = models.ForeignKey(Charity, related_name="charity_phases", on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)

class Donations(models.Model):
    VENDOR_CHOICE ={
        ("M Pesa","M Pesa"),
        ("Mixx","Mixx"),
        ("Airtel Money","Airtel Money"),
        ("HaloPesa","HaloPesa"),
        ("T Pesa","T Pesa")
    }

    user = models.ForeignKey(Users, related_name="donors_users", on_delete=models.CASCADE, blank=True, null=True)
    charity = models.ForeignKey(Charity, related_name="donations", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    vendor = models.CharField(choices=VENDOR_CHOICE,max_length=15)
    donated_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        # check if user is logged in or has email
        if not self.user:
            raise ValidationError({"error":"login to donate"})
        
        # get current amount already donated for this charity
        total_donated = Donations.objects.filter(charity=self.charity).exclude(pk = self.pk).aggregate(total = models.Sum('amount'))['total'] or 0

        # add current donation to the total donated
        if total_donated + self.amount > self.charity.amount_needed:
            raise ValidationError({"error":"this donation will exceed the amount needed for this charity"})

        return super().clean()
    
    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)