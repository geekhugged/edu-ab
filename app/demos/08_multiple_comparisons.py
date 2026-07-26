"""Демо: множественные сравнения — Bonferroni и Benjamini-Hochberg (FDR)."""
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.multitest import multipletests
import streamlit as st

st.title("🎛️ Множественные сравнения")
st.caption("Блок 3 · Модуль 3.2 — почему проверка кучи метрик/сегментов ловит ложные «победы».")

st.markdown(
    """
Тестируете 20 метрик при α=5%? Даже если *ни одна* не работает, в среднем одна покажет «значимость» случайно.
Симуляция: часть гипотез реально ложные (эффекта нет), часть — истинные. Смотрим, что делают поправки.
    """
)

c = st.columns(4)
m_null = c[0].slider("Гипотез БЕЗ эффекта", 0, 200, 100)
m_true = c[1].slider("Гипотез С эффектом", 0, 50, 10)
effect = c[2].slider("Сила истинного эффекта (σ)", 0.5, 5.0, 3.0, 0.1)
alpha = c[3].select_slider("α", [0.01, 0.05, 0.10], 0.05)

from scipy import stats

rng = np.random.default_rng(77)
# p-value для нулевых — равномерны; для истинных — сдвинуты к нулю
z_true = rng.normal(effect, 1, m_true)
p_true = 2 * (1 - stats.norm.cdf(np.abs(z_true)))
p_null = rng.uniform(0, 1, m_null)
pvals = np.concatenate([p_null, p_true])
is_true = np.array([False] * m_null + [True] * m_true)

def summarize(reject):
    tp = int((reject & is_true).sum())
    fp = int((reject & ~is_true).sum())
    fn = int((~reject & is_true).sum())
    return tp, fp, fn

raw = pvals < alpha
bonf = multipletests(pvals, alpha=alpha, method="bonferroni")[0]
bh = multipletests(pvals, alpha=alpha, method="fdr_bh")[0]

rows = []
for name, rej in [("Без поправки", raw), ("Bonferroni (FWER)", bonf), ("Benjamini–Hochberg (FDR)", bh)]:
    tp, fp, fn = summarize(rej)
    fdr = fp / max(tp + fp, 1)
    rows.append({"Метод": name, "Найдено истинных (TP)": tp,
                 "Ложных срабатываний (FP)": fp, "Пропущено (FN)": fn,
                 "Доля ложных среди находок": f"{fdr:.0%}"})
st.dataframe(rows, width="stretch", hide_index=True)

fig, ax = plt.subplots(figsize=(10, 3.6))
order = np.argsort(pvals)
colors = ["#22c55e" if is_true[i] else "#ef4444" for i in order]
ax.bar(range(len(pvals)), np.sort(pvals), color=colors, width=1.0)
ax.axhline(alpha, color="#334155", ls="--", label=f"наивный порог α={alpha}")
bh_thr = alpha * (np.arange(1, len(pvals) + 1)) / len(pvals)
ax.plot(range(len(pvals)), bh_thr, color="#6366f1", lw=2, label="линия BH")
ax.set_ylim(0, min(1, alpha * 6))
ax.set_xlabel("гипотезы, отсортированные по p-value")
ax.set_ylabel("p-value")
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
st.pyplot(fig)
st.caption("Зелёные — реально есть эффект, красные — нет. BH держит долю ложных находок под контролем, "
           "оставаясь мощнее строгого Bonferroni.")

st.info("Главная защита — заранее объявленная **primary-метрика**. Остальное (сегменты, вторичные метрики) — "
        "с поправками и как генерация гипотез, а не финальные выводы.", icon="🛡️")
