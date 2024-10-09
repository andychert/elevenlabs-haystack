from unittest.mock import patch
import pytest

def text_to_speech_mock(*args, **kwargs):
    """
    Mock the elevenlabs_s3.text_to_speech function.
    Returns a fixed response.
    """
    return {
        "file_path": "/path/to/audio.mp3",
        "s3_file_name": "audio.mp3",
        "s3_bucket_name": "test-bucket",
        "s3_presigned_url": "https://s3.amazonaws.com/test-bucket/audio.mp3?signature"
    }

@pytest.fixture
def mock_text_to_speech():
    """
    Fixture to mock the elevenlabs_s3.text_to_speech function.
    """
    with patch('elevenlabs_haystack.component.elevenlabs_s3.text_to_speech', side_effect=text_to_speech_mock) as mock_method:
        yield mock_method
