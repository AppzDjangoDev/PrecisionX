# Generated by Django 3.2.19 on 2023-11-27 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TradingOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=50, unique=True)),
                ('stock_name', models.CharField(choices=[('Nifty', 'Nifty'), ('BankNifty', 'BankNifty')], max_length=10)),
                ('entry_time', models.DateTimeField(blank=True, null=True)),
                ('entry_price', models.FloatField(blank=True, null=True)),
                ('stop_loss', models.FloatField(default=10)),
                ('strike_ltp', models.FloatField()),
                ('buy_target', models.FloatField()),
                ('option_type', models.CharField(choices=[('CALL', 'CALL'), ('PUT', 'PUT')], default=('CALL', 'CALL'), max_length=4)),
                ('strike_type', models.CharField(choices=[('STRIKE', 'Strike'), ('ITM', 'ITM'), ('OTM', 'OTM')], default=('STRIKE', 'Strike'), max_length=6)),
                ('trailing_stop_loss_interval', models.IntegerField(default=5)),
                ('trailing_stop_loss', models.FloatField(default=5)),
                ('exit_time', models.DateTimeField(blank=True, null=True)),
                ('exit_price', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
