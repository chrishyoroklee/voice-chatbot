# the-voice-chatbot 
the-voice-chatbot is a Streamlit-based web application that allows users to chat with a virtual voice teacher. Powered by LangChain and OpenAI, this enables users to talk to a virtual voice teacher that has been trained with voice-specific resources.

## Features

- **Natural Language Queries**: Ask questions about voice and vocal training.
- **Chat History**: Maintains a conversation history for context-aware responses.
- **Source Documents**: Displays the sections of the PDF used to generate answers.
- **OpenAI Integration**: Uses OpenAI's GPT models for generating responses.
- **Streamlit UI**: Simple and intuitive user interface.

## Demo

## How It Works

1. **PDF Processing**: The app uses `PyPDFLoader` to extract text from the uploaded PDF.
2. **Text Splitting**: The text is split into smaller chunks using `RecursiveCharacterTextSplitter`.
3. **Vector Database**: A vector database is created using `DocArrayInMemorySearch` and OpenAI embeddings.
4. **Chat Interface**: Users can ask questions, and the app retrieves relevant information from the vector database using LangChain's `ConversationalRetrievalChain`.
5. **Response Generation**: OpenAI's GPT model generates responses based on the retrieved information.

## Installation

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key (get it from [OpenAI](https://platform.openai.com/))

### Steps
Go to https://the-voice-chatbot.streamlit.app/
