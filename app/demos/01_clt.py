"""Демо: Центральная предельная теорема и закон больших чисел."""
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("📊 ЦПТ и закон больших чисел")
st.caption("Блок 1 · Модуль 1.3 — фундамент, на котором стоят все A/B тесты.")

st.markdown(
    """
**Идея.** Возьмём *любое* (даже уродливое) распределение. Будем много раз брать из него выборку
размера **n** и считать её среднее. Распределение этих средних всё равно станет **нормальным** —
это и есть Центральная предельная теорема. А стандартная ошибка среднего падает как `σ/√n`.
    """
)

col = st.columns(3)
dist = col[0].selectbox(
    "Исходное распределение",
    ["Логнормальное (выручка)", "Экспоненциальное (время)", "Бернулли (конверсия)", "Равномерное"],
)
n = col[1].slider("Размер выборки n", 1, 500, 30)
reps = col[2].slider("Число повторов", 200, 20000, 5000, step=200)

rng = np.random.default_rng(42)


def draw(size):
    if dist.startswith("Логнормальное"):
        return rng.lognormal(mean=1.0, sigma=1.0, size=size)
    if dist.startswith("Экспоненциальное"):
        return rng.exponential(scale=2.0, size=size)
    if dist.startswith("Бернулли"):
        return rng.binomial(1, 0.2, size=size).astype(float)
    return rng.uniform(0, 1, size=size)


population = draw(100000)
means = draw((reps, n)).mean(axis=1)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].hist(population, bins=60, color="#94a3b8", edgecolor="none")
axes[0].set_title("Исходное распределение (популяция)")
axes[0].set_xlabel("значение")

axes[1].hist(means, bins=50, color="#6366f1", edgecolor="none", density=True)
mu, sd = means.mean(), means.std()
xs = np.linspace(means.min(), means.max(), 200)
axes[1].plot(xs, np.exp(-0.5 * ((xs - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi)),
             color="#ef4444", lw=2, label="нормальная аппроксимация")
axes[1].set_title(f"Распределение средних (n={n})")
axes[1].set_xlabel("выборочное среднее")
axes[1].legend()
for ax in axes:
    ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
st.pyplot(fig)

c1, c2, c3 = st.columns(3)
c1.metric("Истинное среднее популяции", f"{population.mean():.3f}")
c2.metric("Среднее из средних", f"{mu:.3f}")
c3.metric("Стандартная ошибка (эмпир.)", f"{sd:.4f}",
          help="Сравните с теоретической σ/√n — они близки.")

st.success(
    f"Теоретическая SE = σ/√n = {population.std()/np.sqrt(n):.4f}. "
    "Увеличьте n — колокол станет уже (точность растёт как √n), и форма выправится в нормальную "
    "даже для скошенной выручки.",
    icon="✅",
)

with st.expander("💡 Почему это важно для A/B тестов"):
    st.markdown(
        "- t-тест и z-тест сравнивают **средние** групп. Благодаря ЦПТ они работают даже для "
        "скошенных метрик (выручка, время), если выборка достаточно большая.\n"
        "- `SE = σ/√n` — почему для маленького эффекта нужна большая выборка (Модуль 2.4).\n"
        "- Уменьшить σ (например, через CUPED) = сузить SE без роста n (Модуль 4.1)."
    )
