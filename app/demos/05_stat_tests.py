"""Демо: статистические критерии — z-тест долей и t-тест Уэлча + CI для эффекта."""
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
import streamlit as st

st.title("⚖️ Статистические критерии")
st.caption("Блок 2 · Модули 2.5–2.6 — выбираем критерий под тип метрики и строим CI для эффекта.")

tab1, tab2 = st.tabs(["📊 Конверсия — z-тест долей", "💰 Среднее — t-тест Уэлча"])

with tab1:
    st.markdown("Сравнение двух долей (конверсий). Введите наблюдения по группам.")
    c = st.columns(4)
    nA = c[0].number_input("Показы A", value=10000, min_value=1)
    xA = c[1].number_input("Конверсии A", value=500, min_value=0)
    nB = c[2].number_input("Показы B", value=10000, min_value=1)
    xB = c[3].number_input("Конверсии B", value=560, min_value=0)

    pA, pB = xA / nA, xB / nB
    stat, pval = proportions_ztest([xB, xA], [nB, nA])
    ci_low, ci_high = confint_proportions_2indep(xB, nB, xA, nA, method="wald")

    m1, m2, m3 = st.columns(3)
    m1.metric("Конверсия A", f"{pA:.2%}")
    m2.metric("Конверсия B", f"{pB:.2%}", delta=f"{(pB-pA):+.2%} абс.")
    m3.metric("Отн. прирост", f"{(pB/pA-1):+.1%}" if pA > 0 else "—")

    st.write(f"**z = {stat:.3f}, p-value = {pval:.4f}**")
    st.write(f"**95% CI для разницы (B − A): [{ci_low:+.3%}, {ci_high:+.3%}]**")
    if ci_low > 0 or ci_high < 0:
        st.success("CI не содержит 0 → разница статистически значима на уровне 5%.", icon="✅")
    else:
        st.warning("CI содержит 0 → значимой разницы не обнаружено (это НЕ доказательство, что эффекта нет).", icon="⚠️")
    st.caption("Совет: смотрите на CI эффекта, а не только на p-value — он показывает и величину, и неопределённость.")

with tab2:
    st.markdown("Сравнение средних (выручка, время). По умолчанию — **тест Уэлча** (не требует равных дисперсий).")
    c = st.columns(3)
    n = c[0].slider("Размер группы", 100, 20000, 3000, key="t_n")
    mean_a = c[1].number_input("Среднее A", value=100.0)
    uplift = c[2].slider("Истинный эффект B, %", -10.0, 10.0, 3.0, 0.5)

    rng = np.random.default_rng(2024)
    # логнормальная «выручка» с заданным средним
    def lognorm_with_mean(mean, n, sigma=0.9):
        mu = np.log(mean) - sigma**2 / 2
        return rng.lognormal(mu, sigma, n)

    a = lognorm_with_mean(mean_a, n)
    b = lognorm_with_mean(mean_a * (1 + uplift / 100), n)
    t, p = stats.ttest_ind(b, a, equal_var=False)
    diff = b.mean() - a.mean()
    se = np.sqrt(a.var(ddof=1)/n + b.var(ddof=1)/n)
    ci = (diff - 1.96 * se, diff + 1.96 * se)

    m1, m2, m3 = st.columns(3)
    m1.metric("Среднее A (набл.)", f"{a.mean():.2f}")
    m2.metric("Среднее B (набл.)", f"{b.mean():.2f}", delta=f"{diff:+.2f}")
    m3.metric("p-value", f"{p:.4f}")
    st.write(f"**95% CI для разницы средних: [{ci[0]:+.2f}, {ci[1]:+.2f}]**")
    st.caption("Обратите внимание: при малом истинном эффекте тест часто «не видит» его — это вопрос мощности, "
               "а не отсутствия эффекта. Увеличьте n и посмотрите, как сужается CI.")
    st.info("Правило выбора: конверсия → z-тест/χ²; среднее → t-тест Уэлча; дикое распределение и малое n → "
            "Mann–Whitney или bootstrap.", icon="🧭")
