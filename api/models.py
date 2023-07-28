import os

from datetime import timedelta
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


# -------------------------------------------------------------------
# ------------------------- CUSTOM MODELS ---------------------------
# -------------------------------------------------------------------
class Parameters(models.Model):
    created_at = models.DateTimeField(
        "Fecha de creación",
        null=True,
        editable=False
    )
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

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone_now()
        super().save(*args, **kwargs)

    save.alters_data = True

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
    created_at = models.DateTimeField(
        "Created date",
        null=True,
        editable=False
    )
    path = models.TextField(
        null=False,
        blank=False,
        help_text="File path",
    )
    bytes_string = models.TextField(
        default='',
        help_text="Image as a byte string",
    )
    is_protected = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    class Meta:
        verbose_name = "Imagesizator file"
        verbose_name_plural = "Imagesizator files"

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone_now()
        super().save(*args, **kwargs)

    save.alters_data = True

    def delete(self):
        try:
            os.remove(r"" + str(self.path))
            super(ImagesizatorFile, self).delete()
        except Exception as e:
            print(e)
    
    @staticmethod
    def get_final_image_width_and_height(o_width, o_height, to_width, to_height, keep_proportion='none'):
        """
        Return a tuple with the final width and height of the image.
        keep_proportion = 'landscape': resize to_height, width proportionally.
                        'portrait': resize to_width, height proportionally.
                        'none' (default): resize to_width and to_heigth no matter proportions.
        """
        final_width = to_width
        final_height = to_height

        if keep_proportion == 'portrait':
            final_height = int(to_width * o_height / o_width)
        elif keep_proportion == 'landscape':
            final_width = int(to_height * o_width / o_height)
        # else resize ommiting ratio

        return (int(final_width), int(final_height))


class ImagesizatorTemporaryFile(ImagesizatorFile):
    expiration_date = models.DateTimeField(
        "Expiration date (valid until)",
        null=False,
        blank=False,
        editable=False
    )

    class Meta:
        verbose_name = "Temporary file"
        verbose_name_plural = "Temporary files"

    def __str__(self):
        return self.path

    def save(self, seconds=86400, *args, **kwargs):
        self.created_at = timezone_now()
        seconds = int(seconds)
        self.expiration_date = self.created_at + timedelta(seconds=seconds)
        super().save(*args, **kwargs)

    save.alters_data = True

    def get_publish_file_path(self):
        if self.is_protected:
            path = settings.PROTECTED_FOLDER + "/temp"
        else:
            path = settings.PUBLIC_FOLDER + "/temp"
        return path

    def get_named_temporary_file(self, prefix, suffix, publish=False):
        if publish:
            # Return file public url
            publish_path = os.getcwd() + self.get_publish_file_path()

            temporary_file = NamedTemporaryFile(
                "r+b",
                prefix=prefix,
                suffix=suffix,
                dir=publish_path,
                delete=False
            )

            # chmod 770 (Grant rwx access to www-data.www-data 'user and group')
            os.chmod(temporary_file.name, S_IRWXU + S_IRWXG)
            return temporary_file
        else:
            temporary_file = NamedTemporaryFile("r+b", prefix=prefix, suffix=suffix)

            return temporary_file

    @staticmethod
    def get_file_expiration_date(expiration=60*60*24):
        # expiration = 60*60*24. Default: 24hs.
        try:
            if expiration != 60*60*24:
                # custom expiration for this file
                return expiration
            else:
                user_default = int(Parameters.get_parameter_value('default_expiration_time'))  # seconds
                if user_default:
                    expiration = user_default
        except Exception as e:
            pass

        return expiration

class ImagesizatorStaticFile(ImagesizatorFile):

    class Meta:
        verbose_name = "Static file"
        verbose_name_plural = "Static files"

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    save.alters_data = True

    def get_publish_file_path(self):
        if self.is_protected:
            path = settings.PROTECTED_FOLDER + "/static"
        else:
            path = settings.PUBLIC_FOLDER + "/static"
        return path