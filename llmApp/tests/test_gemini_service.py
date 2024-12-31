import pytest
import responses
from llmApp.services.gemini_service import GeminiService
from llmApp.tests.factories import HotelFactory  # Changed to absolute import
import os

@pytest.fixture
def gemini_service():
    # Ensure the API key is set for tests
    os.environ['GEMINI_API_KEY'] = 'test-api-key'
    return GeminiService()

@pytest.fixture
def mock_gemini_response():
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "Sample response text"
                        }
                    ]
                }
            }
        ]
    }

@pytest.mark.django_db
class TestGeminiService:
    @responses.activate
    def test_rewrite_property_title(self, gemini_service, mock_gemini_response):
        # Arrange
        hotel = HotelFactory()
        responses.add(
            responses.POST,
            f"{gemini_service.base_url}/{gemini_service.model}:generateContent",
            json=mock_gemini_response,
            status=200
        )

        # Act
        result = gemini_service.rewrite_property_title(hotel)

        # Assert
        assert result == "Sample response text"
        assert len(responses.calls) == 1

    @responses.activate
    def test_generate_property_description(self, gemini_service, mock_gemini_response):
        # Arrange
        property_data = {
            'property_title': 'Test Hotel',
            'city_name': 'Test City',
            'room_type': 'Standard',
            'rating': '4.5',
            'price': '100'
        }
        responses.add(
            responses.POST,
            f"{gemini_service.base_url}/{gemini_service.model}:generateContent",
            json=mock_gemini_response,
            status=200
        )

        # Act
        result = gemini_service.generate_property_description(property_data)

        # Assert
        assert result == "Sample response text"
        assert len(responses.calls) == 1

    @responses.activate
    def test_generate_property_summary(self, gemini_service, mock_gemini_response):
        # Arrange
        property_data = {
            'property_title': 'Test Hotel',
            'city_name': 'Test City',
            'price': '100',
            'rating': '4.5',
            'description': 'Test description'
        }
        responses.add(
            responses.POST,
            f"{gemini_service.base_url}/{gemini_service.model}:generateContent",
            json=mock_gemini_response,
            status=200
        )

        # Act
        result = gemini_service.generate_property_summary(property_data)

        # Assert
        assert result == "Sample response text"
        assert len(responses.calls) == 1

    @responses.activate
    def test_generate_property_review(self, gemini_service):
        # Arrange
        property_data = {
            'property_title': 'Test Hotel',
            'city_name': 'Test City',
            'price': '100',
            'rating': '4.5'
        }
        mock_review_response = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "RATING: 4.5\nREVIEW: This is a test review"
                            }
                        ]
                    }
                }
            ]
        }
        responses.add(
            responses.POST,
            f"{gemini_service.base_url}/{gemini_service.model}:generateContent",
            json=mock_review_response,
            status=200
        )

        # Act
        rating, review = gemini_service.generate_property_review(property_data)

        # Assert
        assert rating == 4.5
        assert review == "This is a test review"
        assert len(responses.calls) == 1

    @responses.activate
    def test_api_error_handling(self, gemini_service):
        # Arrange
        responses.add(
            responses.POST,
            f"{gemini_service.base_url}/{gemini_service.model}:generateContent",
            status=500
        )

        # Act
        result = gemini_service._make_request("test prompt")

        # Assert
        assert result is None
        assert len(responses.calls) == 1

    def test_invalid_response_handling(self, gemini_service):
        # Arrange
        property_data = {
            'property_title': 'Test Hotel',
            'city_name': 'Test City',
            'price': '100',
            'rating': '4.5'
        }
        mock_invalid_response = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "Invalid format response"
                            }
                        ]
                    }
                }
            ]
        }
        responses.add(
            responses.POST,
            f"{gemini_service.base_url}/{gemini_service.model}:generateContent",
            json=mock_invalid_response,
            status=200
        )

        # Act
        rating, review = gemini_service.generate_property_review(property_data)

        # Assert
        assert rating is None
        assert review is None