# 🐦 TWEEPY - Tweet Sentiment Classifier

A FastAPI-based web application that classifies tweet sentiments using Google's Gemini AI model. The application handles large-scale batch processing with intelligent token management and checkpoint recovery.

## Features

- **File Upload**: Upload tweet data in JSON, CSV, or TXT format (up to 10MB)
- **Smart Batching**: Automatically splits data into optimized batches based on token count
- **AI Classification**: Uses Google Gemini 2.5 Flash for sentiment analysis
- **Batch Processing**: Classifies tweets into Positive, Negative, or Neutral sentiments
- **Checkpoint Recovery**: Resumes processing from last successful batch if interrupted
- **Retry Logic**: Implements exponential backoff for API failures
- **Download Results**: Export processed results as files

## Tech Stack

- **Backend**: FastAPI (Python)
- **AI Model**: Google Gemini 2.5 Flash
- **Token Counting**: Tiktoken (CL100K encoding)
- **Frontend**: HTML/CSS/JavaScript
- **File Handling**: Pathlib, JSON

## Project Structure

```
.
├── src/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── upload.py      # File upload endpoint
│   │   │   └── classify.py    # Classification endpoint
│   │   ├── services/
│   │   │   ├── ai_client.py        # Gemini API integration
│   │   │   ├── batching.py         # Token-based batching logic
│   │   │   ├── checkpoint.py       # Progress tracking
│   │   │   └── data.py             # Data loading utilities
│   │   ├── schemas/
│   │   │   └── classify.py    # Pydantic models for API responses
│   │   ├── templates/
│   │   │   └── home.html      # Web UI
│   │   ├── utils/
│   │   │   └── file_utils.py  # File handling utilities
│   │   ├── config.py          # Configuration settings
│   │   └── main.py            # FastAPI app initialization
│   └── checkpoint.txt         # Processing checkpoint
├── data/
│   ├── input/                 # Uploaded files
│   └── output/                # Processed results
├── tests/                     # Unit tests
├── .env                       # Environment variables
└── pyproject.toml            # Project dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd tweepy
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your Gemini API key
   echo "GEMINI_API_KEY=your_api_key_here" >> .env
   ```

## Usage

1. **Start the server**
   ```bash
   python -m uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open the web interface**
   Navigate to `http://localhost:8000` in your browser

3. **Process tweets**
   - Upload a JSON file containing tweet data
   - Click "Process & Download" to classify sentiments
   - Download the processed results

## API Endpoints

### Upload File
- **POST** `/api/v1/upload`
- Upload tweet data for processing
- Returns: `{filename, size, location}`

### Classify Tweets
- **GET** `/api/v1/classify?file_name={filename}`
- Processes uploaded file and returns classified results
- Returns: File download with sentiment classifications

## Data Format

Expected JSON structure for input files:
```json
[
  {
    "tweet": {
      "full_text": "This is an amazing product! I love it."
    }
  },
  {
    "tweet": {
      "full_text": "Really disappointed with the service."
    }
  }
]
```

## Configuration

Edit `src/app/config.py` to customize:
- `MAX_FILE_SIZE`: Maximum upload file size (default: 10MB)
- `ALLOWED_EXTENSIONS`: Permitted file types (default: .json, .js)
- `UPLOAD_DIR`: Directory for uploaded files
- `DOWNLOAD_DIR`: Directory for processed results

## Performance Features

- **Token-based Batching**: Optimizes API calls by respecting token limits (10,000 tokens per batch)
- **Checkpoint System**: Saves progress after each successful batch
- **Exponential Backoff**: Handles rate limiting with intelligent retry delays
- **Streaming Uploads**: Processes files in chunks to minimize memory usage

## Error Handling

- File size validation
- Filename sanitization to prevent directory traversal
- API error recovery with automatic retries
- Checkpoint-based resumption on failures

## Future Enhancements

- [ ] Support for multiple sentiment categories
- [ ] Batch processing metrics dashboard
- [ ] Multi-language support
- [ ] Custom classification prompts
- [ ] WebSocket for real-time progress updates

## License

MIT

## Support

For issues or questions, please open an issue in the repository.