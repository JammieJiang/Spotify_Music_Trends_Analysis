import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title=""
               "",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Function to convert local image to base64 with compression
def get_base64_image(image_path):
    """Convert local image to base64 string for CSS usage"""
    try:
        from PIL import Image
        import io

        # Open and compress the image
        img = Image.open(image_path)

        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Resize if too large (max width 1920px)
        max_width = 1920
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
            print(f"🔧 Resized image to {new_size}")

        # Save to bytes with compression
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=85, optimize=True)
        img_byte_arr = img_byte_arr.getvalue()

        encoded = base64.b64encode(img_byte_arr).decode()
        size_kb = len(encoded) / 1024
        return encoded
    except ImportError:
        print("⚠️ PIL not found, trying without compression...")
        try:
            with open(image_path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
                return encoded
        except Exception as e:
            print(f"❌ Error loading image: {e}")
            return None
    except FileNotFoundError:
        print(f"❌ Background image not found: {image_path}")
        return None
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return None


# Function to load local CSS file
def load_local_css(css_path):
    """Load local CSS file"""
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            return css_content
    except FileNotFoundError:
        return ""
    except Exception as e:
        return ""


possible_image_names = ["img.png", "img.jpg"]
bg_image = None

for img_name in possible_image_names:
    bg_image = get_base64_image(img_name)
    if bg_image:
        break

# Load local font CSS (optional, fallback to system fonts if not found)
local_font_css = load_local_css("fonts.googleapis.com.css")

# Build CSS with conditional background - 关键修改：使用 .stApp 而不是 .main
if bg_image:
    background_style = f"""
        background: 
            linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%),
            url(data:image/jpeg;base64,{bg_image}) center/cover fixed;
        background-blend-mode: overlay;
    """
else:
    background_style = """
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    """
    print(" Using gradient background (fallback)")

# Custom CSS styles - 关键修改：针对 .stApp 应用背景
st.markdown(f"""
    <style>
    /* Local font CSS */
    {local_font_css}

    /* Fallback to web fonts if local not available */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global styles */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}

    /* Hide Streamlit default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    .stApp {{
        {background_style}
    }}

    /* Main container styles */
    .main {{
        padding: 2rem 3rem;
    }}

    /* Main header styles */
    .main-header {{
        font-size: 96px  !important; 
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 30px 0 10px 0;
        letter-spacing: -2px;
    }}

    /* Subtitle styles */
    .sub-title {{
        text-align: center;
        color: #1e293b;
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 40px;
        line-height: 1.6;
        text-shadow: 0 1px 2px rgba(255,255,255,0.8);
    }}

    /* Section header styles */
    .section-header {{
        font-size: 28px;
        font-weight: 600;
        color: #1e293b;
        margin-top: 50px;
        margin-bottom: 25px;
        padding-bottom: 12px;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }}

    /* Insight card styles */
    .insight-card {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin: 20px 0;
        border-left: 4px solid #667eea;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .insight-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }}

    .insight-card h3 {{
        color: #1e293b;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 15px;
    }}

    .insight-card p {{
        color: #475569;
        font-size: 15px;
        line-height: 1.7;
        margin: 8px 0;
    }}

    /* Stat card styles */
    .stat-card {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 10px 0;
    }}

    .stat-value {{
        font-size: 32px;
        font-weight: 700;
        color: #667eea;
        margin: 10px 0;
    }}

    .stat-label {{
        font-size: 14px;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* Sidebar styles */
    section[data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
    }}

    section[data-testid="stSidebar"] .element-container {{
        color: #1e293b;
    }}

    /* Button styles */
    .stButton>button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.3);
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(102, 126, 234, 0.4);
    }}

    /* Tabs styles */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 500;
        padding: 12px 20px;
        transition: all 0.2s ease;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }}

    /* Metric styles */
    [data-testid="stMetricValue"] {{
        font-size: 28px;
        font-weight: 700;
        color: #667eea;
    }}

    [data-testid="stMetricLabel"] {{
        font-size: 14px;
        font-weight: 500;
        color: #64748b;
    }}

    /* Dataframe styles */
    .dataframe {{
        border: none !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }}

    /* Slider styles */
    .stSlider [data-baseweb="slider"] {{
        background-color: #e2e8f0;
    }}

    /* Divider styles */
    hr {{
        margin: 40px 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    }}

    /* Expander styles */
    .streamlit-expanderHeader {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        font-weight: 600;
        color: #1e293b;
    }}

    /* Footer styles */
    .footer {{
        text-align: center;
        color: #64748b;
        font-size: 14px;
        padding: 30px 0;
        margin-top: 50px;
        border-top: 1px solid rgba(226, 232, 240, 0.5);
    }}

    .footer a {{
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }}

    /* Responsive design */
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 40px;
        }}

        .section-header {{
            font-size: 22px;
        }}
    }}

    /* Chart container styles */
    .plot-container {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }}

    /* Additional glass effect for plotly charts */
    .js-plotly-plot {{
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 10px;
    }}
    </style>
""", unsafe_allow_html=True)


# Data loading function
@st.cache_data
def load_data():
    """
    Load and preprocess Spotify data
    Note: Replace the CSV file path with your actual path
    """
    try:
        # Read CSV file
        data = pd.read_csv('top10_s.csv')

        # Print original columns for debugging
        print("Original columns:", data.columns.tolist())

        # Column mapping - map abbreviated CSV columns to full column names
        column_mapping = {
            'dur': 'duration_ms',
            'dnce': 'danceability',
            'nrgy': 'energy',
            'pop': 'popularity',
            'top genre': 'genre',
            'val': 'valence',
            'acous': 'acousticness',
            'spch': 'speechiness',
            'live': 'liveness',
            'dB': 'loudness'
        }

        # Rename columns
        data = data.rename(columns=column_mapping)

        # Check if required columns exist
        required_columns = ['year', 'title', 'artist', 'genre',
                            'danceability', 'energy', 'duration_ms', 'popularity']
        missing_columns = [col for col in required_columns if col not in data.columns]

        if missing_columns:
            st.error(f"Data file missing the following columns: {missing_columns}")
            st.info("Available columns: " + ", ".join(data.columns.tolist()))
            st.stop()

        # Data preprocessing
        data['duration_min'] = data['duration_ms'] / 60000
        data['year'] = data['year'].astype(int)

        # Data cleaning
        data = data.dropna(subset=required_columns)

        # Data validation
        if len(data) == 0:
            st.error("Data is empty, please check the CSV file")
            st.stop()

        print(f"Successfully loaded {len(data)} records")

        return data

    except FileNotFoundError:
        st.error("File 'top10_s.csv' not found")
        st.info("Please ensure the CSV file is in the same directory as the script")

        # Provide sample data as fallback
        with st.expander("Continue with sample data"):
            if st.button("Generate sample data"):
                np.random.seed(42)
                years = np.repeat(range(2010, 2020), 100)
                genres = np.random.choice(['Pop', 'Rock', 'Hip-Hop', 'Electronic', 'R&B'], 1000)

                data = pd.DataFrame({
                    'year': years,
                    'title': [f'Song_{i}' for i in range(1000)],
                    'artist': [f'Artist_{i % 100}' for i in range(1000)],
                    'genre': genres,
                    'danceability': np.random.uniform(30, 90, 1000),
                    'energy': np.random.uniform(30, 90, 1000),
                    'duration_ms': np.random.uniform(180000, 300000, 1000),
                    'popularity': np.random.uniform(50, 100, 1000)
                })

                data['duration_min'] = data['duration_ms'] / 60000
                return data

        st.stop()

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.exception(e)
        st.stop()


# Load data
df = load_data()

# ============ Page Title ============
st.markdown('<p class="main-header">Spotify Music Trends Analysis</p>',
            unsafe_allow_html=True)

st.markdown("""
    <div class="sub-title">
        Explore the evolution of music characteristics from 2010-2019<br>
        Data-driven insights into popular music trends and patterns
    </div>
""", unsafe_allow_html=True)

# ============ Sidebar Interactive Components ============
st.sidebar.markdown("## Data Filters")
st.sidebar.markdown("Adjust parameters to customize analysis scope")

# Interactive component 1: Year slider
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['year'].min()),
    max_value=int(df['year'].max()),
    value=(int(df['year'].min()), int(df['year'].max())),
    step=1,
    help="Drag the slider to select the year range for analysis"
)

# Interactive component 2: Genre multiselect
all_genres = sorted(df['genre'].unique())
selected_genres = st.sidebar.multiselect(
    "Select Music Genres",
    options=all_genres,
    default=all_genres[:3] if len(all_genres) >= 3 else all_genres,
    help="Select 1-5 genres for comparative analysis"
)

# Data filtering
filtered_df = df[
    (df['year'] >= year_range[0]) &
    (df['year'] <= year_range[1]) &
    (df['genre'].isin(selected_genres))
]

# Display data overview
st.sidebar.markdown("---")
st.sidebar.markdown("### Data Overview")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Total Songs", len(filtered_df))
    st.metric("Year Span", f"{year_range[1] - year_range[0] + 1} years")
with col2:
    st.metric("Genre Count", len(selected_genres))
    st.metric("Data Completeness",
              f"{(1 - filtered_df.isnull().sum().sum() / (filtered_df.shape[0] * filtered_df.shape[1])) * 100:.1f}%")

# ============ Main Content Area ============

# Question 1: Correlation analysis between danceability and energy
st.markdown('<p class="section-header">Question 1: Relationship Evolution of Danceability and Energy</p>',
            unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Chart 1: Scatter plot (with trend line)
    fig1 = px.scatter(
        filtered_df,
        x='danceability',
        y='energy',
        color='year',
        size='popularity',
        hover_data=['title', 'artist', 'genre'],
        color_continuous_scale='Viridis',
        title='Danceability vs Energy (Bubble size represents popularity)',
        labels={
            'danceability': 'Danceability',
            'energy': 'Energy',
            'year': 'Year'
        },
        height=500
    )

    # Add trend line
    z = np.polyfit(filtered_df['danceability'], filtered_df['energy'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(filtered_df['danceability'].min(),
                          filtered_df['danceability'].max(), 100)

    fig1.add_trace(go.Scatter(
        x=x_trend,
        y=p(x_trend),
        mode='lines',
        name='Trend Line',
        line=dict(color='#ef4444', width=2, dash='dash')
    ))

    fig1.update_layout(
        plot_bgcolor='white',
        font=dict(size=12, family='Inter'),
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Calculate correlation coefficient
    corr, p_value = stats.pearsonr(filtered_df['danceability'],
                                   filtered_df['energy'])

    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown("### Key Findings")

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Correlation", f"{corr:.3f}")
    with col_b:
        st.metric("Significance", "Significant" if p_value < 0.05 else "Not Significant")

    st.markdown(f"""
    <p><strong>Trend Interpretation:</strong></p>
    <p>Correlation coefficient is {corr:.3f}, indicating {'positive correlation' if corr > 0 else 'negative correlation'}</p>
    <p>Songs with higher energy values have {'stronger' if corr > 0 else 'weaker'} danceability</p>
    <p>Recent trend: {'both growing simultaneously' if corr > 0.5 else 'relatively weak relationship'}</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Annual trend mini chart
    yearly_avg = filtered_df.groupby('year')[['danceability', 'energy']].mean().reset_index()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=yearly_avg['year'],
        y=yearly_avg['danceability'],
        name='Danceability',
        line=dict(color='#667eea', width=3),
        fill='tonexty'
    ))
    fig_trend.add_trace(go.Scatter(
        x=yearly_avg['year'],
        y=yearly_avg['energy'],
        name='Energy',
        line=dict(color='#764ba2', width=3)
    ))
    fig_trend.update_layout(
        title='Annual Average Trend',
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter')
    )
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# Question 2: Genre analysis
st.markdown('<p class="section-header">Question 2: Characteristic Comparison Across Genres</p>',
            unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Genre Popularity Evolution", "Genre Duration & Rating Analysis"])

with tab1:
    # Chart 2: Stacked bar chart
    genre_year = filtered_df.groupby(['year', 'genre']).size().reset_index(name='count')

    fig2 = px.bar(
        genre_year,
        x='year',
        y='count',
        color='genre',
        title='Annual Song Count Change by Genre (Stacked View)',
        labels={'count': 'Song Count', 'year': 'Year', 'genre': 'Genre'},
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=450
    )

    fig2.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        xaxis=dict(tickmode='linear', tick0=year_range[0], dtick=1),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter')
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Genre proportion statistics
    st.markdown("### Genre Rankings")
    genre_stats = filtered_df['genre'].value_counts()
    cols = st.columns(min(3, len(genre_stats)))

    for idx, (genre, count) in enumerate(genre_stats.head(3).items()):
        with cols[idx]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Top {idx + 1}</div>
                <div class="stat-value">{count}</div>
                <div class="stat-label">{genre} ({count / len(filtered_df) * 100:.1f}%)</div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        # Chart 3: Box plot (duration distribution)
        fig3 = px.box(
            filtered_df,
            x='genre',
            y='duration_min',
            color='genre',
            title='Song Duration Distribution by Genre',
            labels={'duration_min': 'Duration (minutes)', 'genre': 'Genre'},
            color_discrete_sequence=px.colors.qualitative.Pastel,
            height=400
        )

        fig3.update_layout(
            plot_bgcolor='white',
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter')
        )

        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        # Popularity comparison (violin plot)
        fig4 = px.violin(
            filtered_df,
            x='genre',
            y='popularity',
            color='genre',
            title='Popularity Distribution by Genre',
            labels={'popularity': 'Popularity Rating', 'genre': 'Genre'},
            box=True,
            height=400
        )

        fig4.update_layout(
            plot_bgcolor='white',
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter')
        )

        st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ============ Raw Data Display ============
with st.expander("View Filtered Raw Data"):
    st.dataframe(
        filtered_df[['year', 'title', 'artist', 'genre',
                     'danceability', 'energy', 'duration_min', 'popularity']],
        use_container_width=True
    )

    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=csv,
        file_name=f'spotify_filtered_{year_range[0]}_{year_range[1]}.csv',
        mime='text/csv'
    )

# Footer
st.markdown("""
    <div class="footer">
        Data Source: Spotify 2010-2019 Popular Songs Dataset | 
        Development Tools: Python + Streamlit + Plotly<br>
    </div>
""", unsafe_allow_html=True)