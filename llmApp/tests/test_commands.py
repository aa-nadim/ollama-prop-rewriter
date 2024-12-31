import pytest
from django.core.management import call_command
from io import StringIO
from llmApp.models import Hotel, PropertyReview, PropertySummary
from llmApp.tests.factories import HotelFactory  # Changed to absolute import
from unittest.mock import patch

@pytest.mark.django_db
class TestManagementCommands:
    @patch('llmApp.services.gemini_service.GeminiService.rewrite_property_title')
    def test_rewrite_titles_command(self, mock_rewrite):
        # Arrange
        hotels = [HotelFactory() for _ in range(3)]
        mock_rewrite.return_value = "New Title"
        out = StringIO()

        # Act
        call_command('rewrite_titles', batch_size=2, stdout=out)

        # Assert
        assert mock_rewrite.call_count == 3
        for hotel in Hotel.objects.all():
            assert hotel.property_title == "New Title"

    @patch('llmApp.services.gemini_service.GeminiService.generate_property_description')
    def test_generate_descriptions_command(self, mock_description):
        # Arrange
        hotels = [HotelFactory(description=None) for _ in range(3)]
        mock_description.return_value = "New Description"
        out = StringIO()

        # Act
        call_command('generate_descriptions', batch_size=2, stdout=out)

        # Assert
        assert mock_description.call_count == 3
        for hotel in Hotel.objects.all():
            assert hotel.description == "New Description"

    @patch('llmApp.services.gemini_service.GeminiService.generate_property_summary')
    def test_generate_summaries_command(self, mock_summary):
        # Arrange
        hotels = [HotelFactory(description="Test Description") for _ in range(3)]
        mock_summary.return_value = "New Summary"
        out = StringIO()

        # Act
        call_command('generate_summaries', batch_size=2, stdout=out)

        # Assert
        assert mock_summary.call_count == 3
        assert PropertySummary.objects.count() == 3

    @patch('llmApp.services.gemini_service.GeminiService.generate_property_review')
    def test_generate_reviews_command(self, mock_review):
        # Arrange
        hotels = [HotelFactory() for _ in range(3)]
        mock_review.return_value = (4.5, "New Review")
        out = StringIO()

        # Act
        call_command('generate_reviews', batch_size=2, stdout=out)

        # Assert
        assert mock_review.call_count == 3
        assert PropertyReview.objects.count() == 3
        for review in PropertyReview.objects.all():
            assert review.rating == 4.5
            assert review.review == "New Review"