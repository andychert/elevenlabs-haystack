"""
ElevenLabs Text-to-Speech components for Haystack.
"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

from .component import ElevenLabsTextToSpeech

__all__ = ["ElevenLabsTextToSpeech"]
