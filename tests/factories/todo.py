import factory
import faker

fake = faker.Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    id = factory.LazyAttribute(
      lambda x: str(fake.random_int(
        min=1000000000000000000,
        max=999999999999999999999))
    )
    access_token = factory.LazyAttribute(
      lambda x: fake.sha256() + fake.sha256()
    )
    email = factory.LazyAttribute(lambda x: fake.email())
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())
    is_staff = factory.LazyAttribute(lambda x: fake.boolean())

    class Meta:
        model = 'todo.User'


class TodoFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(
      lambda x: ' '.join(fake.words(fake.random_int(1, 4)))
    )
    completed = factory.LazyAttribute(lambda x: fake.boolean())
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = 'todo.Todo'
