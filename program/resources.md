# Ресурсы

Подборка проверенных материалов. Не нужно читать всё — берите по одному основному источнику на блок
и остальное как справочник.

---

## Книги (ядро)

- **Kohavi, Tang, Xu — «Trustworthy Online Controlled Experiments»** — главная книга по A/B в индустрии.
  Читать параллельно с Блоками 2–4. Авторы — из Microsoft/Airbnb/LinkedIn.
- **Georgi Georgiev — «Statistical Methods in Online A/B Testing»** — практическая статистика тестов.
- **Ron Kohavi et al. — статьи из «KDD»/«Practical Guide to Controlled Experiments»** — бесплатные PDF.

## Статистика (фундамент, Блок 1)

- **«Practical Statistics for Data Scientists»** (Bruce & Bruce) — прикладная статистика с кодом.
- **«Introduction to Probability»** (Blitzstein & Hwang) + курс Harvard Stat110 (YouTube) — вероятность с нуля.
- **StatQuest (Josh Starmer, YouTube)** — интуитивные объяснения p-value, мощности, распределений.
- **Seeing Theory (seeing-theory.brown.edu)** — интерактивная визуализация вероятности и вывода.

## Причинность (Блоки 2 и 4.7)

- **«Causal Inference for The Brave and True»** (Matheus Facure) — бесплатная онлайн-книга с Python.
- **«The Effect»** (Nick Huntington-Klein) — бесплатно, доступно про DiD/RDD/IV.
- **«Mostly Harmless Econometrics»** — классика (посложнее).

## A/B тестирование (Блоки 2–3)

- **Курс Udacity «A/B Testing» (by Google)** — бесплатный, хорош для дизайна экспериментов.
- Блоги инженерных команд: **Netflix TechBlog, Microsoft ExP, Booking.com, Airbnb, Spotify, DoorDash** —
  раздел experimentation.
- **Evan Miller — «How Not To Run An A/B Test»** и его онлайн-калькуляторы.

## Продвинутое (Блок 4)

- **CUPED:** оригинальная статья Deng, Xu, Kohavi, Walker (2013) «Improving the Sensitivity of Online Controlled Experiments».
- **Sequential:** статьи Optimizely про always-valid inference; работы Johari, Pekelis, Walsh про mSPRT.
- **Байес A/B:** статьи VWO/Dynamic Yield; Chris Stucchio «Bayesian A/B Testing».
- **Бандиты:** «Bandit Algorithms» (Lattimore & Szepesvári, бесплатный PDF); блоги про Thompson Sampling.
- **Switchback / интерференция:** статьи DoorDash и Lyft про маркетплейс-эксперименты.
- **Uplift/HTE:** библиотеки `EconML` (Microsoft), `CausalML` (Uber) + их документация с примерами.

## Python / инструменты (Блок 0)

- `numpy`, `pandas`, `scipy.stats`, `statsmodels` — основной стек.
- `statsmodels.stats.power` / `.proportion` — размеры выборок и тесты долей.
- `pingouin` — удобная обёртка для стат-тестов.
- `EconML`, `CausalML` — продвинутая причинность и uplift.
- Онлайн-калькуляторы: Evan Miller, ABTestGuide (для быстрой проверки расчётов).

---

## Как выбрать одну траекторию (минимум)
1. Блок 1 → StatQuest + «Practical Statistics for Data Scientists».
2. Блоки 2–3 → Udacity A/B Testing + книга Kohavi.
3. Блок 4 → статья CUPED + «Bayesian A/B Testing» + блоги Netflix/DoorDash.
