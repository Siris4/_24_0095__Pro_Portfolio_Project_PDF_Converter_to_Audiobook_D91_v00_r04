from google.cloud import texttospeech
from google.oauth2 import service_account
import PyPDF2

# Path to your service account key file
key_path = r'C:\Users\Siris\Desktop\GitHub Projects 100 Days NewB\_24_0095__Day91_Pro_Portfolio_Project_PDF_Converter_to_Audiobook__240925\NewProject\r00_env_START\r04\siris-speaks-a3c7c1b182ec.json'

# Path to your PDF file
pdf_path = r'C:\Users\Siris\Desktop\GitHub Projects 100 Days NewB\_24_0095__Day91_Pro_Portfolio_Project_PDF_Converter_to_Audiobook__240925\NewProject\r00_env_START\r04\Machine Learning for Asset Managers by Marcos Lopez de Prado.pdf'

# Authenticate using the service account credentials
credentials = service_account.Credentials.from_service_account_file(key_path)

# Set up the Text-to-Speech client with the credentials
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()  # Extract text from each page
        return text

# Function to split text by byte size
def split_text_by_byte_size(text, max_bytes=5000):
    encoded_text = text.encode('utf-8')  # Encode the text to get byte size
    chunks = []
    start = 0
    while start < len(encoded_text):
        end = start + max_bytes
        # Make sure we don't split in the middle of a multi-byte character
        while end < len(encoded_text) and (encoded_text[end] & 0xC0) == 0x80:
            end -= 1
        chunk = encoded_text[start:end].decode('utf-8')
        chunks.append(chunk)
        start = end
    return chunks

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Split the PDF text into smaller chunks by byte size
text_chunks = split_text_by_byte_size(pdf_text)

# Process each chunk separately
for i, chunk in enumerate(text_chunks):
    # Set up the input for the API using the chunked text
    synthesis_input = texttospeech.SynthesisInput(text=chunk)

    # Configure the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # Change to your preferred language
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Can be FEMALE or MALE
    )

    # Specify the audio file format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3  # Other options include LINEAR16 (WAV)
    )

    # Call the Text-to-Speech API
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Save the synthesized speech for each chunk as a separate audio file
    output_filename = f"output_chunk_{i+1}.mp3"
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file '{output_filename}'")
