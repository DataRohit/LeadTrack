# Generated by Django 4.2.17 on 2024-12-13 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tokenrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenrecord',
            name='token_type',
            field=models.CharField(choices=[('activation', 'Activation'), ('reset_password', 'Reset Password')], default='activation', max_length=24),
        ),
    ]