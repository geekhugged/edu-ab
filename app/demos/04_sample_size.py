"""Демо: калькулятор размера выборки, MDE, мощности и длительности теста."""
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
import streamlit as st

st.title("🧮 Калькулятор размера выборки и MDE")
st.caption("Блок 2 · Модуль 2.4 — считаем сколько данных нужно ДО запуска.")

st.markdown(
    "Планирование эксперимента — это баланс: базовая конверсия, минимальный улавливаемый эффект (**MDE**), "
    "уровень **α** и желаемая **мощность**. Уменьшаете MDE вдвое — выборка растёт вчетверо."
)

metric = st.radio("Тип метрики", ["Конверсия (доля)", "Среднее (напр. выручка)"], horizontal=True)
c = st.columns(4)

if metric.startswith("Конверсия"):
    base = c[0].slider("Базовая конверсия, %", 1.0, 50.0, 5.0, 0.5) / 100
    lift = c[1].slider("MDE — относит. прирост, %", 1.0, 50.0, 10.0, 1.0) / 100
    alpha = c[2].select_slider("α", [0.01, 0.05, 0.10], 0.05)
    power = c[3].slider("Мощность", 0.5, 0.99, 0.80, 0.01)
    target = base * (1 + lift)
    es = proportion_effectsize(target, base)
else:
    base = c[0].number_input("Среднее в контроле", value=100.0)
    sd = c[1].number_input("Стд. отклонение σ", value=80.0, min_value=0.1)
    abs_mde = c[2].number_input("MDE (абсолютный)", value=5.0, min_value=0.1)
    alpha = c[3].select_slider("α ", [0.01, 0.05, 0.10], 0.05)
    power = st.slider("Мощность", 0.5, 0.99, 0.80, 0.01)
    es = abs_mde / sd

n = NormalIndPower().solve_power(effect_size=abs(es), alpha=alpha, power=power, alternative="two-sided")
n = int(np.ceil(n))

c1, c2, c3 = st.columns(3)
c1.metric("Нужно на группу", f"{n:,}".replace(",", " "))
c2.metric("Всего (2 группы)", f"{2*n:,}".replace(",", " "))
daily = st.number_input("Трафик в день (на обе группы)", value=2000, min_value=1)
days = int(np.ceil(2 * n / daily))
c3.metric("Длительность", f"{days} дн.", help="Но не короче 1–2 полных недель из-за day-of-week эффекта!")

if days < 7:
    st.warning("Тест короче недели — обязательно докрутите до целого числа недель, иначе day-of-week исказит результат.", icon="⚠️")

st.divider()
st.subheader("Как размер выборки зависит от MDE")
mdes = np.linspace(max(abs(es) * 0.4, 1e-3), abs(es) * 2.5, 60)
ns = [NormalIndPower().solve_power(effect_size=e, alpha=alpha, power=power, alternative="two-sided") for e in mdes]
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(mdes, ns, color="#6366f1", lw=2)
ax.axvline(abs(es), color="#ef4444", ls="--", label="ваш MDE")
ax.scatter([abs(es)], [n], color="#ef4444", zorder=5)
ax.set_xlabel("effect size (MDE в единицах σ)")
ax.set_ylabel("n на группу")
ax.set_title("Квадратичный рост: меньше эффект → сильно больше выборка")
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
st.pyplot(fig)

st.info("Правило: `n ∝ σ² / MDE²`. Отсюда два способа ускорить тест — увеличить MDE (ловить только крупные эффекты) "
        "или снизить дисперсию σ² (например, CUPED — см. соответствующее демо).", icon="💡")
