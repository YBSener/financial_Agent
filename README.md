# 📊 Professional Stock Analysis Dashboard

    ![Usage](./financial_Agent/finagent.gif)

## 🌟 Overview
**Professional Stock Analysis Dashboard** is a web application that allows users to analyze stocks using advanced machine learning models and financial tools. The application provides detailed insights into stock performance, technical analysis, fundamental analysis, and sentiment analysis from various sources.

## ✨ Features
- **📈 Interactive Stock Chart**: Visualize stock price data along with key technical indicators.
- **📊 Comprehensive Stock Analysis**: Get detailed reports on stock performance, including technical and fundamental analysis.
- **🤖 Model Selection**: Choose from multiple language models (OpenAI GPT-4, Llama 3 8B, Groq Llama) for generating analysis reports.
- **💬 Sentiment Analysis**: Analyze sentiment from Reddit discussions.

## 🚀 Installation

### Prerequisites
- Python 3.7+
- Streamlit
- yFinance
- Plotly
- Langchain
- Praw
- CrewAI
- Required API keys

### Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/YBSener/financial_Agent.git
    cd financial_Agent
    ```
2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    Create a `.env` file in the project root and add the following environment variables:
    ```env
    SERPER_API_KEY=your_serper_api_key
    OPENAI_API_KEY=your_openai_api_key
    REDDIT_CLIENT_ID=your_reddit_client_id
    REDDIT_CLIENT_SECRET=your_reddit_client_secret
    REDDIT_USER_AGENT=your_reddit_user_agent
    GROQ_API_KEY=your_groq_api_key
    ```

## 🛠️ Usage

### Running the Application
1. Start the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser 

3. Use the sidebar to configure your analysis:
    - Select the language model.
    - Enter the stock symbol.
    - Choose the time period and indicators.

4. Click the "Analyze Stock" button to generate the report and visualize the stock data.

### Application Structure
- `app.py`: Contains the Streamlit application code for the user interface.
- `main.py`: Defines the CrewAI agents, tasks, and processes for generating stock analysis reports.
- `tools/`: Contains custom tools for sentiment analysis and financial data retrieval.

## 📊 Example Output

### Investment Report: Apple Inc. (AAPL)

#### 1. Executive Summary: Investment Recommendation
Given the current valuation metrics, slowing growth rates, and mixed technical indicators, a "hold" recommendation is advised for Apple Inc. (AAPL). While the company's strong brand and market position remain robust, the high P/E and P/B ratios suggest potential overvaluation, warranting caution for new investments.

#### 2. Company Snapshot: Key Facts
- **Company Name:** Apple Inc.
- **Sector:** Technology
- **Industry:** Consumer Electronics
- **Market Capitalization:** $3.34 trillion
- **P/E Ratio:** 33.90
- **P/B Ratio:** 45.06
- **Current Ratio:** 1.04
- **Debt to Equity Ratio:** 140.97
- **ROE:** 1.47

#### 3. Financial Highlights: Top Metrics and Peer Comparison
Apple's financial metrics reveal mixed signals:
- **Revenue Growth (YoY):** -2.8%
- **Net Income Growth (YoY):** -2.8%
- **Gross Margin:** 45.59%
- **Operating Margin:** 30.74%
- Compared to peers, AAPL's high P/E and P/B ratios indicate market expectations for growth but also suggest a premium valuation due to brand loyalty and innovation.

#### 4. Technical Analysis: Key Findings
Over the past year, AAPL's technical indicators show a generally bullish trend:
- **Current Price:** $217.96
- **Support Level:** $210.30
- **Resistance Level:** $237.23
- **RSI:** 37.02 (indicating oversold conditions)
- **MACD:** Bearish but showing signs of stabilization.

Despite the bullish trend, the current price is below key moving averages, suggesting potential short-term volatility.

#### 5. Fundamental Analysis: Top Strengths and Concerns
**Strengths:**
- Strong brand equity and consumer loyalty.
- High operating and net profit margins relative to competitors.

**Concerns:**
- Declining revenue and net income growth.
- High leverage as indicated by the debt-to-equity ratio of 140.97.
- Current market valuation appears inflated compared to intrinsic value based on DCF analysis ($1.32 trillion).

#### 6. Risk and Opportunity: Major Risk and Growth Catalyst
**Major Risks:**
- High valuation may expose AAPL to significant downside if growth does not meet market expectations.
- Economic downturns affecting consumer spending can impact sales.

**Growth Catalysts:**
- Continued innovation in product lines (e.g., AR/VR, AI integration).
- Expansion into emerging markets.

#### 7. Reddit Sentiment: Key Takeaway from Sentiment Analysis
Sentiment analysis from Reddit indicates a mixed view among retail investors. Out of 100 posts analyzed:
- **Positive Comments:** 10
- **Negative Comments:** 3
- **Neutral Comments:** 87

This suggests a generally cautious but neutral outlook among retail investors, with some acknowledging overvaluation concerns.

#### 8. Investment Thesis: Bull and Bear Cases
**Bull Case:**
- Continued product innovation and expanding services revenue could drive higher growth rates.
- Strong brand loyalty and ecosystem may sustain market share.

**Bear Case:**
- Slowing growth and high valuation could lead to a significant correction.
- Increased competition in technology and consumer electronics could erode margins.

#### 9. Price Target: 12-Month Forecast
Based on current analyses and market conditions, a conservative price target for AAPL over the next 12 months is projected at $210, reflecting potential market corrections and growth risks, while allowing for a recovery towards the support level.

In conclusion, while Apple Inc. remains a strong player in the technology space, investors should approach with a "hold" strategy, carefully considering the high valuation and fluctuating market conditions.

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact
For any questions or support, please open an issue or contact (mailto:ybatu.sener@gmail.com).

