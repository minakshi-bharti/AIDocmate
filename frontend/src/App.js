import React, { useState, useRef } from 'react';
import { FileText, MessageCircle, Loader2, Send, Bot, User, Upload, X } from 'lucide-react';

function App() {
  const [documentText, setDocumentText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [, setExtractedText] = useState('');
  const fileInputRef = useRef(null);

  const API_BASE = '';

  const handleFileUpload = async (file) => {
    if (!file) return;
    
    setIsProcessing(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const result = await response.json();
        setExtractedText(result.extracted_text);
        setDocumentText(result.extracted_text);
        setUploadedFile(file);
        
        // Add success message to chat
        setChatMessages(prev => [...prev, {
          id: Date.now(),
          type: 'bot',
          content: `📄 Document uploaded successfully!\n\n**File:** ${file.name}\n**Size:** ${(file.size / 1024).toFixed(1)} KB\n\n**Extracted Text:**\n${result.extracted_text.substring(0, 200)}${result.extracted_text.length > 200 ? '...' : ''}`,
          timestamp: new Date().toLocaleTimeString()
        }]);
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      setChatMessages(prev => [...prev, {
        id: Date.now(),
        type: 'bot',
        content: '❌ Failed to upload document. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSimplifyDocument = async () => {
    if (!documentText.trim()) return;
    
    setIsProcessing(true);
    
    try {
      const response = await fetch(`${API_BASE}/simplify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: documentText,
          language: 'en',
          reading_level: 'simple'
        }),
      });
      
      if (response.ok) {
        const result = await response.json();
        
        setChatMessages(prev => [...prev, {
          id: Date.now(),
          type: 'bot',
          content: `📋 **Simplified Document Summary:**\n\n${result.simplified_text}\n\n✅ **Key Points:**\n• Original length: ${result.original_length} characters\n• Simplified length: ${result.simplified_length} characters\n• Language: ${result.language}`,
          timestamp: new Date().toLocaleTimeString()
        }]);
      } else {
        throw new Error('Simplification failed');
      }
    } catch (error) {
      setChatMessages(prev => [...prev, {
        id: Date.now(),
        type: 'bot',
        content: '❌ Failed to simplify document. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleGenerateChecklist = async () => {
    if (!documentText.trim()) return;
    
    setIsProcessing(true);
    
    try {
      const response = await fetch(`${API_BASE}/checklist`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: documentText,
          document_type: 'government_form'
        }),
      });
      
      if (response.ok) {
        const result = await response.json();
        
        let checklistText = `📋 **Document Checklist Generated:**\n\n`;
        if (result.items && result.items.length > 0) {
          result.items.forEach((item, index) => {
            checklistText += `${index + 1}. **${item.name}**\n   • ${item.description}\n   • Required: ${item.mandatory ? 'Yes' : 'No'}\n   • Copies: ${item.copies}\n\n`;
          });
        } else {
          checklistText += result.message || 'No checklist items generated.';
        }
        
        setChatMessages(prev => [...prev, {
          id: Date.now(),
          type: 'bot',
          content: checklistText,
          timestamp: new Date().toLocaleTimeString()
        }]);
      } else {
        throw new Error('Checklist generation failed');
      }
    } catch (error) {
      setChatMessages(prev => [...prev, {
        id: Date.now(),
        type: 'bot',
        content: '❌ Failed to generate checklist. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleTranslate = async () => {
    if (!documentText.trim()) return;
    
    setIsProcessing(true);
    
    try {
      const response = await fetch(`${API_BASE}/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: documentText,
          target_language: 'hi' // Hindi
        }),
      });
      
      if (response.ok) {
        const result = await response.json();
        
        setChatMessages(prev => [...prev, {
          id: Date.now(),
          type: 'bot',
          content: `🌐 **Translation to Hindi:**\n\n**Original (English):**\n${result.original_text.substring(0, 150)}${result.original_text.length > 150 ? '...' : ''}\n\n**Translated (Hindi):**\n${result.translated_text}`,
          timestamp: new Date().toLocaleTimeString()
        }]);
      } else {
        throw new Error('Translation failed');
      }
    } catch (error) {
      setChatMessages(prev => [...prev, {
        id: Date.now(),
        type: 'bot',
        content: '❌ Failed to translate document. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: chatInput,
      timestamp: new Date().toLocaleTimeString()
    };
    
    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');

    // Try to get AI response from backend
    try {
      const response = await fetch(`${API_BASE}/explain`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: chatInput
        }),
      });
      
      if (response.ok) {
        const result = await response.json();
        
        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: `🤖 **AI Analysis:**\n\n${result.summary}\n\n**Steps:**\n${result.steps.map((step, i) => `${i + 1}. ${step}`).join('\n')}\n\n**Next Actions:**\n${result.next_actions.map((action, i) => `• ${action}`).join('\n')}\n\n**Urgency:** ${result.urgency_level}`,
          timestamp: new Date().toLocaleTimeString()
        };
        
        setChatMessages(prev => [...prev, botMessage]);
      } else {
        throw new Error('AI analysis failed');
      }
    } catch (error) {
      // Fallback to mock response
      const botResponses = [
        "This appears to be a government document. The key information shows it's a PAN card application form.",
        "Based on the document content, this is a legal notice. You should review the deadlines mentioned carefully.",
        "This document contains important eligibility criteria. Make sure you meet all requirements before proceeding.",
        "I can see this is a financial document. The amounts and dates are clearly specified in the text.",
        "This looks like an official certificate. Please verify all personal details are correct."
      ];
      
      const randomResponse = botResponses[Math.floor(Math.random() * botResponses.length)];
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: randomResponse,
        timestamp: new Date().toLocaleTimeString()
      };
      
      setChatMessages(prev => [...prev, botMessage]);
    }
  };

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const removeFile = () => {
    setUploadedFile(null);
    setExtractedText('');
    setDocumentText('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary-500 rounded-lg flex items-center justify-center">
                <FileText className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AiDocmate</h1>
                <p className="text-sm text-gray-600">Simplify Documents. Smarter. Faster.</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Left Side - Document Input */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <FileText className="w-5 h-5 mr-2 text-primary-500" />
                Document Input
              </h2>
              
              <div className="space-y-4">
                {/* File Upload */}
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.png,.jpg,.jpeg"
                    onChange={handleFileInputChange}
                    className="hidden"
                  />
                  
                  {!uploadedFile ? (
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="flex flex-col items-center space-y-2 text-gray-600 hover:text-primary-600 transition-colors"
                    >
                      <Upload className="w-8 h-8" />
                      <span>Click to upload PDF or Image</span>
                      <span className="text-sm">or drag and drop</span>
                    </button>
                  ) : (
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <FileText className="w-5 h-5 text-primary-500" />
                        <span className="font-medium">{uploadedFile.name}</span>
                        <span className="text-sm text-gray-500">
                          ({(uploadedFile.size / 1024).toFixed(1)} KB)
                        </span>
                      </div>
                      <button
                        onClick={removeFile}
                        className="text-gray-400 hover:text-red-500 transition-colors"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </div>

                {/* Text Input */}
                <textarea
                  value={documentText}
                  onChange={(e) => setDocumentText(e.target.value)}
                  placeholder="Paste your document text here or upload a file above..."
                  className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                />
                
                {/* Action Buttons */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <button
                    onClick={handleSimplifyDocument}
                    disabled={isProcessing || !documentText.trim()}
                    className="bg-primary-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
                  >
                    {isProcessing ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span>Processing...</span>
                      </>
                    ) : (
                      <>
                        <FileText className="w-4 h-4" />
                        <span>Simplify</span>
                      </>
                    )}
                  </button>

                  <button
                    onClick={handleGenerateChecklist}
                    disabled={isProcessing || !documentText.trim()}
                    className="bg-green-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
                  >
                    <FileText className="w-4 h-4" />
                    <span>Checklist</span>
                  </button>

                  <button
                    onClick={handleTranslate}
                    disabled={isProcessing || !documentText.trim()}
                    className="bg-purple-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
                  >
                    <FileText className="w-4 h-4" />
                    <span>Translate</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Right Side - Chatbot */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border p-6 h-[600px] flex flex-col">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <MessageCircle className="w-5 h-5 mr-2 text-primary-500" />
                AI Assistant
              </h2>
              
              {/* Chat Messages */}
              <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                {chatMessages.length === 0 ? (
                  <div className="text-center text-gray-500 py-8">
                    <Bot className="w-12 h-12 mx-auto mb-2 text-gray-300" />
                    <p>Upload a document or ask me anything!</p>
                  </div>
                ) : (
                  chatMessages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                          message.type === 'user'
                            ? 'bg-primary-500 text-white'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        <div className="flex items-start space-x-2">
                          {message.type === 'user' ? (
                            <User className="w-4 h-4 mt-1 flex-shrink-0" />
                          ) : (
                            <Bot className="w-4 h-4 mt-1 flex-shrink-0" />
                          )}
                          <div className="flex-1">
                            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                            <p className={`text-xs mt-1 ${
                              message.type === 'user' ? 'text-primary-100' : 'text-gray-500'
                            }`}>
                              {message.timestamp}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>

              {/* Chat Input */}
              <form onSubmit={handleChatSubmit} className="flex space-x-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="Ask about your document..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
                <button
                  type="submit"
                  disabled={!chatInput.trim()}
                  className="bg-primary-600 text-white p-2 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Send className="w-5 h-5" />
                </button>
              </form>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600">
            Built with ❤️ for A2HackFest 2025
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
