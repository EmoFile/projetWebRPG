# Generated by Django 3.0.3 on 2020-02-14 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enemy',
            name='damage',
            field=models.PositiveIntegerField(default=4),
        ),
        migrations.AddField(
            model_name='enemy',
            name='diceNumber',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='weapon',
            name='damage',
            field=models.PositiveIntegerField(default=4),
        ),
        migrations.AddField(
            model_name='weapon',
            name='diceNumber',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='character',
            name='hpMax',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='chest',
            name='name',
            field=models.CharField(default='New Item', max_length=250),
        ),
        migrations.AlterField(
            model_name='consumable',
            name='name',
            field=models.CharField(default='New Item', max_length=250),
        ),
        migrations.AlterField(
            model_name='head',
            name='name',
            field=models.CharField(default='New Item', max_length=250),
        ),
        migrations.AlterField(
            model_name='leg',
            name='name',
            field=models.CharField(default='New Item', max_length=250),
        ),
        migrations.AlterField(
            model_name='weapon',
            name='name',
            field=models.CharField(default='New Item', max_length=250),
        ),
    ]
