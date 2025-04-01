import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Заголовок додатка
st.title("Щоденник здоров'я")

# Завантаження даних
if "health_data" not in st.session_state:
    st.session_state.health_data = pd.DataFrame(columns=["Дата", "Тиск", "Пульс", "Вага", "Цукор", "Холестерин", "Сечова кислота"])

# Форма для введення даних
st.subheader("Введіть ваші показники")
pressure = st.text_input("Тиск (наприклад, 120/80)")
pulse = st.number_input("Пульс", min_value=30, max_value=200, step=1)
weight = st.number_input("Вага (кг)", min_value=30.0, max_value=200.0, step=0.1)
sugar = st.number_input("Рівень цукру в крові (ммоль/л)", min_value=2.0, max_value=20.0, step=0.1)
cholesterol = st.number_input("Холестерин (ммоль/л)", min_value=2.0, max_value=10.0, step=0.1)
uric_acid = st.number_input("Сечова кислота (ммоль/л)", min_value=100.0, max_value=600.0, step=1.0)

if st.button("Зберегти"):
    new_data = pd.DataFrame({
        "Дата": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "Тиск": [pressure],
        "Пульс": [pulse],
        "Вага": [weight],
        "Цукор": [sugar],
        "Холестерин": [cholesterol],
        "Сечова кислота": [uric_acid]
    })
    st.session_state.health_data = pd.concat([st.session_state.health_data, new_data], ignore_index=True)
    st.success("Дані збережено!")

# Відображення історії вимірювань
st.subheader("Історія вимірювань")
st.dataframe(st.session_state.health_data)

# Відображення графіків
st.subheader("Графіки змін показників")
fig, ax = plt.subplots()
st.session_state.health_data["Дата"] = pd.to_datetime(st.session_state.health_data["Дата"], format="%Y-%m-%d %H:%M")
st.session_state.health_data = st.session_state.health_data.sort_values("Дата")

ax.plot(st.session_state.health_data["Дата"], st.session_state.health_data["Пульс"], label="Пульс")
ax.plot(st.session_state.health_data["Дата"], st.session_state.health_data["Вага"], label="Вага")
ax.plot(st.session_state.health_data["Дата"], st.session_state.health_data["Цукор"], label="Цукор")
ax.plot(st.session_state.health_data["Дата"], st.session_state.health_data["Холестерин"], label="Холестерин")
ax.plot(st.session_state.health_data["Дата"], st.session_state.health_data["Сечова кислота"], label="Сечова кислота")

ax.set_xlabel("Дата")
ax.set_ylabel("Значення")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# Рекомендації
st.subheader("Рекомендації")
recommendations = []
if pulse < 50 or pulse > 100:
    recommendations.append("Перевірте серцевий ритм та зверніться до лікаря.")
if weight > 100:
    recommendations.append("Зверніть увагу на раціон та фізичну активність.")
if sugar > 7.0:
    recommendations.append("Контролюйте рівень цукру та уникайте швидких вуглеводів.")
if cholesterol > 5.0:
    recommendations.append("Обмежте жирну їжу та перегляньте дієту.")
if uric_acid > 400:
    recommendations.append("Можливий ризик подагри – зменшіть вживання м'яса та алкоголю.")

if recommendations:
    for rec in recommendations:
        st.warning(rec)
else:
    st.success("Ваші показники в межах норми!")
