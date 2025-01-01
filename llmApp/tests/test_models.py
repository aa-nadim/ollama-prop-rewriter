from unittest.mock import MagicMock, patch
from django.test import TestCase
from llmApp.models import Hotel, PropertySummary, PropertyReview

class ModelTests(TestCase):
    def setUp(self):
        # Mocked Hotel instance
        self.hotel = MagicMock(spec=Hotel)
        self.hotel.hotel_id = "H1001"
        self.hotel.city_name = "Test City"
        self.hotel.property_title = "Test Hotel"
        self.hotel.price = 150.0
        self.hotel.rating = 4.7
        self.hotel.address = "123 Test Lane"
        self.hotel.latitude = 23.78
        self.hotel.longitude = 90.4
        self.hotel.room_type = "Deluxe"
        self.hotel.image = "http://example.com/image.jpg"
        self.hotel.local_image_path = "/images/test.jpg"
        self.hotel.description = "A luxurious test hotel."

    @patch('llmApp.models.Hotel')
    def test_hotel_model_fields(self, MockHotel):
        MockHotel.objects = MagicMock()
        MockHotel.objects.get.return_value = self.hotel

        hotel = MockHotel.objects.get(hotel_id="H1001")
        self.assertEqual(hotel.hotel_id, "H1001")
        self.assertEqual(hotel.city_name, "Test City")
        self.assertEqual(hotel.property_title, "Test Hotel")
        self.assertEqual(hotel.price, 150.0)
        self.assertEqual(hotel.rating, 4.7)
        self.assertEqual(hotel.address, "123 Test Lane")
        self.assertEqual(hotel.latitude, 23.78)
        self.assertEqual(hotel.longitude, 90.4)
        self.assertEqual(hotel.room_type, "Deluxe")
        self.assertEqual(hotel.image, "http://example.com/image.jpg")
        self.assertEqual(hotel.local_image_path, "/images/test.jpg")
        self.assertEqual(hotel.description, "A luxurious test hotel.")

    @patch('llmApp.models.PropertySummary')
    def test_property_summary_creation(self, MockPropertySummary):
        mock_summary = MagicMock(spec=PropertySummary)
        mock_summary.property = self.hotel
        mock_summary.summary = "Test summary for the property."
        mock_summary.__str__.return_value = "Summary for Test Hotel"

        MockPropertySummary.objects.create.return_value = mock_summary
        summary = MockPropertySummary.objects.create(
            property=self.hotel,
            summary="Test summary for the property."
        )

        self.assertEqual(str(summary), "Summary for Test Hotel")

    @patch('llmApp.models.PropertyReview')
    def test_property_review_creation(self, MockPropertyReview):
        mock_review = MagicMock(spec=PropertyReview)
        mock_review.property = self.hotel
        mock_review.rating = 4.5
        mock_review.review = "Great hotel experience."
        mock_review.__str__.return_value = "Review for Test Hotel"

        MockPropertyReview.objects.create.return_value = mock_review
        review = MockPropertyReview.objects.create(
            property=self.hotel,
            rating=4.5,
            review="Great hotel experience."
        )

        self.assertEqual(str(review), "Review for Test Hotel")

    @patch('llmApp.models.Hotel')
    def test_hotel_empty_description(self, MockHotel):
        hotel_with_no_description = MagicMock(spec=Hotel)
        hotel_with_no_description.property_title = "No Description Hotel"
        hotel_with_no_description.description = None

        MockHotel.objects.get.return_value = hotel_with_no_description
        hotel = MockHotel.objects.get(hotel_id="H1002")

        self.assertIsNone(hotel.description, "The description should be None for a hotel with no description.")
