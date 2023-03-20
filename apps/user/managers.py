from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self,email,firstname,lastname,password=None):
        if not email:
            raise ValueError("Must have Email.")

        if not firstname:
            raise ValueError("Must have Firstname.")
        
        if not lastname:
            raise ValueError("Must have Lastname.")

        if not password:
            raise ValueError("Must have Password.")

        user = self.model(
            email = self.normalize_email(email),
            firstname=firstname,
            lastname=lastname
        )
        user.set_password(password)
        user.normal_user = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, firstname, lastname):
        user = self.create_user(email = email, password = password,firstname= 'Admin',lastname= 'User')
        user.admin = True
        user.active = True
        user.staff = True
        user.save(using = self._db)
        return user