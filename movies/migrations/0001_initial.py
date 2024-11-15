# Generated by Django 5.1.3 on 2024-11-08 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=100)),
                ('movie_link', models.URLField(blank=True, help_text='URL to load the movie from', null=True)),
                ('movie_file', models.FileField(blank=True, help_text='Upload the movie file here', null=True, upload_to='movies/')),
                ('description', models.TextField()),
                ('release_date', models.DateField()),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('poster_image', models.ImageField(blank=True, null=True, upload_to='posters/')),
                ('language', models.CharField(choices=[('EN', 'English'), ('TR', 'Turkish'), ('FR', 'French'), ('ES', 'Spanish'), ('DE', 'German'), ('RU', 'Russian'), ('JP', 'Japanese'), ('KR', 'Korean'), ('CN', 'Chinese'), ('IN', 'Hindi')], default='EN', max_length=2)),
                ('country', models.CharField(choices=[('US', 'United States'), ('TR', 'Turkey'), ('FR', 'France'), ('ES', 'Spain'), ('DE', 'Germany'), ('RU', 'Russia'), ('JP', 'Japan'), ('KR', 'South Korea'), ('CN', 'China'), ('IN', 'India')], default='US', max_length=2)),
                ('duration', models.PositiveIntegerField(default=120, help_text='Duration in minutes')),
                ('director', models.CharField(blank=True, max_length=100, null=True)),
                ('actors', models.TextField(blank=True, help_text='List of main actors', null=True)),
                ('trailer_url', models.URLField(blank=True, null=True)),
                ('imdb_id', models.CharField(blank=True, help_text='IMDb ID if available', max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
