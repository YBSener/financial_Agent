import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from crewai_tools import tool

@tool
def yf_tech_analysis(stock_symbol: str, period: str = "1y"):
    """
    Perform a comprehensive technical analysis on the given stock symbol.
    
    Args:
        stock_symbol (str): The stock symbol to analyze.
        period (str): The time period for analysis. Default is "1y" (1 year).
    
    Returns:
        dict: A dictionary with the detailed technical analysis results.
    """
    # Download data
    data = yf.download(stock_symbol, period=period)
    
    # Basic Moving Averages
    for ma in [20, 50, 100, 200]:
        data[f'{ma}_MA'] = data['Close'].rolling(window=ma).mean()
    
    # Exponential Moving Averages
    for ema in [12, 26, 50, 200]:
        data[f'{ema}_EMA'] = data['Close'].ewm(span=ema, adjust=False).mean()
    
    # MACD
    data['MACD'] = data['12_EMA'] - data['26_EMA']
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    data['20_MA'] = data['Close'].rolling(window=20).mean()
    data['20_SD'] = data['Close'].rolling(window=20).std()
    data['Upper_BB'] = data['20_MA'] + (data['20_SD'] * 2)
    data['Lower_BB'] = data['20_MA'] - (data['20_SD'] * 2)
    
    # Stochastic Oscillator
    low_14 = data['Low'].rolling(window=14).min()
    high_14 = data['High'].rolling(window=14).max()
    data['%K'] = (data['Close'] - low_14) / (high_14 - low_14) * 100
    data['%D'] = data['%K'].rolling(window=3).mean()
    
    # Average True Range (ATR)
    data['TR'] = np.maximum(data['High'] - data['Low'], 
                            np.maximum(abs(data['High'] - data['Close'].shift()), 
                                       abs(data['Low'] - data['Close'].shift())))
    data['ATR'] = data['TR'].rolling(window=14).mean()
    
    # On-Balance Volume (OBV)
    data['OBV'] = (np.sign(data['Close'].diff()) * data['Volume']).cumsum()
    
    # Fibonacci Retracement Levels
    max_price = data['High'].max()
    min_price = data['Low'].min()
    diff = max_price - min_price
    
    fibonacci_levels = {
        '0%': max_price,
        '23.6%': max_price - 0.236 * diff,
        '38.2%': max_price - 0.382 * diff,
        '50%': max_price - 0.5 * diff,
        '61.8%': max_price - 0.618 * diff,
        '100%': min_price
    }
    
    # Calculate support and resistance levels
    data['Support'] = data['Low'].rolling(window=20).min()
    data['Resistance'] = data['High'].rolling(window=20).max()
    
    # Identify potential breakouts
    data['Potential_Breakout'] = np.where((data['Close'] > data['Resistance'].shift(1)), 'Bullish Breakout',
                                 np.where((data['Close'] < data['Support'].shift(1)), 'Bearish Breakdown', 'No Breakout'))
    
    # Trend Identification
    data['Trend'] = np.where((data['Close'] > data['200_MA']) & (data['50_MA'] > data['200_MA']), 'Bullish',
                    np.where((data['Close'] < data['200_MA']) & (data['50_MA'] < data['200_MA']), 'Bearish', 'Neutral'))
    
    # Volume Analysis
    data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
    data['Volume_Trend'] = np.where(data['Volume'] > data['Volume_MA'], 'Above Average', 'Below Average')
    
    # Prepare the results
    latest = data.iloc[-1]
    analysis_results = {
        'Current_Price': latest['Close'],
        'Moving_Averages': {f'{ma}_MA': latest[f'{ma}_MA'] for ma in [20, 50, 100, 200]},
        'Exponential_MAs': {f'{ema}_EMA': latest[f'{ema}_EMA'] for ema in [12, 26, 50, 200]},
        'MACD': {
            'MACD': latest['MACD'],
            'Signal_Line': latest['Signal_Line'],
            'Histogram': latest['MACD_Histogram']
        },
        'RSI': latest['RSI'],
        'Bollinger_Bands': {
            'Upper': latest['Upper_BB'],
            'Middle': latest['20_MA'],
            'Lower': latest['Lower_BB']
        },
        'Stochastic': {
            '%K': latest['%K'],
            '%D': latest['%D']
        },
        'ATR': latest['ATR'],
        'OBV': latest['OBV'],
        'Fibonacci_Levels': fibonacci_levels,
        'Support_Resistance': {
            'Support': latest['Support'],
            'Resistance': latest['Resistance']
        },
        'Potential_Breakout': latest['Potential_Breakout'],
        'Trend': latest['Trend'],
        'Volume': {
            'Current': latest['Volume'],
            'MA': latest['Volume_MA'],
            'Trend': latest['Volume_Trend']
        }
    }
    
    # Add some basic statistics
    analysis_results['Statistics'] = {
        'Yearly_High': data['High'].max(),
        'Yearly_Low': data['Low'].min(),
        'Average_Volume': data['Volume'].mean(),
        'Volatility': data['Close'].pct_change().std() * (252 ** 0.5)  # Annualized volatility
    }
    
    # Add interpretation
    analysis_results['Interpretation'] = {
        'Trend': 'Bullish' if latest['Close'] > latest['200_MA'] else 'Bearish',
        'RSI': 'Overbought' if latest['RSI'] > 70 else ('Oversold' if latest['RSI'] < 30 else 'Neutral'),
        'MACD': 'Bullish' if latest['MACD'] > latest['Signal_Line'] else 'Bearish',
        'Stochastic': 'Overbought' if latest['%K'] > 80 else ('Oversold' if latest['%K'] < 20 else 'Neutral'),
        'Bollinger_Bands': 'Overbought' if latest['Close'] > latest['Upper_BB'] else ('Oversold' if latest['Close'] < latest['Lower_BB'] else 'Neutral'),
        'Volume': 'High' if latest['Volume'] > latest['Volume_MA'] else 'Low'
    }
    
    return analysis_results
