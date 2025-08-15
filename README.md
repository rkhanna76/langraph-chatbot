# LangGraph Chatbot

A modular, production-ready chatbot implementation using LangGraph and OpenAI GPT-4 with web search capabilities and comprehensive monitoring.

## ✨ Features

- **🏗️ Modular Architecture**: Clean separation of concerns with dedicated modules
- **🔧 LangGraph Integration**: Uses LangGraph for conversation flow management
- **🤖 OpenAI GPT-4**: Powered by OpenAI's latest language model
- **🔍 Web Search**: Integrated Tavily search for real-time information
- **📊 Graph Visualization**: Generates visual representations in multiple formats
- **💬 Interactive Mode**: Rich command-line interface with emojis and formatting
- **📝 Comprehensive Logging**: Built-in logging system for debugging and monitoring
- **🏥 Health Checks**: Built-in health monitoring and diagnostics
- **⚙️ Configuration Management**: Centralized configuration with validation
- **🧪 Testing Support**: Built-in test suite for validation
- **🔍 LangSmith Monitoring**: Real-time flow monitoring and tracing
- **📈 Performance Analytics**: Detailed performance metrics and analysis

## 🏗️ Architecture

The chatbot is built with a modular architecture:

```
basic_chatbot/
├── chatbot.py              # Main entry point
├── chatbot_core.py         # Core chatbot implementation
├── config.py               # Configuration management
├── graph_builder.py        # LangGraph construction
├── visualization.py        # Graph visualization handling
├── chat_interface.py       # User interface management
├── state.py                # State definitions
├── logger.py               # Logging system
├── langsmith_integration.py # LangSmith monitoring
├── monitor_flow.py         # Flow monitoring demo
├── test_chatbot.py         # Test suite
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🚀 Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd basic_chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API keys**:
   
   Create a `.env` file in the project root:
   ```bash
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   echo "TAVILY_API_KEY=your-tavily-api-key-here" >> .env
   echo "LANGSMITH_API_KEY=your-langsmith-api-key-here" >> .env
   ```
   
   Or set them as environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   export TAVILY_API_KEY="your-tavily-api-key-here"
   export LANGSMITH_API_KEY="your-langsmith-api-key-here"
   ```

   **Note**: You'll need these API keys:
   - [OpenAI API key](https://platform.openai.com/api-keys) for GPT-4 access
   - [Tavily API key](https://tavily.com/) for web search functionality
   - [LangSmith API key](https://smith.langchain.com/) for monitoring and tracing

## 🎯 Usage

### Basic Usage

Run the chatbot:
```bash
python chatbot.py
```

The chatbot will:
1. ✅ Load and validate configuration
2. 🏥 Perform health checks
3. 📊 Generate graph visualizations
4. 🔗 Start LangSmith monitoring session
5. 🤖 Start an interactive chat session
6. 🔍 Automatically use web search when needed

### Flow Monitoring with LangSmith

Monitor the conversation flow in real-time:
```bash
python monitor_flow.py
```

This will:
- Start a monitored session
- Process test queries
- Show LangSmith project URL
- Demonstrate monitoring features

### Testing

Run the test suite to verify everything works:
```bash
python test_chatbot.py
```

### Interactive Commands

- Type your message and press Enter
- Use `quit`, `exit`, or 'q' to end the session
- Use `Ctrl+C` to interrupt the session

### Graph Visualizations

The chatbot generates visualizations in multiple formats:
- `langgraph_visualization.png` - PNG image of the conversation graph
- `langgraph_visualization.mmd` - Mermaid diagram code (view at [mermaid.live](https://mermaid.live/))
- `langgraph_visualization.svg` - SVG vector format

### Web Search Integration

The chatbot now includes:
- **Tavily Search**: Real-time web search capabilities
- **Automatic Tool Usage**: The LLM decides when to use web search
- **Enhanced Responses**: More accurate and up-to-date information

## 🔍 LangSmith Monitoring

LangSmith provides comprehensive monitoring and tracing:

### Features
- **🔍 Node Execution Tracking**: Monitor chatbot and tools node execution
- **🛠️ Tool Usage Monitoring**: Track which tools are called and their results
- **💬 Conversation Tracking**: Complete conversation history and analysis
- **📊 Performance Analytics**: Execution time, success rates, and metrics
- **🔗 Real-time Monitoring**: Live monitoring of conversation flows

### Setup
1. Get your LangSmith API key from [smith.langchain.com](https://smith.langchain.com/)
2. Add it to your `.env` file: `LANGSMITH_API_KEY=your-key`
3. Run the monitoring demo: `python monitor_flow.py`

### What You Can Monitor
- **Node Execution**: See exactly what happens in chatbot and tools nodes
- **Input/Output**: Track all inputs and outputs for each step
- **Tool Calls**: Monitor when and how tools are used
- **Performance**: Track execution time and success rates
- **Errors**: Debug issues with detailed error tracking
- **Flow Visualization**: See the complete conversation flow

### Accessing Monitoring Data
- **Web Dashboard**: Visit your LangSmith project URL
- **API Access**: Use LangSmith API for custom dashboards
- **Export**: Export data for analysis

## 🔧 Configuration

The chatbot uses a centralized configuration system:

```python
from config import ChatbotConfig

# Load from environment
config = ChatbotConfig.from_env()

# Customize settings
config.max_conversation_turns = 100
config.enable_web_search = True
config.enable_langsmith = True
config.langsmith_project = "my-chatbot-project"
```

## 📊 Logging

Built-in logging system for monitoring and debugging:

```python
from logger import get_logger

logger = get_logger("MyModule")
logger.info("Operation completed successfully")
logger.error("Something went wrong")
```

## 🏥 Health Monitoring

Built-in health checks for system monitoring:

```python
health = chatbot.health_check()
print(f"Status: {health['status']}")
print(f"LangSmith Enabled: {health['langsmith_enabled']}")
print(f"Errors: {health['errors']}")
```

## 🧪 Testing

Comprehensive test suite included:

```bash
# Run all tests
python test_chatbot.py

# Test specific components
python -c "from test_chatbot import test_configuration; test_configuration()"
```

## 🔒 Security Notes

- **Never commit your `.env` file** - it's already in `.gitignore`
- **Keep your API keys secure** - don't share them publicly
- **Use environment variables** in production environments
- **Validate configuration** before running

## 📦 Dependencies

- `langchain` - LangChain framework for LLM interactions
- `langgraph` - LangGraph for conversation flow management
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable loading
- `graphviz` - Graph visualization (optional, for PNG generation)
- `langchain_tavily` - Tavily search integration
- `tavily-python` - Tavily API client
- `langsmith` - LangSmith monitoring and tracing

## 🚨 Troubleshooting

### "python-dotenv not installed"
```bash
pip install python-dotenv
```

### "OpenAI API key not found"
- Check that your `.env` file exists and contains `OPENAI_API_KEY=your-key`
- Or set the environment variable manually

### "Tavily API key not found"
- Check that your `.env` file contains `TAVILY_API_KEY=your-key`
- Get a free API key from [tavily.com](https://tavily.com/)

### "LangSmith API key not found"
- Check that your `.env` file contains `LANGSMITH_API_KEY=your-key`
- Get a free API key from [smith.langchain.com](https://smith.langchain.com/)

### Graph visualization errors
- Install Graphviz: `brew install graphviz` (macOS) or `apt-get install graphviz` (Ubuntu)
- The chatbot will still work without visualization support

### Module import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that all Python files are in the same directory

## 🎨 Customization

The modular architecture makes it easy to customize:

```python
# Custom chat interface
from chat_interface import ChatInterface

class MyChatInterface(ChatInterface):
    def _get_default_welcome(self):
        return "Welcome to my custom chatbot!"

# Custom visualization formats
from visualization import GraphVisualizer

visualizer = GraphVisualizer(formats=["png", "svg"])

# Custom monitoring
from langsmith_integration import LangSmithMonitor

monitor = LangSmithMonitor(config)
monitor.log_custom_event("my_event", {"data": "value"})
```

## 📈 Performance

- **Lazy Loading**: Components are initialized only when needed
- **Error Recovery**: Graceful fallbacks when components fail
- **Resource Management**: Automatic cleanup of old visualizations
- **Health Monitoring**: Continuous system health checks
- **Performance Tracking**: Detailed metrics via LangSmith

## 🤝 Contributing

The modular structure makes it easy to contribute:

1. **Add new modules** in separate files
2. **Extend existing classes** through inheritance
3. **Add new visualization formats** in `visualization.py`
4. **Create new chat interfaces** in `chat_interface.py`
5. **Add monitoring features** in `langsmith_integration.py`

## 📄 License

This project is for educational purposes. Please respect OpenAI's, Tavily's, and LangSmith's terms of service.

## 🔮 Future Enhancements

- **Web Interface**: Add Flask/FastAPI web server
- **Database Integration**: Store conversation history
- **Multi-modal Support**: Image and audio processing
- **Plugin System**: Extensible tool architecture
- **Advanced Monitoring**: Custom dashboards and alerts
- **A/B Testing**: Compare different conversation flows
