# Generated by Django 3.2 on 2022-04-09 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_no', models.IntegerField()),
                ('chapter_name', models.CharField(max_length=100)),
                ('book_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_data.book')),
            ],
            options={
                'verbose_name': 'Chapter',
                'verbose_name_plural': 'Chapters',
            },
        ),
    ]
