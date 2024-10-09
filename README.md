# ElevenLabs Haystack Integration

This package provides Haystack components for integrating ElevenLabs Text-to-Speech services into your Haystack pipelines.

## Installation

Use Poetry to install the package:

```bash
pip install elevenlabs_haystack
```

## Usage

```python
from haystack import component, Pipeline
from haystack.utils import Secret

from elevenlabs_haystack import ElevenLabsTextToSpeech

@component
class WelcomeTextGenerator:
  """
  A component generating personal welcome message and making it upper case
  """
  @component.output_types(welcome_text=str, note=str)
  def run(self, name:str):
    return {"welcome_text": ('Hello {name}, welcome to Haystack!'.format(name=name)).upper(), "note": "welcome message is ready"}

text_pipeline = Pipeline()
text_pipeline.add_component(name="welcome_text_generator", instance= WelcomeTextGenerator())
text_pipeline.add_component(
    instance=ElevenLabsTextToSpeech(
        elevenlabs_api_key=Secret.from_token("elevenlabs_api_key"),
        output_folder="audio_files",
        voice_id="K8lgMMdmFr7QoEooafEf",
        aws_s3_bucket_name="mybucket",
        aws_access_key_id=Secret.from_token("aws_access_key_id"),
        aws_secret_access_key=Secret.from_token("aws_secret_access_key"),
        aws_region_name="us-east-1",
        voice_settings={
            "stability": 0.75,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True,
        },  # Optional
    ),
    name="tts",
)

text_pipeline.connect(sender="welcome_text_generator.welcome_text", receiver="tts.text")

result = text_pipeline.run({"welcome_text_generator":{"name": "Bilge"}})

print(result)

"""
{
   "file_path":"audio_files/364700f0-791f-4ceb-9e71-c13479c8e126.mp3",
   "s3_file_name":"364700f0-791f-4ceb-9e71-c13479c8e126.mp3",
   "s3_bucket_name":"mybucket",
   "s3_presigned_url":"https://mybucket.s3.amazonaws.com/364700f0-791f-4ceb-9e71-c13479c8e126.mp3?AWSAccessKeyId=AKIIVY2PHBT5JH2FX7K2&Signature=9b%2Bgm2OZRucl5iXsd8wwGl9QgoU%3D&Expires=1728488887"
}
"""
```

## Configuration

- API Keys: You can provide API keys directly or set them as environment variables.
- Voice Settings: Customize the voice settings by passing a dictionary to voice_settings.

## License

This project is licensed under the MIT License.
