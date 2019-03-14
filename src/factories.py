import factory
import json
import uuid

import models


class AddressFactory(factory.DictFactory):
    """
    Use with factory.Dict to make JSON strings.

    """
    street = factory.Faker('street_name')
    city = factory.Faker('city')
    state = factory.Faker('state')
    country = factory.Faker('country')

    @classmethod
    def _generate(cls, create, attrs):
        obj = super()._generate(create, attrs)
        return json.dumps(obj)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: str(n))
    guid = factory.Sequence(lambda n: uuid.uuid4())
    name = factory.Faker('name')
    address = factory.Dict({'country': 'United States'}, dict_factory=AddressFactory)

    class Meta:
        model = models.UserModel
