# Generated by Django 4.0.4 on 2022-07-11 19:50

from django.utils.timezone import now as timezone_now
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_imagesizatortemporaryfile_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesizatorfile',
            name='bytes_string',
            field=models.TextField(default='', help_text='Image as a byte string'),
        ),
        migrations.AlterField(
            model_name='imagesizatortemporaryfile',
            name='expiration_date',
            field=models.DateTimeField(default=timezone_now(), editable=False, verbose_name='Expiration date (valid until)'),
            preserve_default=False,
        ),
    ]
