# Generated by Django 2.2 on 2021-02-26 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210226_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marca',
            name='modo',
            field=models.CharField(choices=[(1, 'Regular'), (2, 'Guardia')], default=1, max_length=1),
        ),
    ]
