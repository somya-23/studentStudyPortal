# Generated by Django 4.0.4 on 2022-04-20 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notes',
            options={'verbose_name': 'Notes', 'verbose_name_plural': 'Notes'},
        ),
        migrations.AlterField(
            model_name='notes',
            name='Title',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='HomeWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=500)),
                ('due', models.DateTimeField()),
                ('status', models.BooleanField(default=False, verbose_name='Mark as completed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]