import openai
import os
import boto3
from contextlib import closing
from pydub import AudioSegment
from pydub.playback import play as play_audio

#ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
#SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
#REGION_NAME = 'us-west-2'

# Creating Poetry with GPT-4
messages = [
    {
        "role": "system",
        "content": """Compose a poem with the following characteristics:

                        Style: historical
                        Length: 12 lines
                        Genre: independent
                        write your poetry in the way of the best poets from history.""",
    },
]

user_input = input("Type anything - words, feelings, or more - and watch them become poetry.: ")

# Add user input to messages
messages.append({"role": "user", "content": user_input})

response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
openai.api_key = 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
mod = openai.Moderation.create(

    input= response['choices'][0]['message']['content']
)
output = mod["results"][0].flagged
print(output)


if output:
    print("Try again")
else:

    poetry = response['choices'][0]['message']['content']
    print(poetry)

    def synthesize_speech(text, voice_id="Brian", output_file="poetry.mp3"):
        # Initialize AWS Polly client
        polly_client = boto3.client(
            "polly",
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=SECRET_ACCESS_KEY,
            region_name=REGION_NAME,
        )

        # Synthesize speech with the specified voice
        response = polly_client.synthesize_speech(
            OutputFormat="mp3", Text=text, VoiceId=voice_id, TextType="text", Engine="neural"
        )

        # Save synthesized speech to a file and load it with pydub
        with closing(response["AudioStream"]) as stream:
            with open(output_file, "wb") as file:
                file.write(stream.read())

            audio = AudioSegment.from_file(output_file, format="mp3")

        print(f"Poetry saved to {output_file}")
        return audio

    audio = synthesize_speech(poetry)

    # Play the audio
    print("Playing the poetry...")
    play_audio(audio)
