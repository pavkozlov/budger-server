from django.contrib.auth.models import User
from django.db import models
# from budger.directory.models.kso import KsoEmployee
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # employee = models.ForeignKey(KsoEmployee, null=True, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30, null=True)
    position = models.CharField(max_length=100)

    read_only_fields = (user,)

    def __str__(self):
        return '{} {} {} ({})'.format(
            self.last_name,
            self.first_name,
            self.second_name,
            self.user
        )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def create(self, validated_data):
        profile = Profile(
            last_name=validated_data.get('last_name', ''),
            first_name=validated_data.get('first_name', ''),
            second_name=validated_data.get('second_name', ''),
            position=validated_data.get('position', ''),
        )
        profile.save()
        return profile

    def update(self, profile, validated_data):
        profile.last_name = validated_data.get('last_name', profile.last_name)
        profile.first_name = validated_data.get('first_name', profile.first_name)
        profile.second_name = validated_data.get('second_name', profile.second_name)
        profile.position = validated_data.get('position', profile.position)
        return profile
