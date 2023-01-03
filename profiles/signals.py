from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Follow
from library.models import Collection


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        Collection.objects.create(owner=profile, name='bookshelf')
        Collection.objects.create(owner=profile, name='wish_list')
        Collection.objects.create(owner=profile, name='favorites')


@receiver(post_save, sender=Follow)
def post_save_follow(sender, instance, created, **kwargs):
    if created:
        follower_ = instance.follower
        followee_ = instance.followee

        followee_.followers.add(follower_.user)
        follower_.following.add(followee_.user)

        followee_.save()
        follower_.save()


@receiver(pre_delete, sender=Follow)
def pre_delete_remove_from_followe(sender, instance, **kwargs):
    follower_ = instance.follower
    followee_ = instance.followee

    followee_.followers.remove(follower_.user)
    follower_.following.remove(followee_.user)

    followee_.save()
    follower_.save()
