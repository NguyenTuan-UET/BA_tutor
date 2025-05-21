const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');
const fs = require('fs');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// Load env
const envPath = path.join(__dirname, '../core/.env');
dotenv.config({ path: envPath });

const app = express();
app.use(cors());
app.use(express.json());

const GEMINI_API_KEY = process.env.GOOGLE_API_KEY || process.env.GEMINI_API_KEY;
const SYSTEM_PROMPT =
  process.env.SYSTEM_PROMPT ||
  'Bạn là một trợ lý AI được huấn luyện để đóng vai trò cố vấn học tập của khoa Tài chính, Học viện Ngân hàng Việt Nam...';

// Gemini API setup
const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

// Simple health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', time: new Date() });
});

// Chat endpoint
app.post('/api/ask', async (req, res) => {
  const { question, docs } = req.body;
  if (!question) return res.status(400).json({ error: 'Missing question' });

  // Compose prompt
  let prompt = SYSTEM_PROMPT;
  if (docs) {
    prompt += `\n--------------------\nDưới đây là tài liệu hiện tại:\n${docs}\n--------------------`;
  }
  prompt += '\n' + question;

  try {
    const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });
    const result = await model.generateContent(prompt);
    res.json({ answer: result.response.text });
  } catch (err) {
    res.status(500).json({ error: err.message || 'Gemini API error' });
  }
});

// Start server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Backend Gemini API server running at http://localhost:${PORT}`);
});
