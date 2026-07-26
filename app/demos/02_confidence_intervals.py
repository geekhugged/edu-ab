"""Демо: доверительные интервалы — аналитика vs bootstrap, и правильная интерпретация."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import streamlit as st

st.title("📏 Доверительные интервалы")
st.caption("Блок 1 · Модуль 1.4 — как выражать неопределённость, а не только точку.")

st.markdown(
    """
95% CI **не** значит «параметр здесь с вероятностью 95%». Правильно: *если повторять эксперимент много раз,
95% построенных интервалов накроют истинное значение*. Ниже — симуляция ровно этой идеи + сравнение
аналитического CI с bootstrap.
    """
)

tab1, tab2 = st.tabs(["🎯 Что значит «95%»", "🥾 Bootstrap vs формула"])

with tab1:
    c = st.columns(3)
    true_mean = c[0].slider("Истинное среднее", 0.0, 10.0, 5.0)
    n = c[1].slider("Размер выборки", 10, 500, 50)
    n_ci = c[2].slider("Сколько экспериментов показать", 20, 200, 50)
    rng = np.random.default_rng(7)
    covered = 0
    fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(n_ci):
        sample = rng.normal(true_mean, 2.0, n)
        m = sample.mean()
        se = sample.std(ddof=1) / np.sqrt(n)
        lo, hi = m - 1.96 * se, m + 1.96 * se
        ok = lo <= true_mean <= hi
        covered += ok
        ax.plot([lo, hi], [i, i], color="#22c55e" if ok else "#ef4444", lw=1.5)
        ax.plot(m, i, "o", color="#334155", ms=2)
    ax.axvline(true_mean, color="#6366f1", lw=2, label="истинное среднее")
    ax.set_yticks([])
    ax.set_xlabel("значение")
    ax.legend(loc="upper right")
    ax.spines[["top", "right", "left"]].set_visible(False)
    st.pyplot(fig)
    st.metric("Доля интервалов, накрывших истину", f"{covered/n_ci:.0%}",
              help="Должно колебаться около 95%. Красные — 'промахи'.")

with tab2:
    st.markdown("Для **медианы** аналитической формулы нет — bootstrap выручает.")
    c = st.columns(2)
    n = c[0].slider("Размер выборки ", 20, 2000, 300, key="bs_n")
    b = c[1].slider("Число bootstrap-ресэмплов", 500, 10000, 3000, step=500)
    rng = np.random.default_rng(1)
    data = rng.lognormal(1.0, 0.9, n)  # скошенная «выручка»

    # аналитический CI для среднего
    m, se = data.mean(), data.std(ddof=1) / np.sqrt(n)
    ci_mean = (m - 1.96 * se, m + 1.96 * se)

    # bootstrap CI для среднего и медианы
    idx = rng.integers(0, n, size=(b, n))
    boot = data[idx]
    boot_means = boot.mean(axis=1)
    boot_medians = np.median(boot, axis=1)
    ci_boot_mean = np.percentile(boot_means, [2.5, 97.5])
    ci_boot_med = np.percentile(boot_medians, [2.5, 97.5])

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(boot_means, bins=40, alpha=.6, color="#6366f1", label="bootstrap средних")
    ax.hist(boot_medians, bins=40, alpha=.6, color="#f59e0b", label="bootstrap медиан")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig)

    st.write("**95% CI для среднего** (аналитический):",
             f"[{ci_mean[0]:.3f}, {ci_mean[1]:.3f}]")
    st.write("**95% CI для среднего** (bootstrap):",
             f"[{ci_boot_mean[0]:.3f}, {ci_boot_mean[1]:.3f}]  ← почти совпадает с формулой")
    st.write("**95% CI для медианы** (только bootstrap):",
             f"[{ci_boot_med[0]:.3f}, {ci_boot_med[1]:.3f}]")
    st.success("Bootstrap — универсальный способ получить CI для любой статистики без вывода формул.", icon="✅")
