from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.models import BaseModel
import uuid
import random
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

NEW, VERIFIED, DONE = "NEW", "VERIFIED", "DONE"
USER, ADMIN, SUPERUSER = "USER", "ADMIN", "SUPERUSER"

class UserModel(AbstractUser, BaseModel):
    AUHT_STATUS = (
        (NEW, NEW),
        (VERIFIED, VERIFIED),
        (DONE, DONE),
    )
    
    USER_ROLE = (
        (USER, USER),
        (ADMIN, ADMIN),
        (SUPERUSER, SUPERUSER),
    )

    auth_status = models.CharField(max_length=10, choices=AUHT_STATUS, default=NEW)
    user_role = models.CharField(max_length=10, choices=USER_ROLE, default=USER)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    first_name = models.CharField(max_length=255) 
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    
    
    def __str__(self) -> str:
        return f"{self.username} - {self.user_role}"
    
    def check_name(self):
        if not self.username:
            new_add_username = f"{uuid.uuid4()}"
            while UserModel.objects.filter(username=new_add_username).exists():
               self.check_name()
            self.username = new_add_username
            
    
    def password_check(self):
        if not self.password:
            self.password = str(uuid.uuid4())
    
    def email_lowwer(self):
        self.email = self.email.lower()
        
    def securrty_password(self):
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)
            
    def clean(self):
        self.check_name()
        self.password_check()
        self.email_lowwer()
        self.securrty_password()
                
    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(UserModel, self).save(*args, **kwargs)
        
    def create_verify_code(self):
        code = random.randint(100000, 999999)
        UserCodeModel.objects.create(user=self, code=code)
        
        return code
        
    def get_token(self):
        resfresh = RefreshToken.for_user(self)
        
        res = {
            "refresh": str(resfresh),
            "access": str(resfresh.access_token)
        }
        return res


EMAIL_VERFIY_TIME = 10


class UserCodeModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_confirmed = models.BooleanField(default=False)
    expiration_time = models.DateTimeField()
    
    
    def __str__(self) -> str:
        return self.code
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_time = timezone.now() + timezone.timedelta(minutes=EMAIL_VERFIY_TIME)
        
        super(UserCodeModel, self).save(*args, **kwargs)
        