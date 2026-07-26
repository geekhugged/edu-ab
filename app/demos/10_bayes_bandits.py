"""Демо: байесовский A/B (Beta-Binomial) и многорукий бандит (Thompson Sampling)."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import streamlit as st

st.title("🃏 Байесовский A/B и бандиты")
st.caption("Блок 4 · Модули 4.3–4.4 — вероятностные решения и адаптивный трафик.")

tab1, tab2 = st.tabs(["🎲 Байес: P(B > A)", "🎰 Бандит: Thompson Sampling"])

with tab1:
    st.markdown(
        "Beta-Binomial: априор `Beta(1,1)` (равномерный) обновляется данными в апостериор "
        "`Beta(1+конверсии, 1+неудачи)`. Из него считаем **P(B>A)** и **ожидаемые потери** — "
        "прямые вероятностные утверждения вместо p-value."
    )
    c = st.columns(4)
    nA = c[0].number_input("Показы A", value=1000, min_value=1)
    xA = c[1].number_input("Конверсии A", value=100, min_value=0)
    nB = c[2].number_input("Показы B", value=1000, min_value=1)
    xB = c[3].number_input("Конверсии B", value=120, min_value=0)

    rng = np.random.default_rng(5)
    postA = stats.beta(1 + xA, 1 + nA - xA)
    postB = stats.beta(1 + xB, 1 + nB - xB)
    sA = postA.rvs(200000, random_state=rng)
    sB = postB.rvs(200000, random_state=rng)
    p_b_better = (sB > sA).mean()
    expected_loss_choosing_b = np.maximum(sA - sB, 0).mean()

    xs = np.linspace(0, max(xA/nA, xB/nB) * 2, 500)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(xs, postA.pdf(xs), color="#94a3b8", lw=2, label="A апостериор")
    ax.fill_between(xs, postA.pdf(xs), color="#94a3b8", alpha=.25)
    ax.plot(xs, postB.pdf(xs), color="#6366f1", lw=2, label="B апостериор")
    ax.fill_between(xs, postB.pdf(xs), color="#6366f1", alpha=.25)
    ax.set_xlabel("истинная конверсия")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig)

    c1, c2 = st.columns(2)
    c1.metric("P(B > A)", f"{p_b_better:.1%}")
    c2.metric("Ожидаемые потери при выборе B", f"{expected_loss_choosing_b:.4%}",
              help="Насколько в среднем проиграем, если B на деле хуже. Порог решения, напр. < 0.1%.")
    if p_b_better > 0.95:
        st.success("P(B>A) > 95% и малые ожидаемые потери → можно раскатывать B.", icon="✅")
    else:
        st.info("Вероятность пока недостаточна для уверенного решения — нужно больше данных.", icon="ℹ️")

with tab2:
    st.markdown(
        "**Многорукий бандит** адаптивно льёт больше трафика на лучший вариант (Thompson Sampling: "
        "семплируем из апостериоров и выбираем максимум). Сравним суммарный **regret** с равномерным A/B."
    )
    c = st.columns(2)
    n_arms = c[0].slider("Число вариантов", 2, 6, 3)
    horizon = c[1].slider("Число показов", 500, 20000, 5000, step=500)

    rng = np.random.default_rng(2026)
    true_rates = np.linspace(0.10, 0.16, n_arms)
    rng.shuffle(true_rates)
    best = true_rates.max()

    # Thompson Sampling
    alpha_ = np.ones(n_arms)
    beta_ = np.ones(n_arms)
    ts_reward = 0
    ts_regret = []
    pulls = np.zeros(n_arms, dtype=int)
    for _ in range(horizon):
        theta = rng.beta(alpha_, beta_)
        arm = int(np.argmax(theta))
        r = rng.random() < true_rates[arm]
        alpha_[arm] += r
        beta_[arm] += 1 - r
        ts_reward += r
        pulls[arm] += 1
        ts_regret.append(best - true_rates[arm])

    # равномерный A/B
    ab_regret = [best - true_rates[i % n_arms] for i in range(horizon)]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(np.cumsum(ab_regret), color="#94a3b8", lw=2, label="равномерный A/B")
    ax.plot(np.cumsum(ts_regret), color="#6366f1", lw=2, label="Thompson Sampling")
    ax.set_xlabel("показы")
    ax.set_ylabel("накопленный regret")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig)

    st.write("**Истинные конверсии вариантов:**",
             ", ".join(f"{r:.1%}" for r in true_rates),
             f" · лучший = {best:.1%}")
    st.write("**Доля трафика, отданная каждому варианту бандитом:**",
             ", ".join(f"{p/horizon:.0%}" for p in pulls))
    st.success(
        f"Бандит потерял меньше: суммарный regret {np.sum(ts_regret):.1f} против {np.sum(ab_regret):.1f} у A/B. "
        "Но помните: бандит хуже для честной оценки эффекта и guardrail-контроля — он про оптимизацию, "
        "а не про обучение для будущих решений.", icon="✅")
