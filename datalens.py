# Imports
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="DataLens - Streamlit Data Analyzer", layout="centered")

# 1. Title and Subheader
st.title("🔍 DataLens")
st.subheader("Explore, Clean & Visualize Your Data Instantly")

# 2. Upload Dataset
upload = st.file_uploader("📂 Upload Your Dataset (CSV format)", type=["csv"])

if upload:
    try:
        data = pd.read_csv(upload)
        st.success("✅ Dataset Uploaded Successfully!")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # 3. Preview Dataset
    with st.expander("👀 Preview Dataset"):
        view_option = st.radio("Select view:", ("Head", "Tail"))
        st.write(data.head() if view_option == "Head" else data.tail())

    # 4. Datatypes
    with st.expander("🔤 Column Data Types"):
        st.write(data.dtypes)

    # 5. Shape of Dataset
    with st.expander("📐 Dataset Dimensions"):
        dim_option = st.radio("Select dimension to view:", ('Rows', 'Columns'))
        st.write(f"Number of {dim_option}: {data.shape[0] if dim_option == 'Rows' else data.shape[1]}")

    # 6. Null Values
    with st.expander("🧩 Missing Values"):
        if data.isnull().values.any():
            st.warning("⚠️ This dataset contains missing values.")
            st.write("**Missing values per column:**")
            st.write(data.isnull().sum())

            fig, ax = plt.subplots()
            sns.heatmap(data.isnull(), cbar=False, cmap="magma", ax=ax)
            st.pyplot(fig)

            # Handle null data
            null_action = st.selectbox(
                "How would you like to handle missing values?",
                ("Do Nothing", "Remove Rows with Nulls")
            )
            if null_action == "Remove Rows with Nulls":
                data.dropna(inplace=True)
                st.success("✅ All rows with null values have been removed.")
        else:
            st.success("🎉 No missing values found!")

    # 7. Duplicate Values
    with st.expander("🌀 Duplicate Values"):
        if data.duplicated().any():
            st.warning("This dataset contains duplicate rows.")
            dup_action = st.selectbox("Do you want to remove duplicates?", ("Select", "Yes", "No"))
            if dup_action == "Yes":
                data.drop_duplicates(inplace=True)
                st.success("✅ Duplicate rows removed successfully.")
            elif dup_action == "No":
                st.info("Duplicates kept as-is.")
        else:
            st.success("No duplicate rows found.")

    # 8. Summary Statistics
    with st.expander("📈 Summary Statistics"):
        st.write(data.describe(include='all'))

    # 9. Quick Visualization
    with st.expander("📊 Quick Visualization"):
        st.markdown("Generate a simple visualization from your dataset:")
        numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()

        if len(numeric_cols) >= 1:
            col1 = st.selectbox("Select X-axis:", options=numeric_cols)
            col2 = st.selectbox("Select Y-axis (optional):", options=["None"] + numeric_cols)

            if st.button("Plot Chart"):
                fig, ax = plt.subplots()
                if col2 != "None":
                    sns.scatterplot(x=data[col1], y=data[col2], ax=ax)
                    ax.set_title(f"{col1} vs {col2}")
                else:
                    sns.histplot(data[col1], kde=True, ax=ax)
                    ax.set_title(f"Distribution of {col1}")
                st.pyplot(fig)
        else:
            st.info("No numeric columns available for plotting.")

    # 10. Download Cleaned Dataset
    with st.expander("💾 Download Cleaned Dataset"):
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

# 11. About Section
if st.button("ℹ️ About App"):
    st.info("Built with ❤️ using Streamlit. Empowering data exploration, cleaning, and visualization.")

# 12. Author
if st.checkbox("👤 By"):
    st.success("Developed by Tinotenda Maseura")
