# Generated by Django 4.2.16 on 2024-12-01 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0004_reward_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBusinessRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relations', to='adminPanel.business')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_relations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]