__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from crew import create_crew

st.set_page_config(layout="wide", page_title="Stock Analysis Agent", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .reportview-container { background: white; }
    .sidebar .sidebar-content { background: white; }
    .big-font { font-size:30px !important; font-weight: bold; color: #1E3A8A; }
    .medium-font { font-size:20px !important; font-weight: bold; color: #1E3A8A; }
    .small-font { font-size:14px !important; }
    .analysis-card { background-color: black; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    .analysis-title { font-size: 18px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
    .analysis-content { font-size: 14px; color: #FFFFFF; line-height: 1.6; }
    .analysis-list { padding-left: 20px; }
    .analysis-list-item { margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Stock Analysis Agent</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="medium-font">Configuration</p>', unsafe_allow_html=True)

# Açıklama
st.markdown("""
<div class="analysis-card">
    <h2 class="analysis-title">Advanced AI-Powered Stock Analysis Platform</h2>
    <p class="analysis-content">
        Welcome to our cutting-edge stock analysis platform, leveraging Artificial Intelligence and Large Language Models (LLMs) to deliver professional-grade investment insights. Our system offers:
    </p>
    <ul class="analysis-list">
        <li class="analysis-list-item">Comprehensive sentiment analysis derived from Reddit discussions</li>
        <li class="analysis-list-item">In-depth fundamental and technical analyses</li>
        <li class="analysis-list-item">Extensive web and news research integration</li>
        <li class="analysis-list-item">Customizable analysis parameters including time frames and specific indicators</li>
    </ul>
    <p class="analysis-content">
        Users can obtain a detailed, AI-generated analysis report by simply selecting a stock symbol, specifying a time period, and choosing desired analysis indicators. This platform aims to empower investors with data-driven, AI-enhanced decision-making tools for the complex world of stock market investments.
    </p>
</div>
""", unsafe_allow_html=True)

# Model selection
model_option = st.sidebar.selectbox("Select LLM Model", ['OpenAI GPT-4o','OpenAI GPT-4o Mini', 'Llama 3 8B', 'Llama 3.1 70B', 'Llama 3.1 8B'])

# User API key inputs based on model selection
if model_option in ['OpenAI GPT-4o', 'OpenAI GPT-4o Mini']:
    openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    groq_api_key = None
else:
    groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    openai_api_key = None

stock_symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
time_period = st.sidebar.selectbox("Select Time Period", ['1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'])
indicators = st.sidebar.multiselect("Select Indicators", ['Moving Averages', 'Volume', 'RSI', 'MACD'])
analyze_button = st.sidebar.button("📊 Analyze Stock", help="Click to start the stock analysis")

# Initialize session state
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
    st.session_state.stock_info = None
    st.session_state.stock_data = None
    st.session_state.result_file_path = None

def get_stock_data(stock_symbol, period='1y'):
    return yf.download(stock_symbol, period=period)

def plot_stock_chart(stock_data, indicators):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.6, 0.2, 0.2])

    # Main price chart
    fig.add_trace(go.Candlestick(x=stock_data.index,
                                 open=stock_data['Open'],
                                 high=stock_data['High'],
                                 low=stock_data['Low'],
                                 close=stock_data['Close'],
                                 name='Price'),
                  row=1, col=1)

    # Add selected indicators
    if 'Moving Averages' in indicators:
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'].rolling(window=50).mean(), name='50 MA', line=dict(color='orange')), row=1, col=1)
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'].rolling(window=200).mean(), name='200 MA', line=dict(color='red')), row=1, col=1)

    if 'Volume' in indicators:
        fig.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'], name='Volume'), row=2, col=1)

    if 'RSI' in indicators:
        delta = stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        fig.add_trace(go.Scatter(x=stock_data.index, y=rsi, name='RSI'), row=3, col=1)

    if 'MACD' in indicators:
        ema12 = stock_data['Close'].ewm(span=12, adjust=False).mean()
        ema26 = stock_data['Close'].ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        fig.add_trace(go.Scatter(x=stock_data.index, y=macd, name='MACD'), row=3, col=1)
        fig.add_trace(go.Scatter(x=stock_data.index, y=signal, name='Signal'), row=3, col=1)

    fig.update_layout(
        title='Stock Analysis',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        height=800,
        showlegend=True
    )

    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=False),
        type="date"
    )

    return fig

if analyze_button:
    st.session_state.analyzed = False  # Reset analyzed state
    st.snow()

    
    # Fetch stock info and data
    with st.spinner(f"Fetching data for {stock_symbol}..."):
        stock = yf.Ticker(stock_symbol)
        st.session_state.stock_info = stock.info
        st.session_state.stock_data = get_stock_data(stock_symbol, period=time_period)

    # Create and run the crew
    with st.spinner("Running analysis, please wait..."):
        
        st.session_state.result_file_path = create_crew(stock_symbol, model_option, openai_api_key, groq_api_key)
    
    st.session_state.analyzed = True

# Display stock info if available
if st.session_state.stock_info:
    st.markdown('<p class="medium-font">Stock Information</p>', unsafe_allow_html=True)
    info = st.session_state.stock_info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Company Name:** {info.get('longName', 'N/A')}")
        st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
    with col2:
        st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
        st.markdown(f"**Country:** {info.get('country', 'N/A')}")
    with col3:
        st.markdown(f"**Current Price:** ${info.get('currentPrice', 'N/A')}")
        st.markdown(f"**Market Cap:** ${info.get('marketCap', 'N/A')}")

# Display CrewAI result if available
if st.session_state.result_file_path:
    st.markdown('<p class="medium-font">Analysis Result</p>', unsafe_allow_html=True)
    
    # Read the result from the file
    with open(st.session_state.result_file_path, 'r') as file:
        result = file.read()
    
    # Display the markdown content
    st.markdown(result)

# Display chart
if st.session_state.analyzed and st.session_state.stock_data is not None:
    st.markdown('<p class="medium-font">Interactive Stock Chart</p>', unsafe_allow_html=True)
    st.plotly_chart(plot_stock_chart(st.session_state.stock_data, indicators), use_container_width=True)

# Footer
st.markdown("---")
st.markdown('<p class="small-font">Created by Batuhan Sener | Data provided by Reddit and Yahoo Finance </p>', unsafe_allow_html=True)
