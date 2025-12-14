import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# --- Load CSV ---
df = pd.read_csv("world_pop(str).csv")
df = df.rename(columns={
    'Year': 'year',
    'Population': 'population',
    'Yearly % Change': 'yearly_change_percent',
    'Net Change': 'net_change',
    'Density (P/Km²)': 'density_per_km2'
})

df['yearly_change_percent'] = df['yearly_change_percent'].astype(str).str.replace('%','').str.replace(',','').astype(float)
df['population'] = df['population'].astype(str).str.replace(',','').astype(float)
df['net_change'] = df['net_change'].astype(str).str.replace(',','').astype(float)
df['density_per_km2'] = df['density_per_km2'].astype(str).str.replace(',','').astype(float)

# --- Load GDP Model ---
rf_model = joblib.load("gdp_model.pkl")
le_country = joblib.load("country_encoder.pkl")
le_region = joblib.load("region_encoder.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# --- Sidebar for Mode Selection ---
mode = st.sidebar.selectbox("Select Mode:", ["Population Dashboard", "GDP Prediction"])

if mode == "Population Dashboard":
    # --- Slider for Year Range ---
    year_min = int(df['year'].min())
    year_max = int(df['year'].max())
    selected_range = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))

    # --- Filtered Data ---
    filtered_df = df[(df['year'] >= selected_range[0]) & (df['year'] <= selected_range[1])]

    # --- Visualizations ---
   

    st.title("🌍 GDP per Capita Prediction")

    option = st.selectbox(
        "Choose Visualization:",
        [
            "Population Over Time",
            "Top 5 Growth Years",
            "Top 10 Population Years",
            "Top 10 Population Increase Years",
            "Growth Rate Line Chart",
            "Population vs Density"
        ]
    )

    # --- Functions (same as before) ---
    def visualize_population_over_time():
        if not filtered_df.empty:
            fig, ax = plt.subplots(figsize=(12,6))
            ax.plot(filtered_df['year'], filtered_df['population'], marker='o', color='blue')
            ax.set_title('World Population Over Time', fontsize=16)
            ax.set_xlabel('Year')
            ax.set_ylabel('Population')
            ax.grid(True)
            st.pyplot(fig)

    def visualize_top_growth_years():
        if not filtered_df.empty:
            top5 = filtered_df.nlargest(5, 'yearly_change_percent').sort_values('yearly_change_percent')
            fig, ax = plt.subplots(figsize=(10,6))
            ax.barh(top5['year'].astype(str), top5['yearly_change_percent'], color='green')
            ax.set_title('Top 5 Years by Population Growth %', fontsize=16)
            ax.set_xlabel('Growth Rate (%)')
            ax.set_ylabel('Year')
            st.pyplot(fig)

    def top_population_years():
        if not filtered_df.empty:
            top10 = filtered_df.nlargest(10, 'population').sort_values('population')
            fig, ax = plt.subplots(figsize=(10,6))
            ax.barh(top10['year'].astype(str), top10['population'], color='orange')
            ax.set_title('Top 10 Years by Population', fontsize=16)
            ax.set_xlabel('Population')
            ax.set_ylabel('Year')
            st.pyplot(fig)

    def top_population_increase_years():
        if not filtered_df.empty:
            top10 = filtered_df.nlargest(10, 'net_change').sort_values('net_change')
            fig, ax = plt.subplots(figsize=(10,6))
            ax.barh(top10['year'].astype(str), top10['net_change'], color='green')
            ax.set_title('Top 10 Years by Population Increase', fontsize=16)
            ax.set_xlabel('Population Increase')
            ax.set_ylabel('Year')
            st.pyplot(fig)

    def growth_rate_line_chart():
        if not filtered_df.empty:
            fig, ax = plt.subplots(figsize=(12,6))
            ax.plot(filtered_df['year'], filtered_df['yearly_change_percent'], marker='o', color='blue')
            top3 = filtered_df.nlargest(3, 'yearly_change_percent')
            ax.scatter(top3['year'], top3['yearly_change_percent'], color='red', s=100, label='Top Growth')
            ax.set_title('Yearly Population Growth %', fontsize=16)
            ax.set_xlabel('Year')
            ax.set_ylabel('Growth %')
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    def population_vs_density():
        if not filtered_df.empty:
            fig, ax1 = plt.subplots(figsize=(12,6))
            ax1.plot(filtered_df['year'], filtered_df['population'], color='blue', label='Population')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Population', color='blue')
            ax2 = ax1.twinx()
            ax2.plot(filtered_df['year'], filtered_df['density_per_km2'], color='purple', linestyle='--', label='Density')
            ax2.set_ylabel('Density (people/km²)', color='purple')
            ax1.grid(True)
            fig.tight_layout()
            st.pyplot(fig)

    # --- Execute selected visualization ---
    if option == "Population Over Time":
        visualize_population_over_time()
    elif option == "Top 5 Growth Years":
        visualize_top_growth_years()
    elif option == "Top 10 Population Years":
        top_population_years()
    elif option == "Top 10 Population Increase Years":
        top_population_increase_years()
    elif option == "Growth Rate Line Chart":
        growth_rate_line_chart()
    elif option == "Population vs Density":
        population_vs_density()

elif mode == "GDP Prediction":
    st.title("💰 GDP per Capita Prediction")

    # --- User Inputs ---
 

# ===============================
# Select boxes
# ===============================
import streamlit as st
import pandas as pd
import joblib

# ===============================
# Load model & encoders
# ===============================
rf_model = joblib.load("gdp_model.pkl")
le_country = joblib.load("country_encoder.pkl")
le_region = joblib.load("region_encoder.pkl")
le_climate = joblib.load("climate_encoder.pkl")
feature_columns = joblib.load("feature_columns.pkl")

st.title("🌍 GDP per Capita Prediction")

# ===============================
# Select boxes for categorical
# ===============================
country = st.selectbox("Country", le_country.classes_)
region = st.selectbox("Region", le_region.classes_)
climate = st.selectbox("Climate", le_climate.classes_)

country_encoded = le_country.transform([country])[0]
region_encoded = le_region.transform([region])[0]
climate_encoded = le_climate.transform([climate])[0]

# ===============================
# Numeric inputs
# ===============================
population = st.number_input("Population", min_value=0)
area = st.number_input("Area (sq. mi.)", min_value=0.0)
pop_density = st.number_input("Population Density")
coastline = st.number_input("Coastline ratio")
net_migration = st.number_input("Net migration")
infant_mortality = st.number_input("Infant mortality")
literacy = st.number_input("Literacy (%)")
phones = st.number_input("Phones per 1000")
arable = st.number_input("Arable (%)")
crops = st.number_input("Crops (%)")
other = st.number_input("Other (%)")
birthrate = st.number_input("Birthrate")
deathrate = st.number_input("Deathrate")
agriculture = st.number_input("Agriculture")
industry = st.number_input("Industry")
service = st.number_input("Service")

# ===============================
# Prediction button
# ===============================
if st.button("Predict GDP"):
    try:
        # Create input DataFrame
        input_df = pd.DataFrame([{
            'Population': population,
            'Area (sq. mi.)': area,
            'Pop. Density (per sq. mi.)': pop_density,
            'Coastline (coast/area ratio)': coastline,
            'Net migration': net_migration,
            'Infant mortality (per 1000 births)': infant_mortality,
            'Literacy (%)': literacy,
            'Phones (per 1000)': phones,
            'Arable (%)': arable,
            'Crops (%)': crops,
            'Other (%)': other,
            'Birthrate': birthrate,
            'Deathrate': deathrate,
            'Agriculture': agriculture,
            'Industry': industry,
            'Service': service,
            'Country_num': country_encoded,
            'Region_num': region_encoded,
            'Climate_num': climate_encoded
        }])

        # Match feature order with training
        input_df = input_df[feature_columns]

        # Predict
        prediction = rf_model.predict(input_df)[0]

        st.success(f"💰 Predicted GDP per Capita: ${prediction:,.0f}")

    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")
