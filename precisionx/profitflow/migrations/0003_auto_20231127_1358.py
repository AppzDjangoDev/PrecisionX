# Generated by Django 3.2.19 on 2023-11-27 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profitflow', '0002_alter_tradingorder_buy_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradingorder',
            name='buy_target',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='tradingorder',
            name='stock_name',
            field=models.CharField(choices=[('Nifty', 'Nifty'), ('BankNifty', 'BankNifty')], default=('BankNifty', 'BankNifty'), max_length=10),
        ),
        migrations.AlterField(
            model_name='tradingorder',
            name='stop_loss',
            field=models.FloatField(default=5),
        ),
    ]
