# Generated by Django 4.1.2 on 2023-02-09 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan_approval', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='applicant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loan_approval.applicant'),
        ),
    ]
