<<<<<<< HEAD
# 🚀 AIDocMate - AI-Powered Document Simplification

> **Transform complex documents into simple, actionable insights with the power of AI**

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112.2-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 What is AIDocMate?

AIDocMate is an intelligent document processing platform that uses AI to:
- **Extract text** from PDFs and images using advanced OCR
- **Simplify complex documents** into easy-to-understand language
- **Generate actionable checklists** from any document
- **Translate content** into multiple languages
- **Explain legal/technical notices** in plain English

Perfect for students, professionals, and anyone who needs to understand complex documents quickly!

## ✨ Key Features

- 🔍 **Smart OCR**: Support for both Tesseract and Google Vision API
- 🤖 **AI-Powered Simplification**: Uses OpenAI to make complex text simple
- 📋 **Checklist Generation**: Automatically create actionable items from documents
- 🌍 **Multi-language Support**: Translate documents into various languages
- 📱 **Modern Web Interface**: Beautiful, responsive React frontend
- ⚡ **Fast API**: Built with FastAPI for high performance
- 🔒 **Secure**: Handles sensitive documents with proper security measures

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Python 3.13** - Latest Python features
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### AI Services
- **OpenAI API** - Text simplification and analysis
- **Google Cloud Vision** - Advanced OCR capabilities
- **Google Cloud Translate** - Multi-language support

### Frontend
- **React 18** - Modern UI framework
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Beautiful icons

### OCR & Processing
- **Tesseract** - Open-source OCR engine
- **Pillow** - Image processing
- **PyMuPDF** - PDF handling

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 16+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/aidocmate.git
cd aidocmate
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_APPLICATION_CREDENTIALS=path_to_google_credentials.json
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser and navigate to `http://localhost:8000`

## 📖 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative API Docs**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

### Main Endpoints

- `POST /upload` - Upload and extract text from documents
- `POST /simplify` - Simplify complex text
- `POST /translate` - Translate text to different languages
- `POST /checklist` - Generate actionable checklists
- `POST /explain` - Explain legal/technical notices

## 🎯 Use Cases

- **Students**: Simplify complex academic papers and textbooks
- **Professionals**: Break down legal documents and contracts
- **Researchers**: Extract key points from research papers
- **Business Users**: Understand complex reports and proposals
- **Language Learners**: Translate and simplify foreign language documents

## 🔧 Configuration

### OCR Settings
- **Tesseract**: Default OCR engine (free, offline)
- **Google Vision**: Premium OCR with better accuracy (requires API key)

### AI Models
- **OpenAI GPT**: For text simplification and analysis
- **Custom Prompts**: Easily customizable for specific use cases

## 🧪 Testing

Run the test suite:
```bash
pytest
```

## 📁 Project Structure

```
aidocmate/
├── app/                    # FastAPI application
│   ├── main.py           # Main application file
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
├── frontend/             # React application
│   ├── src/              # Source code
│   └── build/            # Production build
├── samples/              # Sample documents
├── tests/                # Test files
└── requirements.txt      # Python dependencies
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing powerful language models
- Google Cloud for OCR and translation services
- FastAPI team for the excellent web framework
- React team for the amazing frontend library

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/minakshi-bharti/aidocmate/issues)
- **Discussions**: [GitHub Discussions](https://github.com/minakshi-bharti/aidocmate/discussions)
- **Email**: minakshibharti30@gmail.com.com

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=minakshi-bharti/aidocmate&type=Date)](https://star-history.com/#minakshi-bharti/aidocmate&Date)

---

**Made with ❤️ for the hackathon community**

*Transform your documents, transform your understanding!* 
=======
# AIDocmate
AIDocMate is an AI-powered assistant that simplifies government and legal documents. Built with qRaptor, it explains forms in simple language, guides step-by-step form filling, generates document checklists, suggests eligible schemes, and ensures privacy—empowering citizens to complete processes independently.
>>>>>>> 0c8dcfebf0074d0e6fd9d195b2ca1dccf3982133
