"""edu-ab — интерактивные демо по A/B тестированию.

Запуск:
    pip install -r requirements.txt
    streamlit run streamlit_app.py
"""
import streamlit as st

st.set_page_config(
    page_title="edu-ab · Демо по A/B тестированию",
    page_icon="🧪",
    layout="wide",
)


def home():
    st.title("🧪 edu-ab — интерактивные демо по A/B тестированию")
    st.markdown(
        """
Это учебный тренажёр к программе **edu-ab**. Каждое демо соответствует теме из
[программы](https://github.com/geekhugged/edu-ab) — двигайте слайдеры и смотрите,
как меняются распределения, доверительные интервалы, ошибки и решения.

**Как пользоваться:** выберите демо в меню слева, прочитайте короткую вводную наверху страницы,
затем экспериментируйте с параметрами. Идея — *почувствовать* статистику, а не заучить формулу.
        """
    )
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Блок 1 — Статистика")
        st.markdown(
            "- 📊 ЦПТ и ЗБЧ\n- 📏 Доверительные интервалы\n- 🎯 Проверка гипотез (p-value, мощность, A/A)"
        )
        st.subheader("Блок 2 — Основы A/B")
        st.markdown("- 🧮 Калькулятор размера выборки\n- ⚖️ Статистические критерии")
    with c2:
        st.subheader("Блок 3 — Подводные камни")
        st.markdown("- 👀 Проблема peeking\n- 🔀 SRM-чек\n- 🎛️ Множественные сравнения")
        st.subheader("Блок 4 — Продвинутое")
        st.markdown("- ⚡ CUPED (снижение дисперсии)\n- 🃏 Байес и бандиты")

    st.info(
        "Совет: начните с «ЦПТ» и «Проверка гипотез» — на них держатся все остальные демо.",
        icon="💡",
    )


PAGES = [
    st.Page(home, title="Главная", icon="🏠", default=True),
    st.Page("demos/01_clt.py", title="ЦПТ и ЗБЧ", icon="📊"),
    st.Page("demos/02_confidence_intervals.py", title="Доверительные интервалы", icon="📏"),
    st.Page("demos/03_hypothesis_testing.py", title="Проверка гипотез", icon="🎯"),
    st.Page("demos/04_sample_size.py", title="Калькулятор выборки", icon="🧮"),
    st.Page("demos/05_stat_tests.py", title="Статкритерии", icon="⚖️"),
    st.Page("demos/06_peeking.py", title="Проблема peeking", icon="👀"),
    st.Page("demos/07_srm.py", title="SRM-чек", icon="🔀"),
    st.Page("demos/08_multiple_comparisons.py", title="Множественные сравнения", icon="🎛️"),
    st.Page("demos/09_cuped.py", title="CUPED", icon="⚡"),
    st.Page("demos/10_bayes_bandits.py", title="Байес и бандиты", icon="🃏"),
]

st.navigation(
    {
        "О тренажёре": [PAGES[0]],
        "Блок 1 · Статистика": PAGES[1:4],
        "Блок 2 · Основы A/B": PAGES[4:6],
        "Блок 3 · Подводные камни": PAGES[6:9],
        "Блок 4 · Продвинутое": PAGES[9:11],
    }
).run()
