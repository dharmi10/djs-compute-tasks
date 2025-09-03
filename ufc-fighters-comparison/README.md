# 🥊 UFC Fighter Comparison App

This project is a Streamlit web application that allows users to compare the statistics of two UFC fighters side-by-side. Select any two fighters and a specific attribute to see a head-to-head comparison of their career stats.

![UFC App Demo](https://i.imgur.com/example.png)  ---

## 📋 Features

- **Select Fighters:** Choose any two fighters from the dataset.
- **Compare Attributes:** Compare them across a wide range of statistical features like Reach, Takedown Accuracy, and Striking Defense.
- **View Summaries:** See a clear summary table of each fighter's main career statistics (Wins, Losses, Draws).
- **Interactive Interface:** A user-friendly and responsive web interface built with Streamlit.

---

## 📊 Data Source

The data used in this project is sourced from the [UFC Fighters Statistics dataset on Kaggle](https://www.kaggle.com/datasets/rajeevw/ufcdata).

The initial data exploration and cleaning process is documented in the `UFC_Fighter_Analysis.ipynb` notebook.

---

## 🚀 Setup and Installation

To run this application locally, please follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/compute-taks.git](https://github.com/your-username/compute-taks.git)
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd compute-taks/ufc-fighter-comparison
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

---

## 📂 File Structure

- **`app.py`**: The main script for the Streamlit application.
- **`UFC_Fighter_Analysis.ipynb`**: Jupyter Notebook containing the data cleaning and exploratory data analysis (EDA).
- **`ufc-fighters-statistics-CLEANED.csv`**: The cleaned dataset used by the app.
- **`requirements.txt`**: A list of necessary Python libraries for the project.