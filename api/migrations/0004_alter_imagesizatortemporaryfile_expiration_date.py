# Generated by Django 4.0.4 on 2022-07-11 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_imagesizatortemporaryfile_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesizatortemporaryfile',
            name='expiration_date',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Expiration date (valid until)'),
        ),
    ]
