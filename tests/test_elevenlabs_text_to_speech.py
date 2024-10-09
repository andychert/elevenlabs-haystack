import os
from unittest.mock import patch
import pytest
from haystack.utils import Secret

from elevenlabs_haystack import ElevenLabsTextToSpeech

class TestElevenLabsTextToSpeech:
    """Test cases for the ElevenLabsTextToSpeech class."""

    def test_init_default(self, monkeypatch):
        """Default initialization of the ElevenLabsTextToSpeech class."""
        monkeypatch.setenv("ELEVENLABS_API_KEY", "test-api-key")
        component = ElevenLabsTextToSpeech()
        assert component.elevenlabs_api_key.resolve_value() == "test-api-key"
        assert component.aws_access_key_id.resolve_value() is None
        assert component.aws_secret_access_key.resolve_value() is None
        assert component.aws_region_name is None
        assert component.aws_s3_bucket_name is None
        assert component.output_folder is None
        assert component.voice_id is None
        assert component.model_id is None
        assert component.voice_settings is None

    def test_init_with_parameters(self):
        component = ElevenLabsTextToSpeech(
            elevenlabs_api_key=Secret.from_token("test-api-key"),
            aws_access_key_id=Secret.from_token("aws-key"),
            aws_secret_access_key=Secret.from_token("aws-secret"),
            aws_region_name="us-west-1",
            aws_s3_bucket_name="test-bucket",
            output_folder="/tmp/output",
            voice_id="test-voice-id",
            model_id="test-model-id",
            voice_settings={"stability": 0.5},
            some_other_param="value",  # kwargs
        )
        assert component.elevenlabs_api_key.resolve_value() == "test-api-key"
        assert component.aws_access_key_id.resolve_value() == "aws-key"
        assert component.aws_secret_access_key.resolve_value() == "aws-secret"
        assert component.aws_region_name == "us-west-1"
        assert component.aws_s3_bucket_name == "test-bucket"
        assert component.output_folder == "/tmp/output"
        assert component.voice_id == "test-voice-id"
        assert component.model_id == "test-model-id"
        assert component.voice_settings == {"stability": 0.5}
        assert component.kwargs == {"some_other_param": "value"}

    def test_to_dict_default(self, monkeypatch):
        monkeypatch.setenv("ELEVENLABS_API_KEY", "test-api-key")
        component = ElevenLabsTextToSpeech()
        data = component.to_dict()
        assert data == {
            "type": "elevenlabs_haystack.component.ElevenLabsTextToSpeech",
            "init_parameters": {
                "elevenlabs_api_key": {
                    "env_vars": ["ELEVENLABS_API_KEY"],
                    "strict": True,
                    "type": "env_var",
                },
                "aws_access_key_id": {
                    "env_vars": ["AWS_ACCESS_KEY_ID"],
                    "strict": False,
                    "type": "env_var",
                },
                "aws_secret_access_key": {
                    "env_vars": ["AWS_SECRET_ACCESS_KEY"],
                    "strict": False,
                    "type": "env_var",
                },
                "aws_region_name": None,
                "aws_s3_bucket_name": None,
                "output_folder": None,
                "voice_id": None,
                "model_id": None,
                "voice_settings": None,
                # Remove 'kwargs': {} from expected data
            },
        }


    def test_to_dict_with_parameters(self, monkeypatch):
        monkeypatch.setenv("ELEVENLABS_API_KEY", "test-api-key")
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "aws-key")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "aws-secret")
        component = ElevenLabsTextToSpeech(
            elevenlabs_api_key=Secret.from_env_var("ELEVENLABS_API_KEY"),
            aws_access_key_id=Secret.from_env_var("AWS_ACCESS_KEY_ID", strict=True),
            aws_secret_access_key=Secret.from_env_var("AWS_SECRET_ACCESS_KEY", strict=True),
            aws_region_name="us-west-1",
            aws_s3_bucket_name="test-bucket",
            output_folder="/tmp/output",
            voice_id="test-voice-id",
            model_id="test-model-id",
            voice_settings={"stability": 0.5},
            some_other_param="value",  # Pass directly
        )
        data = component.to_dict()
        assert data == {
            "type": "elevenlabs_haystack.component.ElevenLabsTextToSpeech",
            "init_parameters": {
                "elevenlabs_api_key": {
                    "env_vars": ["ELEVENLABS_API_KEY"],
                    "strict": True,
                    "type": "env_var",
                },
                "aws_access_key_id": {
                    "env_vars": ["AWS_ACCESS_KEY_ID"],
                    "strict": True,
                    "type": "env_var",
                },
                "aws_secret_access_key": {
                    "env_vars": ["AWS_SECRET_ACCESS_KEY"],
                    "strict": True,
                    "type": "env_var",
                },
                "aws_region_name": "us-west-1",
                "aws_s3_bucket_name": "test-bucket",
                "output_folder": "/tmp/output",
                "voice_id": "test-voice-id",
                "model_id": "test-model-id",
                "voice_settings": {"stability": 0.5},
                "some_other_param": "value",  # Adjust expected data
            },
        }


    def test_from_dict(self, monkeypatch):
        monkeypatch.setenv("ELEVENLABS_API_KEY", "test-api-key")
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "aws-key")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "aws-secret")
        data = {
            "type": "elevenlabs_haystack.component.ElevenLabsTextToSpeech",
            "init_parameters": {
                "elevenlabs_api_key": {
                    "env_vars": ["ELEVENLABS_API_KEY"],
                    "strict": True,
                    "type": "env_var",
                },
                "aws_access_key_id": {
                    "env_vars": ["AWS_ACCESS_KEY_ID"],
                    "strict": True,
                    "type": "env_var",
                },
                "aws_secret_access_key": {
                    "env_vars": ["AWS_SECRET_ACCESS_KEY"],
                    "strict": True,
                    "type": "env_var",
                },
                "aws_region_name": "us-west-1",
                "aws_s3_bucket_name": "test-bucket",
                "output_folder": "/tmp/output",
                "voice_id": "test-voice-id",
                "model_id": "test-model-id",
                "voice_settings": {"stability": 0.5},
                "some_other_param": "value",  # Include directly
            },
        }
        component = ElevenLabsTextToSpeech.from_dict(data)
        assert component.elevenlabs_api_key.resolve_value() == "test-api-key"
        assert component.aws_access_key_id.resolve_value() == "aws-key"
        assert component.aws_secret_access_key.resolve_value() == "aws-secret"
        assert component.aws_region_name == "us-west-1"
        assert component.aws_s3_bucket_name == "test-bucket"
        assert component.output_folder == "/tmp/output"
        assert component.voice_id == "test-voice-id"
        assert component.model_id == "test-model-id"
        assert component.voice_settings == {"stability": 0.5}
        assert component.kwargs == {"some_other_param": "value"}


    def test_from_dict_fail_wo_env_var(self, monkeypatch):
        monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
        data = {
            "type": "elevenlabs_haystack.component.ElevenLabsTextToSpeech",
            "init_parameters": {
                "elevenlabs_api_key": {
                    "env_vars": ["ELEVENLABS_API_KEY"],
                    "strict": True,
                    "type": "env_var",
                },
                # other parameters...
            },
        }
        component = ElevenLabsTextToSpeech.from_dict(data)
        with pytest.raises(ValueError, match="None of the .* environment variables are set"):
            component.elevenlabs_api_key.resolve_value()


    def test_run(self, mock_text_to_speech):
        """Test the run method of the ElevenLabsTextToSpeech class."""
        component = ElevenLabsTextToSpeech(
            elevenlabs_api_key=Secret.from_token("test-api-key"),
            aws_access_key_id=Secret.from_token("aws-key"),
            aws_secret_access_key=Secret.from_token("aws-secret"),
            aws_region_name="us-west-1",
            aws_s3_bucket_name="test-bucket",
            output_folder="/tmp/output",
            voice_id="test-voice-id",
            model_id="test-model-id",
            voice_settings={"stability": 0.5},
            some_other_param="value",  # Assuming kwargs
        )
        text = "Hello, world!"
        response = component.run(text)
        # Check that the mock_text_to_speech was called with the correct parameters
        expected_params = {
            "text": text,
            "output_folder": "/tmp/output",
            "elevenlabs_api_key": "test-api-key",
            "aws_s3_bucket_name": "test-bucket",
            "aws_access_key_id": "aws-key",
            "aws_secret_access_key": "aws-secret",
            "aws_region_name": "us-west-1",
            "voice_id": "test-voice-id",
            "model_id": "test-model-id",
            "voice_settings": {"stability": 0.5},
            "some_other_param": "value",
        }
        mock_text_to_speech.assert_called_once_with(**expected_params)
        # Check the response
        assert response == {
            "file_path": "/path/to/audio.mp3",
            "s3_file_name": "audio.mp3",
            "s3_bucket_name": "test-bucket",
            "s3_presigned_url": "https://s3.amazonaws.com/test-bucket/audio.mp3?signature"
        }

    def test_run_error(self, mock_text_to_speech, monkeypatch):
        """Test that run method raises exception when text_to_speech fails."""
        mock_text_to_speech.side_effect = Exception("Test exception")
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "aws-key")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "aws-secret")
        component = ElevenLabsTextToSpeech(
            elevenlabs_api_key=Secret.from_token("test-api-key"),
            aws_access_key_id=Secret.from_env_var("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=Secret.from_env_var("AWS_SECRET_ACCESS_KEY"),
        )
        with pytest.raises(Exception, match="Test exception"):
            component.run("Hello, world!")

