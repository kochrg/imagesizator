import os

from datetime import timedelta, datetime
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.timezone import now as timezone_now
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from stat import S_IRWXG, S_IRWXU
from tempfile import NamedTemporaryFile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Parameters(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # recommended key format = endpoint_name_parameter_name
    key = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text="Ingrese el nombre del parámetro",
    )
    value = models.TextField(
        default='',
        help_text="Ingrese el valor del parámetro",
    )

    class Meta:
        verbose_name = "Parameter"
        verbose_name_plural = "Parameters"

    def __str__(self):
        return self.key

    @staticmethod
    def get_parameter_value(key):
        try:
            parameter = Parameters.objects.get(key=key)

            if parameter.value == 'None':
                return None

            return parameter.value
        except Parameters.DoesNotExist:
            print("Error getting parameter: " + str(key))
        except Exception as e:
            print("Error (get_aparameter_value):", e)

        return False

    @staticmethod
    def add_parameter_if_not_exists(key, value):
        """
        Add a parameter if it not exists in database.
        """
        parameter = Parameters.get_parameter_value(key)

        if parameter is not None:
            if not parameter:
                print("Adding parameter:", key)
                Parameters(
                    key=key,
                    value=value
                ).save()
                return True

        return False


class ImagesizatorFile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(
        max_length=100,
        null=False
    )
    path = models.TextField(
        null=False,
        blank=False,
        help_text="File path",
    )
    prefix = models.CharField(
        max_length=50,
        null=True
    )
    suffix = models.CharField(
        max_length=10,
        null=True
    )
    # bytes_string = decoded_file = base64.b64decode(request.data["file"])
    bytes_string = models.TextField(
        default='',
        help_text="Image as a byte string",
    )
    is_protected = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )
    is_static = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )
    expiration_date = models.DateTimeField(
        "Expiration date (valid until)",
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        verbose_name = "Imagesizator file"
        verbose_name_plural = "Imagesizator files"

    def __str__(self):
        return self.path

    @property
    def url(self):
        file_url = Parameters.get_parameter_value('imagesizator_domain') + "/"
        return  file_url + self.publish_path + self.file_name

    @property
    def publish_path(self):
        path = ""
        if self.is_protected:
            if self.is_temporal:
                path += settings.PROTECTED_FOLDER + "/temp/"
            else:
                path = settings.PROTECTED_FOLDER + "/static/"
        else:
            if self.is_temporal:
                path += settings.PUBLIC_FOLDER + "/temp/"
            else:
                path = settings.PUBLIC_FOLDER + "/static/"
        return path

    @property
    def is_temporal(self):
        return not self.is_static

    def set_named_temporary_file(self, suffix, prefix='file_'):
        temporary_file = NamedTemporaryFile(
            "r+b",
            prefix=prefix,
            suffix=suffix,
            dir=self.publish_path,
            delete=False
        )

        # chmod 770 (Grant rwx access to www-data.www-data 'user and group')
        os.chmod(temporary_file.name, S_IRWXU + S_IRWXG)
        self.path = temporary_file.name
        self.file_name = temporary_file.name.split("/")[-1]
        self.prefix = prefix
        self.suffix
        return temporary_file

    def set_file_expiration_date(self, expiration=None):
        # expiration = 60*60*24. Default: 24hs.
        seconds = expiration
        try:
            if seconds is None:
                # Custom defaul_expiration_time in config?
                user_default = int(Parameters.get_parameter_value('default_expiration_time'))  # seconds
                if user_default:
                    seconds = user_default
                else:
                    seconds = 60*60*24
            # else: use expiration from parameter (default)
        except Exception as e:
            pass

        if not self.created_at:
            self.created_at = datetime.now()
        self.expiration_date = self.created_at + timedelta(seconds=int(seconds))

        return self.expiration_date

    def delete(self):
        try:
            os.remove(r"" + str(self.path))
            super(ImagesizatorFile, self).delete()
        except Exception as e:
            print(e)

    def save(self, *args, **kwargs):
        if not self.path:
            any_type_file = self.set_named_temporary_file(
                self.suffix,
                'file_' + self.suffix.replace(".", "") + "_",
            )
            any_type_file.write(self.bytes_string)
            any_type_file.close()
  
        if self.is_temporal and not self.expiration_date:
            self.set_file_expiration_date()

        super().save(*args, **kwargs)

    save.alters_data = True