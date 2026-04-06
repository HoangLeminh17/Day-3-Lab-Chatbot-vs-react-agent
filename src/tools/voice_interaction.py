"""
Voice interaction tool for converting user speech to text input for the agent.
Supports multiple speech recognition backends (Google, OpenAI Whisper, offline).
"""

import os
from typing import Optional
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()


class VoiceInteractionTool:
    """Tool for capturing and converting voice input to text."""
    
    def __init__(
        self,
        backend: str = "google",
        language: str = "vi-VN",
        microphone_index: Optional[int] = None,
        ambient_duration: float = 1.2,
        pause_threshold: float = 1.2,
        non_speaking_duration: float = 0.7,
    ):
        """
        Initialize the voice interaction tool.
        
        Args:
            backend: Speech recognition backend ('google', 'whisper', or 'sphinx' for offline)
            language: Speech recognition language code (for example: 'vi-VN', 'en-US')
            microphone_index: Optional microphone index. If None, default system mic is used.
            ambient_duration: Seconds used to calibrate ambient noise.
            pause_threshold: Seconds of silence before phrase is considered complete.
            non_speaking_duration: Minimum seconds of silence to keep on both sides of phrase.
        """
        self.recognizer = sr.Recognizer()
        self.backend = backend
        self.language = language
        self.microphone_index = microphone_index
        self.ambient_duration = ambient_duration
        self.pause_threshold = pause_threshold
        self.non_speaking_duration = non_speaking_duration
        self.microphone = None
        
    def listen_and_transcribe(self, timeout: int = 60, phrase_time_limit: int = None) -> Optional[str]:
        """
        Listen to microphone input and transcribe speech to text.
        
        Args:
            timeout: Maximum time in seconds to wait for speech to start
            phrase_time_limit: Maximum time in seconds for the speech phrase
            
        Returns:
            Transcribed text or None if recognition failed
        """
        try:
            # Initialize microphone lazily
            if self.microphone is None:
                try:
                    self.microphone = sr.Microphone(device_index=self.microphone_index)
                except (AttributeError, OSError) as e:
                    print(f"Error: Microphone not available - {e}")
                    print("Please install pyaudio: pip install pyaudio")
                    return None
            
            with self.microphone as source:
                print("Listening... (speak now)")
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = self.pause_threshold
                self.recognizer.non_speaking_duration = self.non_speaking_duration
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=self.ambient_duration)
                
                # Listen to the microphone
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
            print("Processing...")
            
            # Transcribe using selected backend
            if self.backend == "whisper":
                return self._transcribe_whisper(audio)
            elif self.backend == "google":
                return self._transcribe_google(audio)
            elif self.backend == "sphinx":
                return self._transcribe_sphinx(audio)
            else:
                raise ValueError(f"Unknown backend: {self.backend}")
                
        except sr.UnknownValueError:
            print("Error: Could not understand audio. Please speak again.")
            return None
        except sr.RequestError as e:
            print(f"Error: Could not communicate with the API: {e}")
            return None
        except Exception as e:
            print(f"Error: Error during listening: {e}")
            return None
    
    def _transcribe_whisper(self, audio: sr.AudioData) -> Optional[str]:
        """
        Transcribe using OpenAI Whisper API.
        
        Args:
            audio: Audio data from microphone
            
        Returns:
            Transcribed text or None
        """
        try:
            from openai import OpenAI
            
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("Warning: OPENAI_API_KEY not set. Using Google Speech Recognition instead.")
                return self._transcribe_google(audio)
            
            # Convert audio to wav format for Whisper
            wav_data = audio.get_wav_data()
            
            # Use OpenAI Whisper API
            client = OpenAI(api_key=api_key)
            
            # Save audio temporarily
            temp_audio_path = "/tmp/voice_input.wav"
            with open(temp_audio_path, "wb") as f:
                f.write(wav_data)
            
            # Transcribe with Whisper
            with open(temp_audio_path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language=(self.language.split("-")[0] if "-" in self.language else self.language)
                )
            
            # Clean up
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            
            text = transcript.text.strip()
            print(f"Transcribed (Whisper): {text}")
            return text
            
        except Exception as e:
            print(f"Error: Whisper transcription failed: {e}. Falling back to Google.")
            return self._transcribe_google(audio)
    
    def _transcribe_google(self, audio: sr.AudioData) -> Optional[str]:
        """
        Transcribe using Google Speech Recognition API.
        
        Args:
            audio: Audio data from microphone
            
        Returns:
            Transcribed text or None
        """
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            text = text.strip()
            print(f"Transcribed (Google): {text}")
            return text
        except sr.UnknownValueError:
            print("Error: Google could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Error: Google API error: {e}")
            return None
    
    def _transcribe_sphinx(self, audio: sr.AudioData) -> Optional[str]:
        """
        Transcribe using PocketSphinx (offline, no API key needed).
        
        Args:
            audio: Audio data from microphone
            
        Returns:
            Transcribed text or None
        """
        try:
            text = self.recognizer.recognize_sphinx(audio)
            text = text.strip()
            print(f"Transcribed (Sphinx): {text}")
            return text
        except sr.UnknownValueError:
            print("Error: Sphinx could not understand audio.")
            return None
        except Exception as e:
            print(f"Error: Sphinx error: {e}")
            return None


def voice_input(backend: str = "google", timeout: int = 20) -> Optional[str]:
    """
    Simple function to get voice input from user.
    
    Args:
        backend: Speech recognition backend ('google', 'whisper', or 'sphinx')
        timeout: Maximum time in seconds to wait for speech to start
        
    Returns:
        Transcribed text or None if recognition failed
    """
    language = os.getenv("SPEECH_LANGUAGE", "vi-VN")
    microphone_index_env = os.getenv("MICROPHONE_INDEX")
    microphone_index = int(microphone_index_env) if microphone_index_env and microphone_index_env.isdigit() else None
    phrase_time_limit_env = os.getenv("SPEECH_PHRASE_TIME_LIMIT")
    phrase_time_limit = int(phrase_time_limit_env) if phrase_time_limit_env and phrase_time_limit_env.isdigit() else None
    ambient_duration = float(os.getenv("SPEECH_AMBIENT_DURATION", "1.2"))
    pause_threshold = float(os.getenv("SPEECH_PAUSE_THRESHOLD", "1.2"))
    non_speaking_duration = float(os.getenv("SPEECH_NON_SPEAKING_DURATION", "0.7"))
    tool = VoiceInteractionTool(
        backend=os.getenv("SPEECH_BACKEND", backend),
        language=language,
        microphone_index=microphone_index,
        ambient_duration=ambient_duration,
        pause_threshold=pause_threshold,
        non_speaking_duration=non_speaking_duration,
    )
    return tool.listen_and_transcribe(timeout=timeout, phrase_time_limit=phrase_time_limit)


def list_microphones() -> list[str]:
    """Return available microphone device names."""
    try:
        return sr.Microphone.list_microphone_names()
    except Exception:
        return []


def voice_to_text_agent_tool():
    """
    Tool definition for use with the ReAct Agent.
    Returns a dictionary with tool metadata.
    """
    return {
        "name": "voice_input",
        "description": "Capture and convert user voice input to text. Call this to get voice instructions from the user.",
        "fn": voice_input
    }
