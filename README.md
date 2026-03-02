# LLM Comparison Tool

A modern web application that sends the same query to Claude, ChatGPT, and Gemini simultaneously, displaying their responses side-by-side in a beautiful, responsive UI.

## Features

- 🤖 **Multi-LLM Support**: Compare responses from Claude, ChatGPT, and Gemini
- ⚡ **Parallel Requests**: Query all three LLMs at the same time
- 🎨 **Beautiful UI**: Clean, modern interface with responsive design
- 📱 **Mobile Friendly**: Works seamlessly on desktop, tablet, and mobile
- 🎯 **Real-time Status**: Loading indicators show when each response completes
- 🚀 **Fast**: Built with FastAPI for quick request handling

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: HTML, CSS, JavaScript
- **LLM APIs**: OpenAI, Anthropic (Claude), Google Gemini

## Installation

### Prerequisites
- Python 3.8+
- API keys for:
  - OpenAI (ChatGPT)
  - Anthropic (Claude)
  - Google (Gemini)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/siddheshmahadik24/llmcompare.git
cd llmcompare
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

Or set environment variables at the OS level.

## Running the App

```bash
python llm_comparison_app.py
```

The app will start at `http://localhost:8000`

## Usage

1. Open your browser and go to `http://localhost:8000`
2. Type your question in the text area
3. Click "Compare Responses" or press `Ctrl+Enter`
4. Watch as all three LLMs respond in parallel
5. Compare their answers side-by-side

## API Endpoints

### POST /api/query
Send a query to all three LLMs

**Request:**
```json
{
  "query": "Your question here"
}
```

**Response:**
```json
{
  "query": "Your question here",
  "claude": "Claude's response...",
  "chatgpt": "ChatGPT's response...",
  "gemini": "Gemini's response..."
}
```

## File Structure

```
.
├── llm_comparison_app.py      # FastAPI backend server
├── requirements.txt            # Python dependencies
├── .env                        # API keys (not in version control)
└── static/
    ├── index.html             # Main UI
    ├── style.css              # Styling
    └── script.js              # Frontend logic
```

## Configuration

You can modify the LLM models used by editing `llm_comparison_app.py`:

- **Claude**: `model="claude-opus-4-6"`
- **ChatGPT**: `model="gpt-4o-mini"`
- **Gemini**: `model="gemini-2.0-flash"`

## Troubleshooting

**API Key Issues:**
- Ensure your API keys are correctly set in `.env` or environment variables
- Check that you have active billing on your API accounts
- Verify API key permissions for each service

**Model Not Found Errors:**
- Update the model names in `llm_comparison_app.py` to match available models
- Check the API provider's documentation for current model names

## Future Enhancements

- [ ] Save comparison history
- [ ] Export results to PDF/JSON
- [ ] Custom model selection
- [ ] Cost estimation for each query
- [ ] Prompt templates
- [ ] Dark mode

## License

MIT License

## Author

Created by Siddhesh Mahadik (@siddheshmahadik24)
