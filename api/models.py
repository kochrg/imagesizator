# from django.db import models
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.timezone import now as timezone_now
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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