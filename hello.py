from tkinter import *
from tkinter import messagebox
from deep_translator import GoogleTranslator
from gtts import gTTS
from playsound import playsound
import threading
import os


class LanguageTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translator")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        # language dictionary
        self.languages = {
            "Telugu": "te",
            "Tamil": "ta",
            "Hindi": "hi",
            "English": "en",
            "Bengali": "bn",
            "Marathi": "mr",
            "Urdu": "ur",
            "Kannada": "kn",
            "Malayalam": "ml",
            "Punjabi": "pa"
        }

        self.create_widgets()

    def create_widgets(self):
        # title
        Label(self.root, text="Language Translator",
              font=("Arial", 16)).pack(pady=10)

        # input box
        Label(self.root, text="Enter Text").pack()
        self.input_text = Text(self.root, height=5, width=45)
        self.input_text.pack(pady=5)

        # language dropdown
        Label(self.root, text="Select Language").pack(pady=5)

        self.language_var = StringVar()
        self.language_var.set("Telugu")

        OptionMenu(self.root, self.language_var,
                   *self.languages.keys()).pack()

        # translate button
        Button(self.root, text="Translate",
               command=self.translate_text,
               bg="red", fg="white").pack(pady=10)

        # output box
        Label(self.root, text="Translated Text").pack()
        self.output = Text(self.root, height=5, width=45)
        self.output.pack(pady=5)

    def speak_text(self, text, lang):
        try:
            filename = "voice.mp3"

            tts = gTTS(text=text, lang=lang)
            tts.save(filename)

            playsound(filename)

            os.remove(filename)

        except Exception as e:
            messagebox.showerror("Audio Error", str(e))

    def translate_text(self):
        text = self.input_text.get("1.0", END).strip()

        if text == "":
            messagebox.showwarning("Warning", "Please enter text")
            return

        try:
            lang = self.languages[self.language_var.get()]

            translated = GoogleTranslator(
                source='auto',
                target=lang
            ).translate(text)

            self.output.delete("1.0", END)
            self.output.insert(END, translated)

            # audio in thread
            threading.Thread(
                target=self.speak_text,
                args=(translated, lang),
                daemon=True
            ).start()

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = Tk()
    app = LanguageTranslator(root)
    root.mainloop()