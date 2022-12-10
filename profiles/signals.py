from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Follow


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Follow)
def post_save_follow(sender, instance, created, **kwargs):
    if created:
        follower_ = instance.follower
        followee_ = instance.followee

        followee_.followers.add(follower_.user)
        follower_.following.add(followee_.user)

        followee_.save()
        follower_.save()
