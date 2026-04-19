import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_stock():
    print("=" * 90)
    print(" " * 30 + "STOCK ANALYZER")
    print(" " * 25 + "Moneycontrol Edition")
    print("=" * 90)
    
    # ============================================================
    # EDIT THIS SECTION WITH YOUR STOCK DATA
    # ============================================================
    
    stock_name = "Your Stock Name"  # e.g., "TCS", "Reliance", "Infosys"
    current_price = 1000            # Current market price from NSE/BSE
    
    # Paste data from Moneycontrol (Standalone Financials)
    # Format: [Year, Revenue, Net Profit, EPS, Book Value, Total Assets, Equity, Debt]
    data = {
        'Year': ['Mar \'15', 'Mar \'16', 'Mar \'17', 'Mar \'18', 'Mar \'19', 
                 'Mar \'20', 'Mar \'21', 'Mar \'22', 'Mar \'23', 'Mar \'24'],
        
        'Revenue': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],      # Total Income (Rs. Cr)
        'Net_Profit': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # Net Profit (Rs. Cr)
        'EPS': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],          # Basic EPS (Rs.)
        'Book_Value': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # Book Value per share
        'Total_Assets': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Total Assets
        'Shareholder_Equity': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Shareholders Funds
        'Total_Debt': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    # Long Term + Short Term Debt
    }
    
    # ============================================================
    # DON'T MODIFY BELOW THIS LINE
    # ============================================================
    
    df = pd.DataFrame(data)
    
    # Check if data is still placeholder
    if df['Revenue'].sum() == 0:
        print("\n⚠️  ERROR: Please enter your stock data first!")
        print("Copy data from Moneycontrol into the 'data' dictionary above.")
        return
    
    # Calculate Ratios
    df['Revenue_Growth'] = df['Revenue'].pct_change() * 100
    df['Profit_Growth'] = df['Net_Profit'].pct_change() * 100
    df['EPS_Growth'] = df['EPS'].pct_change() * 100
    df['Net_Margin'] = (df['Net_Profit'] / df['Revenue']) * 100
    df['ROE'] = (df['Net_Profit'] / df['Shareholder_Equity']) * 100
    df['ROA'] = (df['Net_Profit'] / df['Total_Assets']) * 100
    df['Debt_to_Equity'] = df['Total_Debt'] / df['Shareholder_Equity']
    
    # Display Historical Data
    print(f"\n📊 Analyzing: {stock_name}")
    print(f"💰 Current Price: ₹{current_price}")
    print("-" * 90)
    
    display = pd.DataFrame({
        'Year': df['Year'],
        'Revenue': df['Revenue'],
        'Net Profit': df['Net_Profit'],
        'EPS': df['EPS'],
        'ROE %': df['ROE'].round(2),
        'Margin %': df['Net_Margin'].round(2)
    })
    print(display.to_string(index=False))
    
    # CAGR Calculations
    def cagr(start, end, years):
        if start <= 0 or end <= 0 or years == 0:
            return 0
        return ((end/start) ** (1/years) - 1) * 100
    
    n = len(df) - 1
    rev_cagr = cagr(df['Revenue'].iloc[0], df['Revenue'].iloc[-1], n)
    profit_cagr = cagr(df['Net_Profit'].iloc[0], df['Net_Profit'].iloc[-1], n)
    eps_cagr = cagr(abs(df['EPS'].iloc[0]), abs(df['EPS'].iloc[-1]), n)
    
    print(f"\n📈 CAGR ({n} Years):")
    print(f"   Revenue:     {rev_cagr:.2f}%")
    print(f"   Net Profit:  {profit_cagr:.2f}%")
    print(f"   EPS:         {eps_cagr:.2f}%")
    
    # 10-Year Projections
    avg_roe = df['ROE'].tail(5).mean()
    growth = (avg_roe * 0.80 / 100) * 0.70  # Conservative
    
    print(f"\n🔮 10-Year Projections (Growth: {growth*100:.2f}%):")
    projections = []
    eps = df['EPS'].iloc[-1]
    
    for i in range(1, 11):
        year = 2024 + i
        eps = eps * (1 + growth)
        price_20 = eps * 20  # Base case PE 20
        projections.append({'Year': year, 'EPS': eps, 'Price': price_20})
    
    proj_df = pd.DataFrame(projections)
    
    for idx, row in proj_df.iterrows():
        if idx in [0, 4, 9]:  # Show Year 1, 5, 10
            print(f"   {int(row['Year'])}: EPS ₹{row['EPS']:.2f}, Price ₹{row['Price']:.0f}")
    
    target = proj_df['Price'].iloc[-1]
    upside = ((target / current_price) - 1) * 100
    print(f"\n🎯 2034 Target Price: ₹{target:.0f} ({upside:+.0f}% upside)")
    
    # Valuation
    print(f"\n💎 Valuation:")
    eps_curr = df['EPS'].iloc[-1]
    bv_curr = df['Book_Value'].iloc[-1]
    
    graham = np.sqrt(22.5 * eps_curr * bv_curr)
    print(f"   Graham Number: ₹{graham:.2f}")
    print(f"   Book Value:    ₹{bv_curr:.2f} (P/B: {current_price/bv_curr:.2f})")
    print(f"   Current PE:    {current_price/eps_curr:.2f}x")
    
    # Quality Score
    score = 0
    print(f"\n⭐ Quality Score:")
    if df['ROE'].tail(5).mean() > 15: 
        score += 1
        print("   ✓ ROE > 15%")
    else:
        print("   ✗ ROE < 15%")
        
    if df['Net_Margin'].tail(5).mean() > 10:
        score += 1
        print("   ✓ Margin > 10%")
    else:
        print("   ✗ Margin < 10%")
        
    if df['Debt_to_Equity'].iloc[-1] < 0.5:
        score += 1
        print("   ✓ Low Debt")
    else:
        print("   ✗ High Debt")
        
    if rev_cagr > 10:
        score += 1
        print("   ✓ Good Growth")
    else:
        print("   ✗ Slow Growth")
    
    print(f"\n   Score: {score}/4 - ", end="")
    if score >= 4:
        print("STRONG BUY")
    elif score >= 3:
        print("BUY")
    elif score >= 2:
        print("HOLD")
    else:
        print("AVOID")
    
    # Create Charts
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    axes[0,0].plot(df['Year'], df['Revenue'], marker='o', label='Revenue', linewidth=2)
    axes[0,0].plot(df['Year'], df['Net_Profit'], marker='s', label='Net Profit', linewidth=2)
    axes[0,0].set_title('Revenue & Profit Trend')
    axes[0,0].legend()
    axes[0,0].tick_params(axis='x', rotation=45)
    axes[0,0].grid(True, alpha=0.3)
    
    axes[0,1].plot(df['Year'], df['ROE'], marker='o', color='orange', linewidth=2)
    axes[0,1].axhline(y=15, color='green', linestyle='--', label='Good (15%)')
    axes[0,1].set_title('ROE Trend')
    axes[0,1].legend()
    axes[0,1].tick_params(axis='x', rotation=45)
    axes[0,1].grid(True, alpha=0.3)
    
    colors = ['green' if x > 0 else 'red' for x in df['EPS_Growth'].fillna(0)]
    axes[1,0].bar(df['Year'][1:], df['EPS_Growth'][1:], color=colors[1:])
    axes[1,0].set_title('EPS Growth (YoY)')
    axes[1,0].tick_params(axis='x', rotation=45)
    axes[1,0].grid(True, alpha=0.3)
    
    axes[1,1].plot(proj_df['Year'], proj_df['Price'], marker='o', color='blue', linewidth=2, label='Projected')
    axes[1,1].axhline(y=current_price, color='red', linestyle='--', label=f'Current ₹{current_price}')
    axes[1,1].set_title('10-Year Price Projection')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = f"{stock_name.replace(' ', '_')}_analysis.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()
    
    print(f"\n✅ Chart saved: {filename}")
    print("=" * 90)

if __name__ == "__main__":
    analyze_stock()
