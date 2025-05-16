import os
import signal

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import (
    DefaultAudioInterface,
)

from dotenv import load_dotenv
from tools import client_tools

load_dotenv()

agent_id = os.getenv("AGENT_ID")
api_key = os.getenv("ELEVENLABS_API_KEY")
if not agent_id:
    raise ValueError("AGENT_ID environment variable is not set.")
if not api_key:
    raise ValueError("ELEVENLABS_API_KEY environment variable is not set.")
if not client_tools:
    raise ValueError("No tools found. Please set up your tools in the tools.py file.")  

client = ElevenLabs(api_key=api_key)


conversation = Conversation(
    client,
    agent_id,
    client_tools=client_tools,
    requires_auth=bool(api_key),
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=lambda response: print(f"Agent: {response}"),
    callback_agent_response_correction=lambda original, corrected: print(f"Agent: {original} -> {corrected}"),
    callback_user_transcript=lambda transcript: print(f"User: {transcript}"),
)

conversation.start_session()
signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())
conversation_id = conversation.wait_for_session_end()
print(f"Conversation ID: {conversation_id}")