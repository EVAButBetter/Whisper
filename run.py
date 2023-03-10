from speech_recognition.recorder import Recorder
from speech_recognition.speech_recognition_whisper import SpeechRecognitionWhisper
import sys
import requests

url = 'http://localhost:8000/api/v1/pipeline/'


def get_transcription():
    recording_path = recorder.listen()

    lang, eng_transcription = speech_recognition_system.run(recording_path)

    return eng_transcription


def run_whisper(step_num=1):
    if step_num == 0:
        print("Session has ended.")
        exit()
    else:

        eng_transcription = get_transcription()

        myobj = {'content': eng_transcription}

        try:
            x = requests.post(url, json=myobj)
        except requests.exceptions.ConnectionError:
            print("There was an error. Closing")
            return 0

        if x.status_code != 200:
            print("there was an error. closing")
            return 0

        json_answer = x.json()

        print(json_answer["content"]["text"])
        print("\n")
        # TODO: CHECK IF OUTPUT IS VOICE AND GENERATE IF SO

        next_step = json_answer["content"]["next_step"]
        return next_step


if __name__ == "__main__":

    argv = sys.argv

    print("#### STARTING EVA... BUT BETTER! ####\n")

    recorder = Recorder()

    speech_recognition_system = SpeechRecognitionWhisper()

    speech_recognition_system.print_description()

    ### LISTENING ###
    print("You have chosen audio input/output, so please make your request now to your microphone\n")
    input_type = "voice"

    next_step = 1
    while True:
        next_step = run_whisper(step_num=next_step)
