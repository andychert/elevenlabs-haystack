import pytest
from unittest.mock import patch
from haystack import component
from haystack.utils import Secret
from elevenlabs_haystack import ElevenLabsTextToSpeech


def test_welcome_text_generator():
    """Test the WelcomeTextGenerator component output."""

    @component
    class WelcomeTextGenerator:
        @component.output_types(welcome_text=str, note=str)
        def run(self, name: str):
            welcome_text = f'Hello {name}, welcome to Haystack!'.upper()
            return {
                "welcome_text": welcome_text,
                "note": "welcome message is ready"
            }

    # Create an instance of WelcomeTextGenerator
    welcome_generator = WelcomeTextGenerator()

    # Run the component
    result = welcome_generator.run(name="Bilge")

    # Expected result
    expected_result = {
        "welcome_text": "HELLO BILGE, WELCOME TO HAYSTACK!",
        "note": "welcome message is ready"
    }

    # Assert the result matches the expected output
    assert result == expected_result


@pytest.fixture
def mock_text_to_speech_fixture():
    """Mock fixture for the ElevenLabs text_to_speech function."""
    with patch('elevenlabs_haystack.component.elevenlabs_s3.text_to_speech', return_value={
        "id": "test-id",
        "file_name": "audio_files/test_file.mp3",
        "s3_file_name": "s3/test_file.mp3",
        "s3_bucket_name": "test-bucket",
        "s3_presigned_url": "https://test-bucket.s3.amazonaws.com/s3/test_file.mp3"
    }) as mock_method:
        yield mock_method


def test_elevenlabs_text_to_speech(mock_text_to_speech_fixture):
    """Test the ElevenLabsTextToSpeech component with mock input."""
    
    # Create an instance of ElevenLabsTextToSpeech
    tts_component = ElevenLabsTextToSpeech(
        elevenlabs_api_key=Secret.from_token("test-api-key"),
        output_folder="audio_files",
        voice_id="test-voice-id",
        aws_s3_bucket_name="test-bucket",
        aws_s3_output_folder="s3_files",
        aws_access_key_id=Secret.from_token("aws-key"),
        aws_secret_access_key=Secret.from_token("aws-secret"),
        aws_region_name="us-west-1",
        voice_settings={
            "stability": 0.75,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True,
        },
    )

    # Run the component
    result = tts_component.run(text="HELLO BILGE, WELCOME TO HAYSTACK!")

    # Expected result
    expected_result = {
        "id": "test-id",
        "file_name": "audio_files/test_file.mp3",
        "s3_file_name": "s3/test_file.mp3",
        "s3_bucket_name": "test-bucket",
        "s3_presigned_url": "https://test-bucket.s3.amazonaws.com/s3/test_file.mp3"
    }

    # Assert the result matches the expected output
    assert result == expected_result
