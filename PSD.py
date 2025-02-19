import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(layout="wide")

# URL Direct Link dari Imgur
image_url = "https://i.imgur.com/cab82rH.png"

# Menampilkan gambar dengan lebar yang ditentukan (misalnya 300 piksel)
st.image(image_url, width=500)


# Load data
data = pd.read_excel(r"E:\Stunting Dataset (1).xlsx")

# Periksa apakah ada nilai yang hilang
missing_values = data.isnull().sum()
print(missing_values)

# Mengonversi kolom kategorikal menjadi numerik
label_encoder = LabelEncoder()
data['ASI Eksklusif'] = label_encoder.fit_transform(data['ASI Eksklusif'])
data['Sex'] = label_encoder.fit_transform(data['Sex'])

# Memisahkan fitur (X) dan target (y)
X = data.drop(columns=['Stunting'])
y = data['Stunting']

# Memisahkan data menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inisialisasi dan fitting StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Inisialisasi model Regresi Logistik
logistic_model = LogisticRegression()
logistic_model.fit(X_train_scaled, y_train)

# Inisialisasi model Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# Inisialisasi model Gradient Boosting
gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
gb_model.fit(X_train_scaled, y_train)

# Menghitung akurasi masing-masing model
logistic_accuracy = accuracy_score(y_test, logistic_model.predict(X_test_scaled))
rf_accuracy = accuracy_score(y_test, rf_model.predict(X_test_scaled))
gb_accuracy = accuracy_score(y_test, gb_model.predict(X_test_scaled))

# Memilih model dengan akurasi tertinggi
best_model = max((logistic_model, rf_model, gb_model), key=lambda model: accuracy_score(y_test, model.predict(X_test_scaled)))

print(f"The best model for predicting stunting is {best_model.__class__.__name__} with an accuracy of {max(logistic_accuracy, rf_accuracy, gb_accuracy)}")

# Define a function to predict stunting based on input features
def predict_stunting(sex, age, birth_weight, birth_length, body_weight, body_length, asix):
    input_data = scaler.transform([[sex, age, birth_weight, birth_length, body_weight, body_length, asix]])
    probability_stunting = best_model.predict_proba(input_data)[0][1]  # Probabilitas stunting
    return probability_stunting

# Sidebar with menu
selected = option_menu(
    menu_title="Menu",
    options=['Home', 'Predict','Info', 'Tentang Data'],
    icons=["house","activity","book","envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Home page
if selected == 'Home':
    st.subheader('Tentang Aplikasi')
    st.write('Aplikasi ini memprediksi stunting pada anak berdasarkan berbagai faktor.')
    st.write('Aplikasi ini menggunakan algoritma pembelajaran mesin untuk memprediksi kemungkinan terjadinya stunting.')
    st.image("https://rsudblora.blorakab.go.id/wp-content/uploads/2022/12/apa-itu-stunting-1024x576.jpeg", caption="My Image", use_column_width=True)
    
# Predict page
if selected == 'Predict':
    st.subheader('Input Data')
    sex = st.sidebar.selectbox('Sex', ['Male', 'Female'])
    age = st.sidebar.number_input('Age', min_value=0, max_value=100, value=0, step=1)
    birth_weight = st.sidebar.number_input('Birth Weight', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    birth_length = st.sidebar.number_input('Birth Length', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    body_weight = st.sidebar.number_input('Body Weight', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    body_length = st.sidebar.number_input('Body Length', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    asix = st.sidebar.selectbox('ASI Eksklusif', ['No', 'Yes'])

    # Convert sex and ASI Eksklusif to numerical values
    sex_num = 1 if sex == 'Female' else 0
    asix_num = 1 if asix == 'Yes' else 0

    # Predict stunting
    if st.button('Predict'):
        if age == 0 or birth_weight == 0.0 or birth_length == 0.0 or body_weight == 0.0 or body_length == 0.0:
            st.write("Lengkapi data di atas.")
        else:
            probability_stunting = predict_stunting(sex_num, age, birth_weight, birth_length, body_weight, body_length, asix_num)
            
            # Menentukan prediksi berdasarkan probabilitas
            if probability_stunting > 0.5:
                st.write('Anak mengalami stunting.')
            else:
                st.write('Anak tidak mengalami stunting.')
            
            st.write(f"Probability of stunting: {probability_stunting}")
            st.write(f"Probability of not stunting: {1 - probability_stunting}")

# Info page
if selected == 'Info':
    st.subheader('FAQ')
    st.write('Apa itu stunting?')
    st.write("Stunting adalah kondisi di mana tinggi badan seorang anak lebih rendah dari tinggi yang diharapkan untuk usianya.")
    st.write('Ini merupakan indikator dari kekurangan gizi kronis.')

    st.write('Mengapa stunting menjadi masalah?')
    st.write('Stunting dapat memiliki dampak negatif pada perkembangan fisik dan kognitif seorang anak.')
    st.write('Hal ini juga dapat menyebabkan performa buruk di sekolah dan pendapatan yang lebih rendah di masa dewasa.')

    st.write('Bagaimana stunting diukur?')
    st.write('Stunting diukur sebagai Z-score tinggi-untuk-usia, yang merupakan ukuran standar tinggi badan seorang anak relatif terhadap usia dan jenis kelamin mereka.')
    st.write('Anak-anak dengan Z-score di bawah -2 dianggap mengalami stunting.')

    st.write('Bagaimana stunting dapat dicegah?')
    st.write('Stunting dapat dicegah melalui berbagai intervensi, seperti meningkatkan gizi selama kehamilan dan masa kanak-kanak, mempromosikan pemberian ASI, dan menyediakan akses ke air bersih dan sanitasi.')

# Tentang Data page
if selected == 'Tentang Data':
    st.subheader('Data Overview')
    st.write('Dataset ini berisi informasi tentang status stunting anak berdasarkan berbagai faktor.')
    
    # Menambahkan dropdown
    analysis_option = st.selectbox("Select Analysis Option", ["Informasi data", "Grafik Coxplot", "Histogram"])

    # Memperbarui berdasarkan pilihan dropdown
    if analysis_option == "Informasi data":
        st.subheader("Yuk kita Liat datanya")
        st.write(data.head())
        st.subheader("Serba Serbi Data")
        st.write(data.describe())
        st.write(f'Total number of data points: {len(data)}') 
        st.write('Columns:')
        st.write(X.columns.tolist())

    elif analysis_option == "Grafik Coxplot":
        st.subheader('Coxplot Graph')
        # Tambahkan kode untuk grafik Coxplot
        st.write('Coxplot showing relationship between multiple variables')
        selected_features = st.multiselect('Select features for Coxplot:', options=X.columns)
        if selected_features:
            coxplot_data = data[selected_features]
            pair_grid = sns.pairplot(coxplot_data, diag_kind='kde')
            # Render PairGrid object using st.pyplot()
            st.pyplot(pair_grid.fig)

    elif analysis_option == "Histogram":
        st.subheader('Histogram Graph')
        # Tambahkan kode untuk histogram
        st.write('The following histogram shows the distribution of a selected feature:')
        selected_feature = st.selectbox('Select a feature for histogram:', options=X.columns)

        # Menonaktifkan peringatan PyplotGlobalUseWarning
        st.set_option('deprecation.showPyplotGlobalUse', False)
    
        # Create histogram using Matplotlib
        plt.hist(data[selected_feature], bins='auto', color='cadetblue', alpha=0.7, rwidth=0.85)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title('Histogram of ' + selected_feature)
        st.pyplot()
