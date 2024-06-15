import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils.timezone import make_aware
from faker import Faker

from visits.models import PageVisit
import factory
from tqdm import tqdm

faker = Faker("en_US")


def username():
    return faker.profile()["username"]


class UserFactory(factory.django.DjangoModelFactory):
    profile = factory.Faker("profile")
    username = factory.LazyAttribute(lambda x: x.profile["username"])
    email = factory.LazyAttribute(lambda x: x.profile["mail"])
    first_name = factory.LazyAttribute(lambda x: x.profile["name"].split(" ", 1)[0])
    last_name = factory.LazyAttribute(lambda x: x.profile["name"].split(" ", 1)[1])

    is_staff = False
    is_superuser = False

    class Meta:
        model = User
        exclude = ["profile"]


SECTIONS = ["index", "dashboard", "settings"]


def section():
    return random.choice(SECTIONS)


def visit_time():
    return make_aware(faker.date_time_this_month())


class PageVisitFactory(factory.django.DjangoModelFactory):
    section = factory.LazyFunction(section)
    visit_time = factory.LazyFunction(visit_time)

    class Meta:
        model = PageVisit


class Command(BaseCommand):
    def handle(self, *args, **options):
        PageVisit.objects.all().delete()
        User.objects.exclude(is_staff=True).delete()

        users = UserFactory.create_batch(100)

        for user in tqdm(users):
            PageVisit.objects.bulk_create(
                PageVisitFactory.build_batch(random.randint(1, 1_000), user=user)
            )
