import streamlit as st
from coin_change import coin_change_dp_verbose, coin_change_greedy_verbose
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Coin Change Solver",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .method-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .method-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .coin-display {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-weight: bold;
    }
    
    .result-success {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .result-error {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar-content {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💰 Coin Change Problem Solver</h1>
    <p>Compare Dynamic Programming vs Greedy Algorithm Performance</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.markdown("## 🔧 Configuration")
    
    # Amount input with validation
    amount = st.number_input(
        "💵 Target Amount:", 
        min_value=1, 
        max_value=10000,
        value=11,
        step=1,
        help="Enter the amount you want to make change for"
    )
    
    # Coin denominations
    st.markdown("### 🪙 Coin Denominations")
    coin_preset = st.selectbox(
        "Quick Presets:",
        ["Custom", "US Coins (1,5,10,25)", "Euro Coins (1,2,5,10,20,50)", "UK Coins (1,2,5,10,20,50)"]
    )
    
    if coin_preset == "US Coins (1,5,10,25)":
        coins_input = "1,5,10,25"
    elif coin_preset == "Euro Coins (1,2,5,10,20,50)":
        coins_input = "1,2,5,10,20,50"
    elif coin_preset == "UK Coins (1,2,5,10,20,50)":
        coins_input = "1,2,5,10,20,50"
    else:
        coins_input = st.text_input("Enter coin values (comma-separated):", "1,5,10,25")
    
    # Validate coins input
    try:
        coins = [int(x.strip()) for x in coins_input.split(",") if x.strip().isdigit()]
        coins = sorted(list(set(coins)))  # Remove duplicates and sort
        if not coins:
            st.error("Please enter valid coin denominations")
            st.stop()
    except:
        st.error("Invalid coin format. Use comma-separated numbers.")
        st.stop()
    
    # Display coins
    st.markdown("**Available Coins:**")
    coins_html = "".join([f'<span class="coin-display">{coin}</span>' for coin in coins])
    st.markdown(coins_html, unsafe_allow_html=True)
    
    # Algorithm selection
    st.markdown("### 🧮 Algorithm Selection")
    algorithm_choice = st.radio(
        "Choose Algorithm:",
        ["Both (Compare)", "Dynamic Programming Only", "Greedy Only"],
        help="Select which algorithm(s) to run"
    )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🚀 Calculate Solution", type="primary"):
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = {}
        
        if algorithm_choice in ["Both (Compare)", "Dynamic Programming Only"]:
            status_text.text("Running Dynamic Programming...")
            progress_bar.progress(25)
            
            dp_count, dp_used, dp_logs = coin_change_dp_verbose(coins, amount)
            results['DP'] = {
                'count': dp_count,
                'used': dp_used,
                'logs': dp_logs,
                'name': 'Dynamic Programming'
            }
            progress_bar.progress(50)
        
        if algorithm_choice in ["Both (Compare)", "Greedy Only"]:
            status_text.text("Running Greedy Algorithm...")
            progress_bar.progress(75)
            
            greedy_count, greedy_used, greedy_logs = coin_change_greedy_verbose(coins, amount)
            results['Greedy'] = {
                'count': greedy_count,
                'used': greedy_used,
                'logs': greedy_logs,
                'name': 'Greedy Algorithm'
            }
            progress_bar.progress(100)
        
        status_text.text("Complete!")
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        st.markdown("## 📊 Results")
        
        if algorithm_choice == "Both (Compare)":
            # Comparison view
            col_dp, col_greedy = st.columns(2)
            
            with col_dp:
                st.markdown("### 🧠 Dynamic Programming")
                if results['DP']['count'] == -1:
                    st.markdown("""
                    <div class="result-error">
                        <h4>❌ No Solution Found</h4>
                        <p>The target amount cannot be made with given coins.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-success">
                        <h4>✅ Optimal Solution</h4>
                        <p><strong>Minimum Coins:</strong> {results['DP']['count']}</p>
                        <p><strong>Coins Used:</strong> {results['DP']['used']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_greedy:
                st.markdown("### ⚡ Greedy Algorithm")
                if results['Greedy']['count'] == -1:
                    st.markdown("""
                    <div class="result-error">
                        <h4>❌ No Solution Found</h4>
                        <p>The target amount cannot be made with given coins.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-success">
                        <h4>✅ Solution Found</h4>
                        <p><strong>Coins Used:</strong> {results['Greedy']['count']}</p>
                        <p><strong>Coins:</strong> {results['Greedy']['used']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Performance comparison chart
            if results['DP']['count'] != -1 and results['Greedy']['count'] != -1:
                comparison_data = pd.DataFrame({
                    'Algorithm': ['Dynamic Programming', 'Greedy'],
                    'Coins Used': [results['DP']['count'], results['Greedy']['count']]
                })
                
                fig = px.bar(
                    comparison_data, 
                    x='Algorithm', 
                    y='Coins Used',
                    title='Algorithm Performance Comparison',
                    color='Algorithm',
                    color_discrete_map={
                        'Dynamic Programming': '#667eea',
                        'Greedy': '#764ba2'
                    }
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            # Single algorithm view
            algorithm_key = 'DP' if 'DP' in results else 'Greedy'
            result = results[algorithm_key]
            
            if result['count'] == -1:
                st.markdown(f"""
                <div class="result-error">
                    <h3>❌ No Solution Found</h3>
                    <p>The target amount {amount} cannot be made with the given coin denominations.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-success">
                    <h3>✅ {result['name']} Solution</h3>
                    <p><strong>Minimum Coins Needed:</strong> {result['count']}</p>
                    <p><strong>Coins Used:</strong> {result['used']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Visualization of coin usage
                if result['used']:
                    coin_counts = {}
                    for coin in result['used']:
                        coin_counts[coin] = coin_counts.get(coin, 0) + 1
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=list(coin_counts.keys()),
                            y=list(coin_counts.values()),
                            marker_color='#667eea'
                        )
                    ])
                    fig.update_layout(
                        title='Coin Usage Distribution',
                        xaxis_title='Coin Denomination',
                        yaxis_title='Number of Coins Used'
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Process logs
        st.markdown("## 🔍 Calculation Process")
        
        for key, result in results.items():
            with st.expander(f"📋 {result['name']} Step-by-Step Process"):
                if result['logs']:
                    st.code("\n".join(result['logs']), language="text")
                else:
                    st.info("No detailed logs available for this algorithm.")

with col2:
    # Information panel
    st.markdown("## ℹ️ Algorithm Info")
    
    with st.expander("🧠 Dynamic Programming", expanded=True):
        st.markdown("""
        **Optimal Solution Guaranteed**
        - Uses bottom-up approach
        - Considers all possibilities
        - Time: O(amount × coins)
        - Space: O(amount)
        """)
    
    with st.expander("⚡ Greedy Algorithm"):
        st.markdown("""
        **Fast but Not Always Optimal**
        - Uses largest coin first
        - May not find optimal solution
        - Time: O(coins × log coins)
        - Space: O(1)
        """)
    
    # Quick stats
    if coins:
        st.markdown("## 📈 Quick Stats")
        st.metric("Target Amount", f"{amount}")
        st.metric("Available Denominations", len(coins))
        st.metric("Largest Coin", max(coins))
        st.metric("Smallest Coin", min(coins))

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    💡 <strong>Tip:</strong> Dynamic Programming always finds the optimal solution, 
    while Greedy is faster but may not always be optimal for all coin systems.
</div>
""", unsafe_allow_html=True)