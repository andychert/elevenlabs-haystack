# ElevenLabs Haystack Integration

This repository contains an integration of ElevenLabs' Text-to-Speech API with Haystack pipelines. This package allows you to convert text to speech using ElevenLabs' API and optionally save the generated audio to AWS S3.

## Installation

1. Install:

   ```bash
   pip install elevenlabs_haystack
   ```

2. Set up environment variables for sensitive credentials.

   Create a `.env` file in the root directory with the following content (replace with your actual credentials):

   ```bash
   ELEVENLABS_API_KEY=sk_your_elevenlabs_api_key_here
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   AWS_REGION_NAME=us-east-1
   AWS_S3_BUCKET_NAME=your_s3_bucket_name
   ```

   These variables will be automatically loaded using `dotenv` and used to access ElevenLabs and AWS services securely.

## Usage

### Basic Text-to-Speech Example

This example shows how to use the `ElevenLabsTextToSpeech` component to convert text to speech and save the generated audio file locally or in an AWS S3 bucket. It uses environment variables to access sensitive credentials.

```python
from haystack.utils import Secret
from elevenlabs_haystack import ElevenLabsTextToSpeech

# Initialize the ElevenLabsTextToSpeech component using environment variables for sensitive data
tts = ElevenLabsTextToSpeech(
    elevenlabs_api_key=Secret.from_env_var("ELEVENLABS_API_KEY"),
    output_folder="audio_files",  # Save the generated audio locally
    voice_id="K8lgMMdmFr7QoEooafEf",  # ElevenLabs voice ID
    aws_s3_bucket_name=Secret.from_env_var("AWS_S3_BUCKET_NAME"),  # S3 bucket for optional upload
    aws_s3_output_folder="s3_files",  # Save the generated audio to AWS S3
    aws_access_key_id=Secret.from_env_var("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=Secret.from_env_var("AWS_SECRET_ACCESS_KEY"),
    aws_region_name=Secret.from_env_var("AWS_REGION_NAME"),  # AWS region
    voice_settings={
        "stability": 0.75,
        "similarity_boost": 0.75,
        "style": 0.5,
        "use_speaker_boost": True,  # Optional voice settings
    },
)

# Run the text-to-speech conversion
result = tts.run("Hello, world!")

# Print the result
print(result)

"""
{
    "id": "elevenlabs-id",
    "file_name": "audio_files/elevenlabs-id.mp3",
    "s3_file_name": "s3_files/elevenlabs-id.mp3",
    "s3_bucket_name": "test-bucket",
    "s3_presigned_url": "https://test-bucket.s3.amazonaws.com/s3_files/elevenlabs-id.mp3"
}
"""
```

### Example Using Haystack Pipeline

This example demonstrates how to integrate the `ElevenLabsTextToSpeech` component into a Haystack pipeline. Additionally, we define a `WelcomeTextGenerator` component that generates a personalized welcome message.

```python
from haystack import component, Pipeline
from haystack.utils import Secret
from elevenlabs_haystack import ElevenLabsTextToSpeech

# Define a simple component to generate a welcome message
@component
class WelcomeTextGenerator:
    """
    A component generating a personal welcome message and making it upper case.
    """
    @component.output_types(welcome_text=str, note=str)
    def run(self, name: str):
        return {
            "welcome_text": f'Hello {name}, welcome to Haystack!'.upper(),
            "note": "welcome message is ready"
        }

# Create a Pipeline
text_pipeline = Pipeline()

# Add WelcomeTextGenerator to the Pipeline
text_pipeline.add_component(
    name="welcome_text_generator",
    instance=WelcomeTextGenerator()
)

# Add ElevenLabsTextToSpeech to the Pipeline using environment variables
text_pipeline.add_component(
    name="tts",
    instance=ElevenLabsTextToSpeech(
        elevenlabs_api_key=Secret.from_env_var("ELEVENLABS_API_KEY"),
        output_folder="audio_files",  # Save the generated audio locally
        voice_id="K8lgMMdmFr7QoEooafEf",  # ElevenLabs voice ID
        aws_s3_bucket_name=Secret.from_env_var("AWS_S3_BUCKET_NAME"),  # S3 bucket for optional upload
        aws_s3_output_folder="s3_files",  # Save the generated audio to AWS S3
        aws_access_key_id=Secret.from_env_var("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=Secret.from_env_var("AWS_SECRET_ACCESS_KEY"),
        aws_region_name=Secret.from_env_var("AWS_REGION_NAME"),  # Load region from env
        voice_settings={
            "stability": 0.75,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True,  # Optional voice settings
        },
    ),
)

# Connect the output of WelcomeTextGenerator to the input of ElevenLabsTextToSpeech
text_pipeline.connect(sender="welcome_text_generator.welcome_text", receiver="tts")

# Run the pipeline with a sample name
result = text_pipeline.run({"welcome_text_generator": {"name": "Bilge"}})

# Print the result
print(result)

"""
{
    "id": "elevenlabs-id",
    "file_name": "audio_files/elevenlabs-id.mp3",
    "s3_file_name": "s3_files/elevenlabs-id.mp3",
    "s3_bucket_name": "test-bucket",
    "s3_presigned_url": "https://test-bucket.s3.amazonaws.com/s3_files/elevenlabs-id.mp3"
}
"""
```

### Example `.env` File

Here's an example `.env` file containing environment variables:

```bash
ELEVENLABS_API_KEY=sk_your_elevenlabs_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION_NAME=us-east-1
AWS_S3_BUCKET_NAME=your_s3_bucket_name
```

### Running the Examples

To run the examples:

1. Ensure you have set up your environment variables in the `.env` file as shown above.
2. Run your Python script:

   ```bash
   poetry run python your_script.py
   ```

## License

This project is licensed under the MIT License.
