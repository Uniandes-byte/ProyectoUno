# Generated by Django 4.2 on 2023-04-30 00:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('modelo', models.CharField(choices=[('NB', 'MultinomialNB'), ('LR', 'LogisticRegression'), ('NN', 'NeuralNetwork')], max_length=20, verbose_name='Modelo')),
                ('file', models.FileField(upload_to='files', verbose_name='file')),
            ],
        ),
    ]
