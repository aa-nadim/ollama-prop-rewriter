import unittest
from unittest.mock import patch, MagicMock
from django.core.management import call_command
from django.test import TestCase
from llmApp.models import Hotel, PropertyReview, PropertySummary

class TestManagementCommands(TestCase):
    """
    Unit tests for management commands in the llmApp/management/commands directory.
    """

    def setUp(self):
        # Create a mock hotel instance that will be used across tests
        self.mock_hotel = MagicMock()
        self.mock_hotel.id = 1
        self.mock_hotel.property_title = "Test Hotel"
        self.mock_hotel.city_name = "Test City"
        self.mock_hotel.room_type = "Deluxe"
        self.mock_hotel.price = 100.00
        self.mock_hotel.rating = 4.5
        self.mock_hotel.description = "Test description"

        # Create the property data dictionary that will be used by the service
        self.property_data = {
            'property_title': 'Test Hotel',
            'city_name': 'Test City',
            'room_type': 'Deluxe',
            'price': '100.00',
            'rating': '4.5',
            'description': 'Test description'
        }

        # Mock the hotel's to_dict method
        self.mock_hotel.to_dict.return_value = self.property_data

    @patch('llmApp.management.commands.generate_descriptions.GeminiService')
    @patch('llmApp.models.Hotel.objects')
    def test_generate_descriptions(self, mock_hotel_objects, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.generate_property_description.return_value = "Generated description"

        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__iter__.return_value = [self.mock_hotel]
        mock_hotel_objects.filter.return_value = mock_queryset

        call_command('generate_descriptions', batch_size=1)

        mock_hotel_objects.filter.assert_called_once_with(description__isnull=True)
        mock_service.generate_property_description.assert_called_once_with(self.property_data)
        self.mock_hotel.save.assert_called_once()

    @patch('llmApp.management.commands.generate_reviews.GeminiService')
    @patch('llmApp.models.Hotel.objects')
    @patch('llmApp.models.PropertyReview.objects')
    def test_generate_reviews(self, mock_review_objects, mock_hotel_objects, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.generate_property_review.return_value = (4.5, "Test review")

        mock_hotel_queryset = MagicMock()
        mock_hotel_queryset.count.return_value = 1
        mock_hotel_queryset.__iter__.return_value = [self.mock_hotel]
        mock_hotel_objects.exclude.return_value = mock_hotel_queryset

        mock_review_queryset = MagicMock()
        mock_review_queryset.exists.return_value = False
        mock_review_objects.filter.return_value = mock_review_queryset

        call_command('generate_reviews', batch_size=1)

        mock_service.generate_property_review.assert_called_once_with(self.property_data)
        mock_review_objects.create.assert_called_once_with(
            property=self.mock_hotel,
            rating=4.5,
            review="Test review"
        )

    @patch('llmApp.management.commands.generate_summaries.GeminiService')
    @patch('llmApp.models.Hotel.objects')
    @patch('llmApp.models.PropertySummary.objects')
    def test_generate_summaries(self, mock_summary_objects, mock_hotel_objects, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.generate_property_summary.return_value = "Test summary"

        mock_hotel_queryset = MagicMock()
        mock_hotel_queryset.count.return_value = 1
        mock_hotel_queryset.__iter__.return_value = [self.mock_hotel]
        mock_hotel_objects.filter.return_value = mock_hotel_queryset
        mock_hotel_queryset.exclude.return_value = mock_hotel_queryset

        mock_summary_queryset = MagicMock()
        mock_summary_queryset.exists.return_value = False
        mock_summary_objects.filter.return_value = mock_summary_queryset

        call_command('generate_summaries', batch_size=1)

        mock_service.generate_property_summary.assert_called_once_with(self.property_data)
        mock_summary_objects.create.assert_called_once_with(
            property=self.mock_hotel,
            summary="Test summary"
        )

    @patch('llmApp.management.commands.rewrite_titles.GeminiService')
    @patch('llmApp.models.Hotel.objects')
    def test_rewrite_titles(self, mock_hotel_objects, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.rewrite_property_title.return_value = "Updated Test Hotel"

        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__iter__.return_value = [self.mock_hotel]
        mock_hotel_objects.all.return_value = mock_queryset

        call_command('rewrite_titles', batch_size=1)

        mock_service.rewrite_property_title.assert_called_once_with(self.mock_hotel)
        self.mock_hotel.property_title = "Updated Test Hotel"
        self.mock_hotel.save.assert_called_once()

    def test_command_error_handling(self):
        with patch('llmApp.management.commands.generate_descriptions.GeminiService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.generate_property_description.side_effect = Exception("API Error")

            with patch('llmApp.models.Hotel.objects') as mock_hotel_objects:
                mock_queryset = MagicMock()
                mock_queryset.count.return_value = 1
                mock_queryset.__iter__.return_value = [self.mock_hotel]
                mock_hotel_objects.filter.return_value = mock_queryset

                try:
                    call_command('generate_descriptions', batch_size=1)
                except Exception as e:
                    self.fail(f"Command raised unexpected exception: {e}")

if __name__ == '__main__':
    unittest.main()
