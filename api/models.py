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

    @property
    def url(self):
        file_url = Parameters.get_parameter_value('imagesizator_domain')
        if file_url[:-1] != "/":
            file_url += "/"
        file_url += self.path
        return file_url

    def save(self, decoded_file, suffix, publish_path, *args, **kwargs):
        any_type_file = self.get_named_temporary_file(
            suffix,
            publish_path,
            'file_' + suffix.replace(".", "") + "_",
        )
        any_type_file.write(decoded_file)
        self.path = str(any_type_file.name)
        any_type_file.close()
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

    def get_named_temporary_file(self, suffix, publish_path=None, prefix='file_'):
        if publish_path:
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

    def save(self, decoded_file, suffix, seconds=86400, *args, **kwargs):
        seconds = int(seconds)
        self.expiration_date = self.created_at + timedelta(seconds=seconds)
        super().save(
            decoded_file=decoded_file,
            suffix=suffix,
            publish_path=self.publish_path,
            *args,
            **kwargs
        )

    save.alters_data = True

    @property
    def publish_path(self):
        path = os.getcwd()
        if self.is_protected:
            path += settings.PROTECTED_FOLDER + "/temp"
        else:
            path += settings.PUBLIC_FOLDER + "/temp"
        return path
    
    @property
    def is_temporal(self):
        return True
    
    @property
    def is_static(self):
        return False

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

    def save(self, decoded_file, suffix, *args, **kwargs):
        super().save(
            decoded_file=decoded_file,
            suffix=suffix,
            publish_path=self.publish_path,
            *args,
            **kwargs
        )

    save.alters_data = True

    @property
    def is_temporal(self):
        return False
    
    @property
    def is_static(self):
        return True

    @property
    def publish_path(self):
        path = os.getcwd()
        if self.is_protected:
            path = settings.PROTECTED_FOLDER + "/static"
        else:
            path = settings.PUBLIC_FOLDER + "/static"
        return path