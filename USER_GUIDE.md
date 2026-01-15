# 📘 Company Internal Chatbot - User Guide

## 🎯 Overview

The Company Internal Chatbot is a secure, AI-powered assistant that provides role-based access to company documents and information. Each user can only access information relevant to their role and department.

---

## 🚀 Getting Started

### Accessing the Chatbot

1. **Open the application** in your web browser: `http://localhost:8501`
2. **Login** with your company credentials
3. **Start chatting** with the AI assistant

### System Requirements

- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection
- Valid company credentials

---

## 🔐 User Roles & Access Levels

### 1️⃣ Admin Role

**Access Level:** Full access to all company documents

**Available Information:**
- ✅ Engineering documentation
- ✅ Financial reports and summaries
- ✅ Marketing reports and campaigns
- ✅ HR data and employee information
- ✅ General company policies

**Sample Queries:**
```
"What are the technical architecture components?"
"Show me the Q4 2024 financial results"
"What were the marketing campaign results?"
"How many employees are in the Bangalore office?"
"What is the company's remote work policy?"
```

**Best Practices:**
- Use admin access responsibly
- Only access data necessary for your tasks
- All queries are logged in the audit trail

---

### 2️⃣ Finance Role

**Access Level:** Financial documents and general policies

**Available Information:**
- ✅ Financial reports (quarterly, annual)
- ✅ Budget summaries
- ✅ Financial analysis documents
- ✅ General company policies
- ❌ Engineering, Marketing, HR data

**Sample Queries:**
```
"What were the Q4 2024 financial results?"
"Show me the quarterly financial summary"
"What is the annual revenue for 2024?"
"What are the company expense categories?"
"What is the remote work policy?"
```

**Tips:**
- Ask specific questions about financial metrics
- Reference time periods (Q1, Q2, 2024, etc.)
- Queries return data with confidence scores

---

### 3️⃣ Marketing Role

**Access Level:** Marketing documents and general policies

**Available Information:**
- ✅ Marketing reports (Q1-Q4 2024)
- ✅ Campaign performance data
- ✅ Market analysis reports
- ✅ General company policies
- ❌ Engineering, Finance, HR data

**Sample Queries:**
```
"What were the Q4 2024 marketing highlights?"
"Show me the digital marketing campaign results"
"What are the key market trends?"
"What was the customer engagement rate?"
"What is the company's social media policy?"
```

**Tips:**
- Ask about specific campaigns or quarters
- Request performance metrics and KPIs
- Sources are cited for all responses

---

### 4️⃣ Engineering Role

**Access Level:** Engineering documentation and general policies

**Available Information:**
- ✅ Technical architecture documentation
- ✅ System design documents
- ✅ Engineering specifications
- ✅ General company policies
- ❌ Finance, Marketing, HR data

**Sample Queries:**
```
"What are the main technical components?"
"Describe the system architecture"
"What technologies are used in the RAG pipeline?"
"How does the vector database work?"
"What is the code review policy?"
```

**Tips:**
- Ask technical questions about architecture
- Request information about specific components
- Technical terms are understood by the AI

---

### 5️⃣ HR (Human Resources) Role

**Access Level:** HR data and general policies

**Available Information:**
- ✅ Employee information and data
- ✅ HR reports and statistics
- ✅ Department information
- ✅ General company policies
- ❌ Engineering, Finance, Marketing data

**Sample Queries:**
```
"How many employees work in the Finance department?"
"What is the average salary in Engineering?"
"Show me employee information for employee ID FINEMP1005"
"What are the employee benefits?"
"What is the leave policy?"
```

**Tips:**
- Ask about employee statistics and demographics
- Reference specific employee IDs if needed
- All HR queries are audit-logged for compliance

---

### 6️⃣ Employee Role

**Access Level:** General company policies only

**Available Information:**
- ✅ General company policies
- ✅ Employee handbook information
- ✅ Company-wide announcements
- ❌ Department-specific data
- ❌ Confidential information

**Sample Queries:**
```
"What is the remote work policy?"
"What are the company holidays?"
"How do I submit a leave request?"
"What are the employee benefits?"
"What is the dress code policy?"
```

**Tips:**
- Focus on general policy questions
- Ask about benefits and procedures
- For department-specific questions, contact your manager

---

## 💬 Using the Chat Interface

### 1. Login Page

1. **Select a user** from the dropdown (or enter credentials manually)
2. **Password is auto-filled** for demo users
3. **Click "Login"** to authenticate
4. Wait for the **green "Backend Connected"** indicator

### 2. Chat Interface

**Key Elements:**
- 👤 **User Profile**: Shows your name, role, and department
- 💬 **Chat History**: All your previous messages and responses
- 📝 **Input Box**: Type your questions here
- 📤 **Send Button**: Submit your query

**Understanding Responses:**

Each response includes:
- **Answer**: AI-generated response to your query
- **Confidence Level**: 
  - 🟢 VERY_HIGH (90-100%)
  - 🟡 HIGH (70-89%)
  - 🟠 MEDIUM (50-69%)
  - 🔴 LOW (0-49%)
- **Sources**: Documents used to generate the answer

### 3. Viewing Sources

Click **"📚 View Sources"** to see:
- **Document Name**: Which file the information came from
- **Section**: Specific section of the document
- **Relevance Score**: How relevant the source is (0-100%)
- **Quality Rating**: 
  - 🟢 Highly Relevant
  - 🟡 Relevant
  - 🟠 Somewhat Relevant
  - 🔴 Marginally Relevant

---

## ✅ Best Practices

### Writing Effective Queries

**DO:**
- ✅ Be specific and clear
- ✅ Use complete sentences
- ✅ Reference time periods if relevant
- ✅ Ask one question at a time

**DON'T:**
- ❌ Ask vague or overly broad questions
- ❌ Request information outside your role
- ❌ Use overly technical jargon (unless in Engineering role)
- ❌ Ask multiple unrelated questions at once

### Example Good Queries

| ❌ Poor Query | ✅ Good Query |
|--------------|--------------|
| "Sales?" | "What were the Q4 2024 sales figures?" |
| "Tell me everything about marketing" | "What were the key highlights from the Q4 2024 marketing report?" |
| "Employees" | "How many employees are in the Engineering department?" |
| "Money" | "What was the quarterly revenue for Q3 2024?" |

---

## 🔒 Security & Privacy

### Data Security
- All queries are encrypted using JWT tokens
- Passwords are hashed with bcrypt
- Session tokens expire after 60 minutes

### Audit Logging
- Every query is logged with:
  - Username and role
  - Query text
  - Timestamp
  - Documents accessed

### Privacy Considerations
- Only access data relevant to your role
- Do not share your login credentials
- Log out when finished
- Report suspicious activity to IT

---

## ❓ Troubleshooting

### Common Issues

**Issue: "Backend server is not running"**
- **Solution**: Contact IT support - the backend server needs to be started

**Issue: "No documents found for this query"**
- **Solution**: 
  - Rephrase your question
  - Ensure you're asking about data accessible to your role
  - Try a more specific query

**Issue: "Token expired" or "Unauthorized"**
- **Solution**: Click "Logout" and login again

**Issue: Low confidence responses**
- **Solution**:
  - Review the sources provided
  - Rephrase your query to be more specific
  - Check if the information exists in your accessible documents

---

## 📞 Support

### Getting Help

- **IT Support**: Contact your IT department for technical issues
- **HR Department**: Contact HR for access and permission questions
- **Feedback**: Use the feedback form to report issues or suggest improvements

### Reporting Issues

When reporting an issue, include:
1. Your username (not password!)
2. The query you attempted
3. Error message received
4. Screenshots (if applicable)

---

## 🎓 Quick Reference Card

### Sample Credentials (Demo)

| Username | Password | Role | Access Level |
|----------|----------|------|--------------|
| admin | admin123 | Admin | Full Access |
| john_finance | finance123 | Finance | Finance + General |
| jane_marketing | marketing123 | Marketing | Marketing + General |
| bob_engineering | engineering123 | Engineering | Engineering + General |
| alice_hr | hr123 | HR | HR + General |
| employee | employee123 | Employee | General Only |

### Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: New line in message
- **Ctrl + L**: Focus on input box

### Status Indicators

- 🟢 **Backend Connected**: System is ready
- 🔴 **Backend Disconnected**: Contact IT support
- 🟡 **Processing**: AI is generating response

---

## 📝 Version Information

- **Application**: Company Internal Chatbot v1.0
- **AI Model**: Mistral 7B
- **Vector Database**: ChromaDB
- **Authentication**: JWT + Bcrypt
- **Frontend**: Streamlit
- **Backend**: FastAPI

---

## 📄 Document Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | January 2026 | Initial release |

---

*For technical documentation, see [README.md](README.md)*  
*For backend API documentation, see [backend/QUICKSTART.md](backend/QUICKSTART.md)*
