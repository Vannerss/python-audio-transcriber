import speech_recognition as sr
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

home_dir = os.path.expanduser("~")
documents_dir = os.path.join(home_dir, "Documents")
transcriptionsPath = os.path.join(documents_dir, "Transcriptions")

if not os.path.exists(transcriptionsPath):
    print("Creating missing directory /Transcriptions...")
    os.makedirs(transcriptionsPath, True)
    print("Directory Created. \n")

r = sr.Recognizer()

path_file = ""


def browse_file():
    print("Browsing Files...")
    global path_file
    path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    if path != "":
        selected_label.config(text=f'Selected file: {path}', fg="green")
        path_file = path
        print(path_file)
        process_button.config(state="normal")
        label.config(text="Ready to process.", fg="green")


def process_file():
    processing_label.config(text="Processing File...")
    if path_file != "":
        print("File Path Found")
        start_transcription(path_file, language_dropdown.get())


def open_result():
    os.startfile(transcriptionsPath)


def quit_transcriber():
    quit()


def create_unique_file(directory, base_name, extension):
    file_name = f"{base_name}.{extension}"
    file_path = os.path.join(directory, file_name)

    # If the file already exists, add a number to the file name
    count = 1
    while os.path.exists(file_path):
        file_name = f"{base_name}_{count}.{extension}"
        file_path = os.path.join(directory, file_name)
        count += 1

    return file_path


def start_transcription(path, lang):
    with sr.AudioFile(path) as source:
        print('Fetching File...')
        audio_text = r.listen(source)
        try:
            print('Converting audio transcripts into text...')
            text = r.recognize_google(audio_text, language=lang)

            f = open(create_unique_file(transcriptionsPath, "transcription","txt"), mode="w+")
            f.write(text)
            print(f'Audio File Transcribed... Saved in {transcriptionsPath}')
            processing_label.config(text="Success!", fg="green")
        except:
            processing_label.config(text="Transcription Attempt Failed.", fg="red")


root = tk.Tk()
root.title("Audio Transcriber")

options = ['es-ES', 'en-US']
language_dropdown = ttk.Combobox(root, values=options)

language_dropdown.set(options[0])

browse_button = tk.Button(root, text="Browse Files", command=browse_file)
browse_button.pack(pady=1)
selected_label = tk.Label(root, text="")
selected_label.pack()

process_button = tk.Button(root, text="Process File", command=process_file)
process_button.pack(pady=1)
label = tk.Label(root, text="")
label.pack()

if path_file == "":
    process_button.config(state="disabled")
    label.config(text="Choose an audio file first.", fg="red")

progress_bar = ttk.Progressbar(root, mode="determinate", length=300)
progress_bar.pack(pady=20)

processing_label = tk.Label(root, text="")
processing_label.pack(pady=10)
open_save_location = tk.Button(root, text="Open Save Location", command=open_result)
open_save_location.pack(pady=10)

quit_button = tk.Button(root, text="Quit", command=open_result)
quit_button.pack(pady=10)

root.mainloop()



