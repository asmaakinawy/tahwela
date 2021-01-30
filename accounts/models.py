from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.utils import timezone




def photos_directory_path(instance, filename):
    """Get photos path directory for each Owner."""
    return 'users/{0}/{1}'.format(instance.id, filename+str(now()))


class AccountData(AbstractUser):
    # mobile number is saved in the username field
    email = models.EmailField(max_length=128, unique=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to=photos_directory_path, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    balance = models.CharField(max_length=128, null=True, blank=True, default=0)
    addings_per_day = models.CharField(max_length=128, null=True, blank=True, default=0)
    addings_per_week = models.CharField(max_length=128, null=True, blank=True, default=0)
    expenses_per_day = models.CharField(max_length=128, null=True, blank=True, default=0)
    expenses_per_week = models.CharField(max_length=128, null=True, blank=True)
    date_of_birth	   = models.DateField(null=True,blank=True)
    city 	   		   = models.CharField(max_length=255,default='',null=True,blank=True)
    gender 		   	   = models.TextField(default='', null=True, blank=True)
    idnumber 	   		= models.CharField(max_length=255, null=True, blank=True)

    def add_balance(self, balance):
        self.addings_per_week = int(str(self.addings_per_week)) + int(balance)
        self.addings_per_day = int(str(self.addings_per_day)) + int(balance)
        self.balance = int(str(self.balance)) + int(balance)
        self.save()
        return self.balance

    def is_allowed_to_add_balance(self, balance):
        if (int(str(self.addings_per_day)) + int(balance)) <= 10000 and (int(str(self.addings_per_week)) + int(balance)) <= 50000:
            return True
        return False

    def deducte_balance(self, balance):
        self.balance = int(str(self.balance)) - int(balance)
        self.save()


class BankAccountManage(models.Manager):
    def connect_bank_account(self, username, bank_name, branch_name, account_number, account_holder, bank_reference, reference=None):
        return self.create(user=username, bank_name=bank_name, branch_name=branch_name, account_number=account_number,
                           time_creation=timezone.now(), account_holder=account_holder, bank_reference=bank_reference, reference=reference)


class BankAccount(models.Model):
    bank_name       = models.CharField(max_length=128, blank=False, null=False)
    branch_name     = models.CharField(max_length=128, blank=False, null=False)
    account_number  = models.CharField(max_length=128, blank=False, null=False)
    account_holder  = models.CharField(max_length=128, blank=False, null=False)
    reference       = models.CharField(max_length=128, blank=True, null=True)
    bank_reference   = models.CharField(max_length=128, blank=False, null=False)
    time_creation   = models.DateTimeField(default=timezone.now)
    user            = models.ForeignKey(AccountData, on_delete=models.CASCADE)
    objects         = BankAccountManage()

