#Music Player Project for Dorm Room, Room No. 508, Author: Sarthak Sharma

#All the necessary imports
import os
import pygame
from mutagen.mp3 import MP3
import time
import speech_recognition as pi_speech
import win32com.client as WinEngine
import random
#The main song class, holds all the memeber variables and methods required to manipulate the song object
class Song():
    def __init__(self,song_path):
        self.song_path = song_path
    def get_files(self):
        song_path = self.song_path
        result = []
        allfiles = os.listdir(song_path) # Lists all files in the current directory
        for item in allfiles: # iterate over all files in the current directory
            if item.endswith('.mp3'): # Checks if the file is a mp3 file
                result.append(item)
        return result
    def playsong(self):
        nextSongCommands = ['next','play next song','next song','lets play the next one','next one','play the next one', 'play the next song', 'Hey MusiPi, play the next song']
        transitionVoices = ['Here You Go Man','Changing the song Now','Lets Rock, playing the next song now']
        MusiPi = WinEngine.Dispatch("SAPI.SpVoice")#Initiate Microsoft's SAPI(Sound API and the SpVoice Interface to access Text To Speech)
        commandRecognizer = pi_speech.Recognizer()
        commandMic = pi_speech.Microphone()
        recognizer = pi_speech.Recognizer()#Initialize the recognizer as an instance of the Recognizer class
        mic = pi_speech.Microphone()#Initialize the mic
        with mic as source:
            recognizer.adjust_for_ambient_noise(source) #Adjusts for the ambient noise
            audio_input = recognizer.listen(source) #Takes the audio input from the user
            if((recognizer.recognize_google(audio_input)).lower() == 'start'):# Analyze the audio input
                print("############### -- MusiPi -- ############### Created By :- Sarthak Sharma")
            if(len(self.get_files()) == 0):
                print("Can't find any .mp3 file in the specified directory, Failed to load the files")
            else:
                print(f"##### {len(self.get_files())} Files Found, now loading #####")
                if(len(self.get_files()) == 1):
                    print("### -- Added 1 item to the Queue -- ###")
                else:
                    print(f"### -- Added {len(self.get_files())} items to the Queue -- ###")

                pygame.mixer.init()#Initializes the pygame's mixer
                for vals in range(0, len(self.get_files())):
                    transitionSelector = random.randint(0,3)#To make transitions more human-like
                    current_song= self.get_files()[vals] #Sets the current_song
                    full_path = self.song_path + current_song #Sets the full path of the song for future use with pygame's mixer
                    pygame.mixer.music.load(full_path)
                    audio_file = MP3(full_path) #Creates an instance of MP3 class so as to get the informaion about the file(using Mutagen Here!!)
                    print(f"\n### -- Playing Song Number {vals+1} -- ###")
                    print(f"### -- Song Name :{current_song} -- ### -- Loaded Successfully -- ###")
                    print(f"### -- Length :{audio_file.info.length//60} minutes {audio_file.info.length%60} seconds -- ###")
                    print(f"### -- Now Playing {current_song} -- ###")
                    pygame.mixer.music.play()
                    print("---Ready To Take Voice Commands---")
                    while(pygame.mixer.music.get_busy()):
                        with commandMic as source:
                            commandRecognizer.adjust_for_ambient_noise(source) #Adjusts for the ambient noise
                            audio_input = commandRecognizer.listen(source) #Takes the audio input from the user
                        try:
                            if(commandRecognizer.recognize_google(audio_input).lower() in nextSongCommands):
                                pygame.mixer.music.stop()
                                MusiPi.Speak(transitionVoices[transitionSelector])
                                break;
                            elif(commandRecognizer.recognize_google(audio_input).lower() == "pause"):
                                pygame.mixer.music.pause()
                                MusiPi.Speak("Paused The Playback.")
                            elif(commandRecognizer.recognize_google(audio_input).lower() == "resume"):
                                pygame.mixer.music.unpause()
                                MusiPi.Speak("Resuming the playback now.")
                            elif(commandRecognizer.recognize_google(audio_input).lower() == "shutdown"):
                                pygame.mixer.music.stop()
                                MusiPi.Speak("Shutting MusiPi Down, Thankyou for using me.")
                                quit()
                        except:
                            print("$MusiPi : Unknown Voice Command, Please try again.")
                            audio_input.flush=True#Very Important, Flushes the trash out from the input stream so that new commands can be properly and efficiently recognized.
                        pygame.time.Clock().tick()

if(__name__ == '__main__'):
    song_path = input("Enter the Music Directory Path :")
    song_file = Song(song_path)
    song_file.playsong()
