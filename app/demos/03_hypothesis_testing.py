"""Демо: проверка гипотез — α, β, мощность, p-value и A/A-симуляция."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import streamlit as st

st.title("🎯 Проверка гипотез: p-value, ошибки, мощность")
st.caption("Блок 1 · Модуль 1.5 — сердце любого A/B теста.")

tab1, tab2 = st.tabs(["📈 α, β и мощность", "🔁 A/A-симуляция (ошибка I рода)"])

with tab1:
    st.markdown(
        "Две гипотезы = два распределения тестовой статистики: при **H₀** (эффекта нет) и при **H₁** (эффект есть). "
        "Порог α режет правый хвост H₀ (ложные срабатывания). Всё, что правее порога под H₁ — это **мощность**."
    )
    c = st.columns(3)
    effect = c[0].slider("Величина эффекта (сдвиг H₁), σ", 0.0, 4.0, 2.0, 0.1)
    alpha = c[1].select_slider("Уровень α", [0.01, 0.05, 0.10], 0.05)
    tails = c[2].radio("Тип теста", ["двусторонний", "односторонний"], horizontal=True)

    xs = np.linspace(-4, 8, 600)
    h0 = stats.norm.pdf(xs, 0, 1)
    h1 = stats.norm.pdf(xs, effect, 1)
    if tails == "односторонний":
        crit = stats.norm.ppf(1 - alpha)
        power = 1 - stats.norm.cdf(crit - effect)
        crit_lines = [crit]
    else:
        crit = stats.norm.ppf(1 - alpha / 2)
        power = 1 - stats.norm.cdf(crit - effect) + stats.norm.cdf(-crit - effect)
        crit_lines = [crit, -crit]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(xs, h0, color="#64748b", label="H₀ (эффекта нет)")
    ax.plot(xs, h1, color="#6366f1", label="H₁ (эффект есть)")
    for cl in crit_lines:
        ax.axvline(cl, color="#ef4444", ls="--", lw=1)
    reject = np.zeros_like(xs, dtype=bool)
    for cl in crit_lines:
        reject |= xs >= cl if cl > 0 else xs <= cl
    ax.fill_between(xs, 0, h0, where=reject, color="#ef4444", alpha=.3, label="α: ложные срабатывания")
    ax.fill_between(xs, 0, h1, where=reject, color="#22c55e", alpha=.3, label="мощность 1−β")
    ax.legend(fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_yticks([])
    st.pyplot(fig)

    c1, c2, c3 = st.columns(3)
    c1.metric("α (ошибка I рода)", f"{alpha:.0%}")
    c2.metric("Мощность 1−β", f"{power:.0%}")
    c3.metric("β (ошибка II рода)", f"{1-power:.0%}")
    st.info("Двигайте эффект → видно, что мощность растёт. Уменьшайте α → мощность падает при том же эффекте. "
            "Единственный способ иметь и малую α, и высокую мощность при малом эффекте — **больше выборка**.",
            icon="💡")

with tab2:
    st.markdown(
        "**A/A-тест:** обе группы из *одного* распределения, реального эффекта нет. "
        "Прогоним много таких тестов и посмотрим долю «значимых» (p < α). Она должна быть ≈ α — "
        "это и есть ошибка I рода в чистом виде."
    )
    c = st.columns(3)
    n = c[0].slider("Размер группы", 50, 5000, 1000, key="aa_n")
    alpha2 = c[1].select_slider("α", [0.01, 0.05, 0.10], 0.05, key="aa_a")
    trials = c[2].slider("Число A/A-тестов", 500, 20000, 5000, step=500)

    rng = np.random.default_rng(123)
    a = rng.normal(0, 1, size=(trials, n))
    b = rng.normal(0, 1, size=(trials, n))
    _, pvals = stats.ttest_ind(a, b, axis=1)
    false_pos = (pvals < alpha2).mean()

    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.hist(pvals, bins=20, color="#6366f1", edgecolor="white")
    ax.axvline(alpha2, color="#ef4444", ls="--", label=f"порог α={alpha2}")
    ax.set_xlabel("p-value")
    ax.set_title("p-value равномерны при истинной H₀")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig)

    st.metric("Доля «значимых» A/A-тестов", f"{false_pos:.1%}",
              delta=f"ожидалось ≈ {alpha2:.0%}", delta_color="off")
    st.warning("Вывод: «статистическая значимость» возникает от чистого шума в ~α случаев. "
               "Поэтому нельзя гнаться за p<0.05 и подглядывать (см. демо «Проблема peeking»).", icon="⚠️")
