"""Демо: CUPED — снижение дисперсии за счёт предэкспериментальной ковариаты."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import streamlit as st

st.title("⚡ CUPED — снижение дисперсии")
st.caption("Блок 4 · Модуль 4.1 — тот же тест, но чувствительнее и быстрее.")

st.markdown(
    r"""
**Идея CUPED.** У пользователя есть метрика *до* эксперимента (напр. активность на прошлой неделе),
коррелирующая с метрикой во время теста. Вычтем предсказуемую часть:
$$Y_{cuped} = Y - \theta \,(X - \bar X),\quad \theta = \frac{\mathrm{Cov}(Y,X)}{\mathrm{Var}(X)}$$
Среднее не смещается, а дисперсия падает в $(1-\rho^2)$ раз. Значит — уже CI и меньше нужная выборка.
    """
)

c = st.columns(3)
n = c[0].slider("Размер группы", 200, 20000, 3000, step=100)
corr = c[1].slider("Корреляция с пред-периодом ρ", 0.0, 0.95, 0.7, 0.05)
true_effect = c[2].slider("Истинный эффект B, ед.", 0.0, 2.0, 0.3, 0.05)

rng = np.random.default_rng(11)
# ковариата X (пред-период) и метрика Y с заданной корреляцией
X = rng.normal(0, 1, 2 * n)
noise = rng.normal(0, 1, 2 * n)
Y = corr * X + np.sqrt(max(1 - corr**2, 1e-9)) * noise
group = np.array([0] * n + [1] * n)
Y = Y + group * true_effect  # добавляем эффект группе B

# CUPED-корректировка
theta = np.cov(Y, X)[0, 1] / np.var(X)
Y_cuped = Y - theta * (X - X.mean())

def analyze(vals):
    a, b = vals[group == 0], vals[group == 1]
    diff = b.mean() - a.mean()
    se = np.sqrt(a.var(ddof=1) / n + b.var(ddof=1) / n)
    t, p = stats.ttest_ind(b, a, equal_var=False)
    return diff, se, p

d0, se0, p0 = analyze(Y)
d1, se1, p1 = analyze(Y_cuped)
var_reduction = 1 - (se1**2) / (se0**2)

c1, c2, c3 = st.columns(3)
c1.metric("Обычный тест — SE эффекта", f"{se0:.4f}", f"p={p0:.4f}")
c2.metric("CUPED — SE эффекта", f"{se1:.4f}", f"p={p1:.4f}")
c3.metric("Снижение дисперсии", f"{var_reduction:.0%}", help="≈ ρ². Столько же — эконом. выборки.")

fig, ax = plt.subplots(figsize=(10, 4))
ax.errorbar([0], [d0], yerr=[1.96 * se0], fmt="o", color="#94a3b8", capsize=6,
            label="обычный t-тест", ms=8)
ax.errorbar([1], [d1], yerr=[1.96 * se1], fmt="o", color="#6366f1", capsize=6,
            label="CUPED", ms=8)
ax.axhline(true_effect, color="#22c55e", ls="--", label="истинный эффект")
ax.axhline(0, color="#e5e7eb")
ax.set_xlim(-0.5, 1.5)
ax.set_xticks([0, 1])
ax.set_xticklabels(["обычный", "CUPED"])
ax.set_ylabel("оценка эффекта (95% CI)")
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
st.pyplot(fig)

st.success(
    f"CUPED сузил доверительный интервал примерно в {np.sqrt(se0**2/se1**2):.2f}× при той же выборке. "
    f"Эквивалентно экономии ~{var_reduction:.0%} трафика. Чем выше корреляция ρ — тем сильнее выигрыш.",
    icon="✅")
st.caption("Важно: ковариата должна быть измерена ДО эксперимента, иначе можно внести смещение.")
