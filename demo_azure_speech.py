
import azure.cognitiveservices.speech as speechsdk

#---- enregistrer vos accès -----
speech_key, service_region = "", "westus2" #<-- compléter avec vos accès

#---------------------------------
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language="fr-FR")
#API en anglais par défaut, retirer speech_recognition_language="fr-FR" pour la version anglaise

#----- Fichier audio -------------
audio_filename = "bonjour.wav" #<--- indiquez ici le nom du fichier .wav 


#---- result functions -----
def result_stt(result):
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("J'ai reconnu: {}".format(result.text))
        
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("Déso, rien reconnu : {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Annulé : {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Erreur details: {}".format(cancellation_details.error_details))

    input("(press Enter)")
    main_menu()

def result_tts(result):

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("c'est dit ;)")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("êtes-vous sûr d'avoir mis à jour vos API keys dans le programme ?")
    
    input("(press Enter)")
    main_menu()

#---- fonctions API ----
#     
def stt_micro():
    
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Dis-moi quelque chose : ")
    send_result = speech_recognizer.recognize_once()
    result_stt(send_result)


def stt_file():

    audio_config = speechsdk.audio.AudioConfig(filename=audio_filename)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print('Ok je lis le fichier ...')

    send_result = speech_recognizer.recognize_once()
    result_stt(send_result)


def stt_custom_file():

    speech_config.endpoint_id = "" # <-- indiquez ici le endpoint id de votre modèle custom
    
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Dis-moi quelque chose : ")

    send_result = speech_recognizer.recognize_once()
    result_stt(send_result)

def tts_standard():

    # Receives a text from console input.
    print("Tapez ici le texte que vous souhaitez que je dise : ")
    text = input()

    language = "eng-US"#"fr-FR" 
    speech_config.speech_synthesis_language = language

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    # Synthesizes the received text to speech.
    
    send_result = speech_synthesizer.speak_text_async(text).get()
    result_tts(send_result)

def tts_neuronal():

    # Receives a text from console input.
    print("Tapez ici le texte que vous souhaitez que je dise : ")
    text = input()

    voice = "Microsoft Server Speech Text to Speech Voice (en-US, AriaNeural)"
    speech_config.speech_synthesis_voice_name = voice

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    # Synthesizes the received text to speech.
    
    send_result = speech_synthesizer.speak_text_async(text).get()
    result_tts(send_result)
    
#---- menu ----  

def main_menu():
    print(""" 
    1. Speech-to-Text avec un micro
    2. Speech-to-Text avec un fichier wav
    3. Custom-Speech avec un micro
    4. Text-to-Speech avec voix standard
    5. Text-to-Speech avec voix neuronale (english)

    6. Quitter
    """)
    choice=input("Azure Speech demo, que choisissez-vous ?")
    if choice=="1":
        stt_micro()
    elif choice=="2":
        stt_file()
    elif choice=="3":
        stt_custom_file()
    elif choice=="4":
        tts_standard()
    elif choice=="5":
        tts_neuronal()
    elif choice=="6":

        print('Bye bye !!')
    else:
        print("choix non valide, bye bye")

main_menu()