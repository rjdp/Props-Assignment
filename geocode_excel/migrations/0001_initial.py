# Generated by Django 2.1 on 2018-08-30 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=300)),
                ('lat', models.DecimalField(decimal_places=8, max_digits=11)),
                ('lng', models.DecimalField(decimal_places=8, max_digits=11)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('imported_xl', models.FileField(upload_to='imported_xls/')),
            ],
        ),
    ]