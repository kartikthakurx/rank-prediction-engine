# 🏆 Rank Prediction Engine

Rank Prediction Engine is a dark-themed machine learning web application built with **Python and Streamlit** that predicts a CodeChef coder's global rank, star tier, and performance potential based on rating and problem-solving metrics.

## ✨ Features

- **Dark-Themed Dashboard & Top Summary Bar:** Displays real-time summary readouts for **Predicted Rank**, **CodeChef Star Tier**, and **Potential Score (%)**.
- **CodeChef 1★–7★ Tier System:** Automatically classifies coders from **1★ (Beginner)** to **7★ (Elite)** with color-coded badges based on current rating.
- **Synced Sliders & Direct Typing Inputs:** Adjust **Current Rating**, **Highest Rating**, **Fully Solved Problems**, and **Partially Solved Problems** by either dragging sliders or typing exact numbers—both stay synced automatically.
- **Built-in Input Validation:** Enforces `Highest Rating >= Current Rating` to prevent out-of-distribution `Performance Score` values, and displays a warning when ratings fall below `1700` (outside the top 9,846 training range).
- **Model Performance Overview:** Displays actual evaluation metrics from the trained Random Forest Regressor directly on the dashboard.

## 📊 Model Performance

Trained on **9,846 CodeChef profiles** (`codechef_data.csv`) using a `RandomForestRegressor` (80/20 train-test split) and compared against Linear Regression (`R² = 0.7324`):

| Metric | Value |
| :--- | :--- |
| **MAE** | ±14.44 positions |
| **RMSE** | 27.84 |
| **MSE** | 775.03 |
| **R² Score** | 0.9999 |

## 🛠️ Tech Stack

- **Web UI:** Streamlit, Custom CSS/HTML
- **Machine Learning & Data:** Python, Pandas, NumPy, scikit-learn, Pickle
- **Training & Visualization:** Jupyter Notebook (`Rank_Predictor.ipynb`), Matplotlib, Seaborn


## 📸 Screenshots


###  Beginner
<img width="550" height="700" alt="Beginner" src="https://github.com/user-attachments/assets/d3a650aa-40c2-491f-933a-0d1c7f8a6c9d" />



###  Strong
<img width="516" height="700" alt="Strong" src="https://github.com/user-attachments/assets/0d60cc82-e281-4fa2-ac1c-34b3e504f575" />



###  Elite
<img width="514" height="700" alt="Elite" src="https://github.com/user-attachments/assets/4c9dcdb7-7fc5-4fe2-b6f1-6c8fa0fe8601" />



## 🚀 Local Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kartikthakurx/rank-predictor.git
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

   *If `streamlit` is not recognized in your terminal, run:*

   ```bash
   python -m streamlit run app.py
   ```
<br>

## 👨‍💻 Developer

**Kartik Thakur**

- **GitHub:** [@kartikthakurx](https://github.com/kartikthakurx)

<br>


## 📜 License

This project is licensed under the MIT License.



## ⭐ Support

If you find this project helpful or well-structured, please consider giving the repository a Star (⭐) on GitHub!

