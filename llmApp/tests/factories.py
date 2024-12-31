import factory
from factory.django import DjangoModelFactory
from llmApp.models import Hotel, PropertyReview, PropertySummary


class HotelFactory(DjangoModelFactory):
    class Meta:
        model = Hotel

    city_name = factory.Sequence(lambda n: f'City {n}')
    property_title = factory.Sequence(lambda n: f'Hotel {n}')
    hotel_id = factory.Sequence(lambda n: f'HOTEL{n}')
    price = factory.Faker('pyfloat', min_value=50, max_value=500)
    rating = factory.Faker('pyfloat', min_value=1, max_value=5)
    address = factory.Faker('address')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
    room_type = factory.Iterator(['Standard', 'Deluxe', 'Suite'])
    image = factory.Faker('url')
    local_image_path = factory.Faker('file_path')
    description = factory.Faker('text')

class PropertyReviewFactory(DjangoModelFactory):
    class Meta:
        model = PropertyReview

    property = factory.SubFactory(HotelFactory)
    rating = factory.Faker('pyfloat', min_value=1, max_value=5)
    review = factory.Faker('text')

class PropertySummaryFactory(DjangoModelFactory):
    class Meta:
        model = PropertySummary

    property = factory.SubFactory(HotelFactory)
    summary = factory.Faker('text')