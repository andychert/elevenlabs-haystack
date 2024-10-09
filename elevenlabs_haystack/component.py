import os
import logging
from typing import Optional, Any, Dict
from haystack import component, default_from_dict, default_to_dict
from haystack.utils import Secret, deserialize_secrets_inplace

import elevenlabs_s3

logger = logging.getLogger(__name__)

@component
class ElevenLabsTextToSpeech:
    """
    A Haystack component that converts text to speech using the elevenlabs_s3's
    text_to_speech function, and optionally uploads the audio to AWS S3.
    """

    def __init__(
        self,
        elevenlabs_api_key: Optional[Secret] = None,
        aws_access_key_id: Optional[Secret] = None,
        aws_secret_access_key: Optional[Secret] = None,
        aws_region_name: Optional[str] = None,
        aws_s3_bucket_name: Optional[str] = None,
        output_folder: Optional[str] = None,
        voice_id: Optional[str] = None,
        model_id: Optional[str] = None,
        voice_settings: Optional[Any] = None,
        **kwargs,
    ):
        """
        Initialize the ElevenLabsTextToSpeech component.
        """
        self.elevenlabs_api_key = elevenlabs_api_key or Secret.from_env_var("ELEVENLABS_API_KEY")
        self.aws_access_key_id = aws_access_key_id or Secret.from_env_var("AWS_ACCESS_KEY_ID", strict=False)
        self.aws_secret_access_key = aws_secret_access_key or Secret.from_env_var("AWS_SECRET_ACCESS_KEY", strict=False)
        self.aws_region_name = aws_region_name or os.getenv("AWS_REGION_NAME")
        self.aws_s3_bucket_name = aws_s3_bucket_name or os.getenv("AWS_S3_BUCKET_NAME")
        self.output_folder = output_folder
        self.voice_id = voice_id
        self.model_id = model_id
        self.voice_settings = voice_settings
        self.kwargs = kwargs

    @component.output_types(
        file_path=Optional[str],
        s3_file_name=Optional[str],
        s3_bucket_name=Optional[str],
        s3_presigned_url=Optional[str],
    )
    def run(self, text: str):
        """
        Convert text to speech and optionally upload to AWS S3.
        """
        result = {}

        # Prepare parameters for text_to_speech function
        params = {
            "text": text,
            "output_folder": self.output_folder,
            "elevenlabs_api_key": self.elevenlabs_api_key.resolve_value() or None,
            "aws_s3_bucket_name": self.aws_s3_bucket_name,
            "aws_access_key_id": self.aws_access_key_id.resolve_value() or None,
            "aws_secret_access_key": self.aws_secret_access_key.resolve_value() or None,
            "aws_region_name": self.aws_region_name,
            "voice_id": self.voice_id,
            "model_id": self.model_id,
            "voice_settings": self.voice_settings,
            **self.kwargs,
        }

        # Call the text_to_speech function from elevenlabs_s3
        try:
            result = elevenlabs_s3.text_to_speech(**params)
            logger.info("Text-to-speech conversion successful.")
        except Exception as e:
            logger.error(f"Error during text-to-speech conversion: {e}")
            raise

        return result

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the component to a dictionary."""
        init_parameters = {
            "elevenlabs_api_key": self.elevenlabs_api_key.to_dict() if self.elevenlabs_api_key else None,
            "aws_access_key_id": self.aws_access_key_id.to_dict() if self.aws_access_key_id else None,
            "aws_secret_access_key": self.aws_secret_access_key.to_dict() if self.aws_secret_access_key else None,
            "aws_region_name": self.aws_region_name,
            "aws_s3_bucket_name": self.aws_s3_bucket_name,
            "output_folder": self.output_folder,
            "voice_id": self.voice_id,
            "model_id": self.model_id,
            "voice_settings": self.voice_settings,
        }
        # Include any additional kwargs
        init_parameters.update(self.kwargs)
        return default_to_dict(
            self,
            **init_parameters
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ElevenLabsTextToSpeech":
        """Deserializes the component from a dictionary."""
        init_parameters = data.get("init_parameters", {})
        deserialize_secrets_inplace(init_parameters, keys=[
            "elevenlabs_api_key",
            "aws_access_key_id",
            "aws_secret_access_key",
        ])
        return cls(**init_parameters)
