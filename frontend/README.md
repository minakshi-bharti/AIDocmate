# AiDocmate Frontend

A modern, responsive React + Tailwind CSS frontend for the AiDocmate document simplification application.

## Features

- 🎨 **Clean, Modern Design** - Built with Tailwind CSS for a professional look
- 📱 **Fully Responsive** - Works perfectly on desktop, tablet, and mobile
- 📄 **Document Input** - Large textarea for pasting document content
- 🤖 **AI Chatbot Interface** - Interactive chat with mock AI responses
- ⚡ **Loading States** - Smooth loading animations and user feedback
- 🎯 **Mock Functionality** - Ready for demo videos with simulated AI responses

## Quick Start

### Prerequisites
- Node.js 16+ and npm

### Installation
```bash
cd frontend
npm install
```

### Development
```bash
npm start
```
Open [http://localhost:3000](http://localhost:3000) to view the app.

### Build for Production
```bash
npm run build
```

## Demo Features

### Document Simplification
1. Paste any text in the left textarea
2. Click "Simplify Document" button
3. See a loading spinner for 2 seconds
4. Get an automatic simplified summary in the chat

### AI Chatbot
1. Type questions in the chat input
2. Get instant mock responses about documents
3. Responses include timestamps and user/bot indicators
4. Random selection from 5 different mock responses

### Mock Responses Include:
- Government document analysis
- Legal notice explanations
- Eligibility criteria insights
- Financial document summaries
- Official certificate verification

## Tech Stack

- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful, customizable icons
- **Responsive Design** - Mobile-first approach

## File Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── App.js          # Main application component
│   ├── index.js        # React entry point
│   └── index.css       # Global styles + Tailwind
├── package.json
├── tailwind.config.js  # Tailwind configuration
└── postcss.config.js   # PostCSS configuration
```

## Customization

### Colors
Modify `tailwind.config.js` to change the primary color scheme:
```js
colors: {
  primary: {
    500: '#3b82f6', // Change this for main brand color
    600: '#2563eb',
    700: '#1d4ed8',
  }
}
```

### Mock Responses
Edit the `botResponses` array in `App.js` to customize AI responses for your demo.

## Demo Video Tips

1. **Start with empty state** - Show the clean interface
2. **Paste sample text** - Use government forms or legal documents
3. **Click Simplify** - Demonstrate the loading state
4. **Show chat interaction** - Ask questions about the document
5. **Highlight responsiveness** - Resize browser window

## Backend Integration

When ready to connect to the FastAPI backend:
1. Replace mock API calls with real fetch requests
2. Update endpoints to match your backend URLs
3. Handle real API responses and errors
4. Add proper authentication if needed

## License

Built for A2HackFest 2025
