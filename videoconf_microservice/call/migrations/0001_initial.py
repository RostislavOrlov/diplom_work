# Generated by Django 3.2.5 on 2024-05-10 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('duration', models.IntegerField(default=0)),
                ('team_id', models.IntegerField()),
                ('user_registrant_id', models.IntegerField()),
                ('user_registrant_username', models.CharField(max_length=1000)),
                ('user_registrant_email', models.CharField(max_length=1000)),
                ('is_launched', models.BooleanField(default=False)),
                ('start_date', models.DateField()),
                ('is_on_waiting_hall', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_planned', models.BooleanField(default=True)),
                ('entry_before_the_organizer_is_enabled', models.BooleanField(default=False)),
                ('off_participants_voice_after_entry', models.BooleanField(default=True)),
                ('is_on_waiting_hall', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingsUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('username', models.CharField(max_length=100)),
                ('user_img_ref', models.CharField(max_length=10000)),
                ('user_email', models.CharField(max_length=1000)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('is_attended_the_meeting', models.BooleanField(default=False)),
                ('breaking_count', models.IntegerField(default=0)),
                ('user_duration', models.IntegerField(default=0)),
                ('user_role', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=50, unique=True)),
                ('channel_name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomsUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('user_duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SessionRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('max_participant_count', models.IntegerField()),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='call.meeting')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingPoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anonymous', models.BooleanField(default=False)),
                ('poll_type', models.CharField(choices=[('poll', 'обычное голосование'), ('quiz', 'квиз')], default='poll', max_length=50)),
                ('question', models.CharField(max_length=1000)),
                ('answer_options', models.CharField(max_length=1000)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='call.meeting')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingInviteLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttl', models.IntegerField()),
                ('join_url', models.CharField(max_length=200)),
                ('meeting', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='call.meeting')),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='settings',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='call.meetingsettings'),
        ),
    ]
