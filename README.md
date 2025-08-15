# LangGraph Chatbot

A sophisticated chatbot built with LangGraph, featuring conditional flow monitoring, web search capabilities, LangSmith integration, and both command-line and web interfaces.

## 🌟 Features

- **🤖 Intelligent Chatbot**: Powered by OpenAI GPT-4 with current date awareness
- **🔍 Web Search Integration**: Real-time information retrieval using Tavily
- **📊 LangSmith Monitoring**: Complete flow tracing and performance monitoring
- **🔄 Conditional Flow**: LLM decides when to use tools vs direct responses
- **💾 Checkpointing**: Conversation state persistence across sessions
- **🌐 Web Interface**: Modern, responsive web UI built with Flask
- **💻 Command Line**: Traditional interactive command-line interface
- **📅 Current Date Awareness**: Always uses actual current date, not training date

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Tavily API key (optional, for web search)
- LangSmith API key (optional, for monitoring)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd basic_chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   echo "TAVILY_API_KEY=your-tavily-api-key-here" >> .env
   echo "LANGSMITH_API_KEY=your-langsmith-api-key-here" >> .env
   ```

## 🎯 Usage

### Web Interface (Recommended)

Start the web UI for a modern chat experience:

```bash
# Option 1: Use the launcher (recommended)
python start_web_ui.py

# Option 2: Direct start
python web_ui.py
```

Then open your browser to: **http://localhost:5000**

**Web UI Features:**
- 🎨 Modern, responsive design
- ⚡ Real-time chat interface
- 📱 Mobile-friendly
- 🔄 Typing indicators
- ⏱️ Response time tracking
- 🟢 Health status indicator

### Command Line Interface

For traditional terminal interaction:

```bash
python chatbot.py
```

**CLI Features:**
- 🔄 Interactive conversation
- 📊 Health checks
- 🖼️ Graph visualization generation
- 📝 Session management

### API Endpoints

The web server provides REST API endpoints:

- `GET /api/health` - Health check
- `POST /api/chat` - Send chat message
- `GET /` - Web interface

## 🏗️ Architecture

### Core Components

```
📁 Project Structure
├── chatbot.py              # Main CLI entry point
├── web_ui.py              # Flask web server
├── chatbot_core.py        # Core chatbot logic
├── graph_builder.py       # LangGraph construction
├── config.py              # Configuration management
├── state.py               # State definitions
├── visualization.py       # Graph visualization
├── chat_interface.py      # Chat interface logic
├── logger.py              # Logging system
├── langsmith_integration.py # LangSmith monitoring
├── templates/
│   └── chat.html          # Web UI template
└── requirements.txt       # Dependencies
```

### Flow Architecture

```
START → chatbot → (conditional) → tools → chatbot → END
                    ↓
                  (end)
```

**Conditional Flow:**
- LLM decides when to use tools
- Web search only when needed
- Proper conversation termination
- No infinite loops

### Monitoring & Observability

- **LangSmith Integration**: Complete flow tracing
- **Health Checks**: System diagnostics
- **Performance Metrics**: Response time tracking
- **Error Handling**: Graceful error recovery

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | ✅ Yes |
| `TAVILY_API_KEY` | Tavily search API key | ❌ No (disables web search) |
| `LANGSMITH_API_KEY` | LangSmith API key | ❌ No (disables monitoring) |

### Configuration Options

```python
# config.py
model_name: str = "gpt-4"              # OpenAI model
max_search_results: int = 3            # Web search results
enable_web_search: bool = True         # Enable/disable web search
enable_langsmith: bool = True          # Enable/disable monitoring
```

## 📊 Monitoring

### LangSmith Dashboard

Access your monitoring dashboard at: **https://smith.langchain.com**

**Features:**
- 🔍 Node execution tracking
- 🛠️ Tool usage monitoring
- 💬 Conversation history
- 📈 Performance metrics
- 🐛 Error debugging

### Health Checks

```bash
# CLI health check
python -c "from chatbot_core import LangGraphChatbot; print(LangGraphChatbot().health_check())"

# Web API health check
curl http://localhost:5000/api/health
```

## 🧪 Testing

### Quick Tests

```bash
# Test current date awareness
python -c "from chatbot_core import LangGraphChatbot; chatbot = LangGraphChatbot(); chatbot.stream_response('What is today\'s date?')"

# Test web search
python -c "from chatbot_core import LangGraphChatbot; chatbot = LangGraphChatbot(); chatbot.stream_response('What is the latest news about AI?')"

# Test conversation continuity
python monitor_flow.py
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**
   ```bash
   # Check .env file
   cat .env
   ```

3. **Port Already in Use**
   ```bash
   # Change port in web_ui.py
   app.run(port=5001)
   ```

4. **LangSmith 403 Errors**
   - Use placeholder key for testing
   - Get real key from LangSmith dashboard

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python chatbot.py
```

## 🚀 Advanced Usage

### Custom Graph Modifications

```python
# Modify graph_builder.py
def _construct_graph(self):
    # Add custom nodes
    # Modify flow logic
    pass
```

### Adding New Tools

```python
# In graph_builder.py
def _init_tools(self):
    # Add custom tools
    custom_tool = Tool(
        name="custom_tool",
        description="Custom tool description",
        func=custom_function
    )
    self.tools.append(custom_tool)
```

### Custom Monitoring

```python
# In langsmith_integration.py
def log_custom_event(self, event_type, data):
    # Add custom monitoring
    pass
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔮 Future Enhancements

- [ ] Multi-user support
- [ ] Conversation export
- [ ] Custom tool integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app
- [ ] Voice interface
- [ ] Multi-language support

---

**Built with ❤️ using LangGraph, OpenAI, and Flask**
