# Generated by Django 4.2.16 on 2024-12-01 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0003_business_transaction_reward_userbusinesspoints'),
    ]

    operations = [
        migrations.AddField(
            model_name='reward',
            name='code',
            field=models.CharField(default=0, max_length=15, unique=True),
            preserve_default=False,
        ),
    ]
