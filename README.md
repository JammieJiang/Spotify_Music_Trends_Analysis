# 🎵 Spotify Music Trends Analysis

An interactive web application built with Streamlit that explores music trends and patterns from Spotify's popular songs dataset (2010-2019). This project provides data-driven insights into how music characteristics have evolved over time through beautiful visualizations and statistical analysis.

## Features

### Interactive Data Exploration
- **Dynamic Filtering**: Filter data by year range and music genres in real-time
- **Beautiful UI**: Modern glassmorphism design with gradient backgrounds
- **Responsive Layout**: Optimized for different screen sizes

### Key Analyses
1. **Danceability vs Energy Correlation**
   - Scatter plot with trend line analysis
   - Statistical correlation coefficients
   - Year-over-year trend visualization

2. **Genre Analysis**
   - Genre popularity evolution over time (stacked bar chart)
   - Song duration distribution by genre (box plot)
   - Popularity ratings comparison (violin plot)
   - Genre ranking statistics

3. **Data Insights**
   - Real-time metrics and statistics
   - Interactive hover details
   - Downloadable filtered datasets

## Technologies Used

- **Python 3.8+**
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **SciPy**: Statistical analysis
- **Pillow (PIL)**: Image processing for background

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/JammieJiang/Spotify_Music_Trends_Analysis.git
cd Spotify_Music_Trends_Analysis
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install required packages**
```bash
pip install -r requirements.txt
```

4. **Prepare your data**
   - Place your `top10_s.csv` file in the project root directory
   - Optionally add background image (`img.png` or `img.jpg`) for custom styling

## Usage

### Running the Application

```bash
streamlit run streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Application

1. **Adjust Filters** (Left Sidebar):
   - Use the year slider to select your desired time range
   - Select one or more genres from the multiselect dropdown
   - View real-time statistics about your filtered dataset

2. **Explore Visualizations**:
   - **Question 1**: Analyze the relationship between danceability and energy
   - **Question 2**: Compare characteristics across different music genres

3. **Export Data**:
   - Expand the "View Filtered Raw Data" section
   - Click "Download Filtered Data (CSV)" to export your filtered dataset

## Project Structure

```
Spotify_Music_Trends_Analysis/
│
├── streamlit_app.py          # Main application file
├── top10_s.csv                # Dataset (required)
├── img.png / img.jpg          # Background image (optional)
├── fonts.googleapis.com.css   # Custom fonts (optional)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── .gitignore                 # Git ignore file
```

## Dataset Format

The application expects a CSV file (`top10_s.csv`) with the following columns:

| Column | Description |
|--------|-------------|
| `year` | Release year |
| `title` | Song title |
| `artist` | Artist name |
| `top genre` | Music genre |
| `dur` | Duration in milliseconds |
| `dnce` | Danceability (0-100) |
| `nrgy` | Energy level (0-100) |
| `pop` | Popularity score (0-100) |
| `val` | Valence (0-100) |
| `acous` | Acousticness (0-100) |
| `spch` | Speechiness (0-100) |
| `live` | Liveness (0-100) |
| `dB` | Loudness in dB |

## Customization

### Background Image
Place an image file named `img.png` or `img.jpg` in the project root to use as a custom background.

### Colors and Styling
The application uses a purple gradient theme. You can modify colors in the CSS section of `streamlit_app.py`:
- Main gradient: `#667eea` to `#764ba2`
- Accent colors defined in the style section

## Key Insights

The application helps answer questions such as:
- How has the relationship between danceability and energy evolved over time?
- Which genres have gained or lost popularity over the years?
- How do song durations vary across different genres?
- What are the popularity trends for different music genres?

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Jammie Jiang**
- GitHub: [@JammieJiang](https://github.com/JammieJiang)
- GitHub：[@RuoxiBao](https://github.com/RuoxiBao08)

## Acknowledgments

- Spotify for providing the music data API
- Streamlit community for the amazing framework
- Plotly for interactive visualization capabilities

## Contact

If you have any questions or suggestions, please feel free to open an issue or contact me directly.

---

Star this repository if you find it helpful!
