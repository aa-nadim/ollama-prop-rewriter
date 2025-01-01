import unittest
from unittest.mock import patch, MagicMock
from llmApp.services.gemini_service import GeminiService

class TestGeminiService(unittest.TestCase):

    def setUp(self):
        self.service = GeminiService()
        self.mock_hotel = MagicMock()
        self.mock_hotel.property_title = "Cozy Downtown Hotel"
        self.mock_hotel.city_name = "New York"
        self.mock_hotel.room_type = "Suite"
        self.mock_hotel.rating = 4.5
        
        self.mock_property_data = {
            "property_title": "Beachfront Villa",
            "city_name": "Miami",
            "room_type": "Villa",
            "rating": 4.8,
            "price": 350,
            "description": "A beautiful villa by the beach with stunning ocean views."
        }

    @patch('llmApp.services.gemini_service.requests.post')
    def test_rewrite_property_title(self, mock_post):
        # Mock API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "Luxurious Downtown Hotel Suite in New York"}]}}
            ]
        }

        response = self.service.rewrite_property_title(self.mock_hotel)
        self.assertEqual(response, "Luxurious Downtown Hotel Suite in New York")
        self.assertTrue(mock_post.called)

    @patch('llmApp.services.gemini_service.requests.post')
    def test_generate_property_description(self, mock_post):
        # Mock API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "This beachfront villa in Miami offers stunning ocean views and luxurious amenities."}]}}
            ]
        }

        response = self.service.generate_property_description(self.mock_property_data)
        self.assertIn("beachfront villa in Miami", response)
        self.assertTrue(mock_post.called)

    @patch('llmApp.services.gemini_service.requests.post')
    def test_generate_property_summary(self, mock_post):
        # Mock API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "A luxurious villa in Miami priced at $350 with an excellent rating of 4.8/5."}]}}
            ]
        }

        response = self.service.generate_property_summary(self.mock_property_data)
        self.assertIn("luxurious villa in Miami", response)
        self.assertTrue(mock_post.called)

    @patch('llmApp.services.gemini_service.requests.post')
    def test_generate_property_review(self, mock_post):
        # Mock API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "RATING: 5\nREVIEW: Amazing property with top-notch amenities and breathtaking views."}]}}
            ]
        }

        rating, review = self.service.generate_property_review(self.mock_property_data)
        self.assertEqual(rating, 5)
        self.assertIn("Amazing property with top-notch amenities", review)
        self.assertTrue(mock_post.called)

    @patch('llmApp.services.gemini_service.requests.post')
    def test_error_handling_in_request(self, mock_post):
        # Simulate a failed request
        mock_post.side_effect = Exception("API request failed")
        
        response = self.service.rewrite_property_title(self.mock_hotel)
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()
