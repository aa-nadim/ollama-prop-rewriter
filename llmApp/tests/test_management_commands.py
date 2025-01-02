import unittest
from unittest.mock import patch, MagicMock
from django.core.management import call_command
from django.test import TestCase
from django.core.management.base import CommandError


class TestManagementCommands(TestCase):
    """
    Unit tests for management commands in the llmApp/management/commands directory.
    """
    def setUp(self):
        self.mock_hotel = MagicMock()
        self.mock_hotel.save = MagicMock()
        self.mock_hotel.id = 1
        self.mock_hotel.property_title = "Test Hotel"
        self.mock_hotel.city_name = "Test City"
        self.mock_hotel.room_type = "Deluxe"
        self.mock_hotel.price = 100.00
        self.mock_hotel.rating = 4.5
        self.mock_hotel.description = "Test description"

        self.property_data = {
            'property_title': 'Test Hotel',
            'city_name': 'Test City',
            'room_type': 'Deluxe',
            'price': '100.00',
            'rating': '4.5',
            'description': 'Test description',
        }

    @patch('llmApp.management.commands.generate_descriptions.Command.handle')
    def test_generate_descriptions_mocked(self, mock_handle):
        """
        Mock the generate_descriptions command to always succeed.
        """
        mock_handle.return_value = None  # Simulate successful execution
        call_command('generate_descriptions', batch_size=1)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_reviews.Command.handle')
    def test_generate_reviews_mocked(self, mock_handle):
        """
        Mock the generate_reviews command to always succeed.
        """
        mock_handle.return_value = None  # Simulate successful execution
        call_command('generate_reviews', batch_size=1)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_summaries.Command.handle')
    def test_generate_summaries_mocked(self, mock_handle):
        """
        Mock the generate_summaries command to always succeed.
        """
        mock_handle.return_value = None  # Simulate successful execution
        call_command('generate_summaries', batch_size=1)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.rewrite_titles.Command.handle')
    def test_rewrite_titles_mocked(self, mock_handle):
        """
        Mock the rewrite_titles command to always succeed.
        """
        mock_handle.return_value = None  # Simulate successful execution
        call_command('rewrite_titles', batch_size=1)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_descriptions.Command.handle')
    def test_generate_descriptions_invalid_arguments(self, mock_handle):
        """
        Test generate_descriptions command with invalid arguments.
        """
        mock_handle.side_effect = CommandError("Invalid argument")
        with self.assertRaises(CommandError):
            call_command('generate_descriptions', batch_size=-1)

        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_reviews.Command.handle')
    def test_generate_reviews_error_handling(self, mock_handle):
        """
        Test generate_reviews command when an error occurs.
        """
        mock_handle.side_effect = Exception("Unexpected error")
        with self.assertRaises(Exception):
            call_command('generate_reviews', batch_size=10)

        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_summaries.Command.handle')
    def test_generate_summaries_no_arguments(self, mock_handle):
        """
        Test generate_summaries command with no arguments.
        """
        mock_handle.return_value = None
        call_command('generate_summaries')  # Default arguments
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.rewrite_titles.Command.handle')
    def test_rewrite_titles_invalid_batch_size(self, mock_handle):
        """
        Test rewrite_titles command with invalid batch size.
        """
        mock_handle.side_effect = CommandError("Invalid batch size")
        with self.assertRaises(CommandError):
            call_command('rewrite_titles', batch_size=-100)

        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_descriptions.Command.handle')
    def test_generate_descriptions_large_batch_size(self, mock_handle):
        """
        Test generate_descriptions command with a large batch size.
        """
        mock_handle.return_value = None
        call_command('generate_descriptions', batch_size=1000)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_reviews.Command.handle')
    def test_generate_reviews_no_data(self, mock_handle):
        """
        Test generate_reviews command when there is no data to process.
        """
        mock_handle.side_effect = CommandError("No data found")
        with self.assertRaises(CommandError):
            call_command('generate_reviews')

        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_descriptions.Command.handle')
    def test_generate_descriptions_success(self, mock_handle):
        """
        Test successful execution of the generate_descriptions command.
        """
        mock_handle.return_value = None
        call_command('generate_descriptions', batch_size=1)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_descriptions.Command.handle')
    def test_generate_descriptions_failure(self, mock_handle):
        """
        Test failure case for the generate_descriptions command.
        """
        mock_handle.side_effect = Exception("Test error")
        with self.assertRaises(Exception) as context:
            call_command('generate_descriptions', batch_size=1)
        self.assertEqual(str(context.exception), "Test error")
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_reviews.Command.handle')
    def test_generate_reviews_success(self, mock_handle):
        """
        Test successful execution of the generate_reviews command.
        """
        mock_handle.return_value = None
        call_command('generate_reviews', batch_size=1)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_reviews.Command.handle')
    def test_generate_reviews_failure(self, mock_handle):
        """
        Test failure case for the generate_reviews command.
        """
        mock_handle.side_effect = Exception("Test error")
        with self.assertRaises(Exception) as context:
            call_command('generate_reviews', batch_size=1)
        self.assertEqual(str(context.exception), "Test error")
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_summaries.Command.handle')
    def test_generate_summaries_success(self, mock_handle):
        """
        Test successful execution of the generate_summaries command.
        """
        mock_handle.return_value = None
        call_command('generate_summaries', batch_size=1)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_summaries.Command.handle')
    def test_generate_summaries_failure(self, mock_handle):
        """
        Test failure case for the generate_summaries command.
        """
        mock_handle.side_effect = Exception("Test error")
        with self.assertRaises(Exception) as context:
            call_command('generate_summaries', batch_size=1)
        self.assertEqual(str(context.exception), "Test error")
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.rewrite_titles.Command.handle')
    def test_rewrite_titles_success(self, mock_handle):
        """
        Test successful execution of the rewrite_titles command.
        """
        mock_handle.return_value = None
        call_command('rewrite_titles', batch_size=1)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.rewrite_titles.Command.handle')
    def test_rewrite_titles_failure(self, mock_handle):
        """
        Test failure case for the rewrite_titles command.
        """
        mock_handle.side_effect = Exception("Test error")
        with self.assertRaises(Exception) as context:
            call_command('rewrite_titles', batch_size=1)
        self.assertEqual(str(context.exception), "Test error")
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_descriptions.Command.handle')
    def test_generate_descriptions_large_batch_size(self, mock_handle):
        mock_handle.return_value = None
        call_command('generate_descriptions', batch_size=1000)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_reviews.Command.handle')
    def test_generate_reviews_no_data(self, mock_handle):
        mock_handle.side_effect = CommandError("No data found")
        with self.assertRaises(CommandError):
            call_command('generate_reviews')
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.generate_summaries.Command.handle')
    def test_generate_summaries_large_batch_size(self, mock_handle):
        mock_handle.return_value = None
        call_command('generate_summaries', batch_size=1000)
        mock_handle.assert_called_once()

    @patch('llmApp.management.commands.rewrite_titles.Hotel.objects')
    @patch('llmApp.management.commands.rewrite_titles.RewriteService', create=True)
    def test_rewrite_titles(self, mock_service_class, mock_hotel_objects):
        mock_service = mock_service_class.return_value
        mock_service.rewrite_property_title.return_value = "Updated Title"

        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__iter__.return_value = [self.mock_hotel]
        mock_hotel_objects.all.return_value = mock_queryset

        call_command('rewrite_titles', batch_size=1)

        mock_hotel_objects.all.assert_called_once()
        mock_service.rewrite_property_title.assert_called_once_with(self.mock_hotel)
        self.mock_hotel.save.assert_called_once()

        
if __name__ == '__main__':
    unittest.main()
