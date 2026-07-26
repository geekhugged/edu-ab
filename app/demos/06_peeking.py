"""Демо: проблема подглядывания (peeking) — как ранняя остановка раздувает ошибку I рода."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import streamlit as st

st.title("👀 Проблема peeking (подглядывания)")
st.caption("Блок 3 · Модуль 3.1 — почему нельзя останавливать тест, «как только стало значимо».")

st.markdown(
    """
Возьмём **A/A-тест** (реального эффекта нет) и будем проверять значимость много раз по мере
накопления данных, останавливаясь при первом p < α. Сравним настоящую долю ложных срабатываний
с честным подходом «посмотреть один раз в конце».
    """
)

c = st.columns(4)
n_max = c[0].slider("Итоговый размер группы", 200, 5000, 2000, step=100)
looks = c[1].slider("Сколько раз подглядываем", 1, 50, 20)
alpha = c[2].select_slider("α", [0.01, 0.05, 0.10], 0.05)
trials = c[3].slider("Число экспериментов", 500, 10000, 3000, step=500)

rng = np.random.default_rng(2025)
checkpoints = np.linspace(n_max // looks, n_max, looks).astype(int)

peek_false_pos = 0
# Векторизованная симуляция: считаем t-статистику на каждом чекпоинте через
# кумулятивные суммы, без питоновского двойного цикла (иначе тысячи вызовов ttest).
a = rng.normal(0, 1, (trials, n_max))
b = rng.normal(0, 1, (trials, n_max))
csa, csb = np.cumsum(a, axis=1), np.cumsum(b, axis=1)
cqa, cqb = np.cumsum(a**2, axis=1), np.cumsum(b**2, axis=1)

pvals_at = np.empty((trials, len(checkpoints)))
for j, cp in enumerate(checkpoints):
    ma, mb = csa[:, cp - 1] / cp, csb[:, cp - 1] / cp
    va = (cqa[:, cp - 1] - cp * ma**2) / (cp - 1)
    vb = (cqb[:, cp - 1] - cp * mb**2) / (cp - 1)
    se = np.sqrt(va / cp + vb / cp)
    tstat = (ma - mb) / se
    pvals_at[:, j] = 2 * (1 - stats.norm.cdf(np.abs(tstat)))  # норм. аппроксимация

peek_rate = (pvals_at < alpha).any(axis=1).mean()   # хоть раз пересекли порог
fixed_rate = (pvals_at[:, -1] < alpha).mean()        # только финальный взгляд
example_paths = pvals_at[:40]

c1, c2 = st.columns(2)
c1.metric("Ложные срабатывания при peeking", f"{peek_rate:.1%}",
          delta=f"+{(peek_rate-alpha)*100:.1f} п.п. сверх α", delta_color="inverse")
c2.metric("Честный тест (1 взгляд)", f"{fixed_rate:.1%}",
          delta=f"≈ α = {alpha:.0%}", delta_color="off")

fig, ax = plt.subplots(figsize=(10, 4))
for path in example_paths:
    ax.plot(checkpoints, path, color="#94a3b8", lw=.6, alpha=.6)  # noqa
ax.axhline(alpha, color="#ef4444", ls="--", label=f"порог α={alpha}")
ax.set_xlabel("накоплено наблюдений")
ax.set_ylabel("p-value")
ax.set_ylim(0, 1)
ax.set_title("Траектории p-value в A/A-тестах (эффекта нет)")
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
st.pyplot(fig)

st.error(
    f"При {looks} подглядываниях ложных «побед» уже ~{peek_rate:.0%} вместо обещанных {alpha:.0%}. "
    "p-value гуляет и рано или поздно пересекает порог случайно.", icon="🚨")

with st.expander("✅ Как правильно"):
    st.markdown(
        "- Зафиксируйте размер выборки и дату остановки **заранее** и смотрите один раз.\n"
        "- Либо используйте **sequential-методы** (alpha-spending, mSPRT, confidence sequences), "
        "которые честно контролируют α при непрерывном мониторинге — Модуль 4.2.\n"
        "- Никаких «дашбордов с live-значимостью» без поправок."
    )
