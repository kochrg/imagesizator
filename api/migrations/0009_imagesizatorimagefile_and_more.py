# Generated by Django 4.0.4 on 2023-08-08 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_imagesizatorfile_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagesizatorImageFile',
            fields=[
                ('imagesizatorfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.imagesizatorfile')),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('proportion', models.CharField(max_length=10, null=True)),
            ],
            options={
                'verbose_name': 'Imagesizator image file',
                'verbose_name_plural': 'Imagesizator image files',
            },
            bases=('api.imagesizatorfile',),
        ),
        migrations.RemoveField(
            model_name='imagesizatortemporaryfile',
            name='imagesizatorfile_ptr',
        ),
        migrations.AddField(
            model_name='imagesizatorfile',
            name='expiration_date',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Expiration date (valid until)'),
        ),
        migrations.AddField(
            model_name='imagesizatorfile',
            name='is_static',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='imagesizatorfile',
            name='prefix',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='imagesizatorfile',
            name='suffix',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.DeleteModel(
            name='ImagesizatorStaticFile',
        ),
        migrations.DeleteModel(
            name='ImagesizatorTemporaryFile',
        ),
    ]