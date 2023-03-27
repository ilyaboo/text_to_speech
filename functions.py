from pathlib import Path
from gtts import gTTS
from gtts import lang
from PyPDF2 import PdfReader
import docx
from langdetect import detect

def filepath_check(filepath, extension):
    # checks the filepath and returns an
    # according status
    path = Path(filepath)
    # check if the path exists
    if not path.exists():
        return "invalid path"
    # check if it is a file
    elif not path.is_file():
        return "not file"
    # check if extension is correct
    elif not filepath.endswith(extension):
        return "invalid extension"
    else:
        return "correct"
    
def generate_speech_audio(filepath, extension):
    # function that generates the audio file
    # from filepath and extension
    # creating a name for recording
    if extension == ".txt":
        text = read_txt(filepath)
    elif extension == ".pdf":
        text = read_pdf(filepath)
    else:
        text = read_docx(filepath)
    name = generate_filename(filepath)
    language = get_language(text)
    if language == None:
        return False
    else:
        audio = gTTS(text = text, lang = language, slow = False)
        audio.save(name)
    return True

def generate_filename(filepath):
    # function that generates the name of a generated
    # .mp3 file using the filepath to the original
    # text file
    name = filepath
    if "/" in filepath:
        name = filepath.split("/")[-1]
    if "." in name:
        name = name.split(".")[0]
    name += ".mp3"
    return name

def read_txt(filepath):
    # function that extracts text from a .txt document
    # and returns a single string with the text
    text = ""
    file = open(filepath, "r")
    for line in file:
        text += line
    file.close()
    return text

def read_pdf(filepath):
    # function that extracts text from a .pdf document
    # and returns a single string with the text
    text = ""
    reader = PdfReader(filepath)
    for page in reader.pages:
        text += " " + page.extract_text()
    return text

def read_docx(filepath):
    # function that extracts text from a .docx document
    # and returns a single string with the text
    doc = docx.Document(filepath)
    text = ""
    for paragraph in doc.paragraphs:
        text += " " + paragraph.text
    return text

def get_language(text):
    # function that detects the language of the
    # text string and returns the code of the langeuage
    # if there is no such language or it is not supported
    # it erturns None
    try:
        language = detect(text)
    except:
        # no language features
        return None
    languages = lang.tts_langs()
    if language not in languages:
        return None
    else:
        return language
