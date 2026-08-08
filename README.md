# 🔮 Nostradamus

### A deterministic sports matchup prediction engine

**Nostradamus** is a sports prediction project designed to predict **which teams or players will face each other during a competition**.

Unlike traditional sports prediction models, Nostradamus does **not primarily aim to predict match winners**. Its purpose is to anticipate the structure of upcoming matchups based on official competition rules, available data, and deterministic prediction mechanisms.

The project is named after &#x2A;*Michel de Nostredame (Nostradamus)**, the French physician and apothecary best known for his prophecies. This time, however, Nostradamus's predictions are based on data, mathematical reasoning, official rules, and reproducible methods.

---

## 🎯 Objective

The main objective of Nostradamus is to predict the **potential matchups within sports competitions involving a draw or a draw-like mechanism**.

The project currently focuses on two sports:

- ⚽ **Men's football**
- 🎾 **Women's tennis**

The goal is not simply to generate independent predictions. Nostradamus must produce **globally coherent predictions** that respect the rules and structural constraints of the competition.

---

## 🌍 Project Scope

Nostradamus focuses on competitions where predicting future matchups can provide an interesting forecasting challenge.

### ⚽ Football

The football component initially focuses on major international competitions involving a draw.

The current scope includes:

- UEFA Champions League
- Africa Cup of Nations (CAN)
- UEFA European Championship (EURO)
- FIFA World Cup

The first competition targeted by Nostradamus is the **UEFA Champions League**.

For the Champions League league phase, Nostradamus aims to predict the eight opponents that each of the 36 participating teams will face, including the home/away configuration.

Following the league phase, the project may also predict potential paths through the knockout stages based on the final standings and subsequent draws.

### 🎾 Women's Tennis

The tennis component focuses on major **WTA tournaments** involving a draw.

The initial scope includes:

- WTA 500 tournaments
- WTA 1000 tournaments
- Grand Slam tournaments

For each tournament, Nostradamus aims to predict the initial matchups and potential paths through the tournament.

The tennis component may take into account information such as:

- ranking changes
- player withdrawals
- wildcards
- other relevant changes occurring before the draw

---

## ⚙️ How Nostradamus Works

Nostradamus is designed to operate similarly to a person carrying out a competition draw while respecting all applicable rules.

### Football

For the Champions League league phase, Nostradamus aims to:

1. Identify the participating teams.
2. Determine the relevant competition information and constraints.
3. Generate a prediction for the eight opponents of every team.
4. Determine the home/away configuration.
5. Ensure that the complete prediction is globally coherent.
6. After the league phase, use the final standings and subsequent draw information to generate potential knockout-stage paths.

### Women's Tennis

For each selected tournament, Nostradamus aims to:

1. Identify the expected participants.
2. Take relevant ranking information into account.
3. Take withdrawals, wildcards and other relevant changes into account.
4. Generate a prediction of the initial matchups.
5. Generate potential tournament paths for the participating players.

---

## 🧠 Core Principles

### Deterministic Predictions

Nostradamus is designed to be **deterministic**.

Given the same dataset, parameters and rules, Nostradamus should produce the **same prediction**.

A new prediction should only be generated when relevant information changes the data or parameters available to the system.

This principle is conceptually similar to using a fixed `random_state` in a machine learning experiment: identical inputs should lead to identical outputs.

The objective is therefore not to generate a different prediction every time the program is executed, but to produce **one reproducible prediction** for a given state of information.

### Draw Consistency

Nostradamus follows a **draw consistency principle**.

A predicted matchup cannot be considered independently from the prediction made for the opponent.

For example, if Nostradamus predicts:

> Paris Saint-Germain → Liverpool, Matchday 4, Home

then the corresponding prediction must automatically be:

> Liverpool → Paris Saint-Germain, Matchday 4, Away

The complete prediction must therefore remain **globally coherent**.

This principle is fundamental to Nostradamus: the system does not generate a collection of independent predictions, but a **single coherent prediction of the competition structure**.

### Official Competition Rules

Nostradamus is based on the official rules governing each competition.

Competition-specific constraints are treated as fundamental requirements of the prediction process.

The use of machine learning will only be considered when it provides a genuine value to the prediction problem. Nostradamus is not intended to use machine learning simply for the sake of using machine learning.

### Explainability

Nostradamus aims to produce results that are **understandable and accessible**, rather than opaque predictions.

The final predictions should therefore be presented in a clear and readable way.

---

## 🔮 Future Vision

In the long term, Nostradamus aims to become a **sports prediction engine** capable of continuously monitoring relevant competition information.

Ideally, Nostradamus would generate one prediction for a given competition state and maintain that prediction until a relevant event occurs.

Examples of such events include:

- player withdrawals
- ranking changes
- wildcards
- changes affecting the competition structure

When relevant information changes, Nostradamus could generate a new prediction based on the updated state.

A future version could also notify users when a significant event causes a prediction to be recalculated.

---

## 🚧 Project Status

Nostradamus is currently in the **early development and project design phase**.

The first implementation focuses on the football component and, more specifically, on the UEFA Champions League.

Current priorities include:

- defining the required datasets
- identifying reliable data sources
- documenting official competition rules
- translating competition rules into computational constraints
- designing the deterministic prediction mechanism
- developing the first football prototype

No final prediction engine has been implemented yet.

---

## 🗺️ Roadmap

### Phase 0 — Project Definition

- [x] Define the project concept
- [x] Define the project scope
- [x] Define the core principles
- [x] Define the deterministic prediction philosophy
- [x] Define the draw consistency principle

### Phase 1 — Football Data & Rules

- [ ] Define the required data
- [ ] Identify data sources
- [ ] Collect historical competition data
- [ ] Document UEFA competition rules
- [ ] Translate rules into computational constraints

### Phase 2 — Football Prediction Engine

- [ ] Design the prediction mechanism
- [ ] Implement the deterministic draw mechanism
- [ ] Implement draw consistency
- [ ] Handle home/away constraints
- [ ] Validate predictions against historical draws

### Phase 3 — Champions League Prediction

- [ ] Generate a prediction before the official draw
- [ ] Compare Nostradamus's prediction with the official draw
- [ ] Analyse prediction accuracy and limitations

### Phase 4 — Knockout Stages

- [ ] Model the knockout-stage draw
- [ ] Predict potential paths
- [ ] Integrate final league-phase standings
- [ ] Extend the prediction to the final

### Phase 5 — Women's Tennis

- [ ] Define the tennis data requirements
- [ ] Identify WTA data sources
- [ ] Model tournament-specific draw constraints
- [ ] Develop the first tennis prediction engine
- [ ] Test the approach on historical tournaments

### Future

- [ ] Develop a user interface
- [ ] Implement event-based prediction updates
- [ ] Add prediction notifications
- [ ] Explore additional sports and competitions

---

## 🛠️ Technologies

The technical stack of Nostradamus is intentionally not fixed at the beginning of the project.

Technology choices will be made according to the requirements identified during development.

Potential technologies may include:

- Python
- Data processing and analysis libraries
- Mathematical and probabilistic methods
- Machine learning, where relevant
- Docker for reproducible deployment
- A web interface for future versions

---

## 👩🏾‍💻 Author

**Lorame Bakaboula**

Nostradamus is a personal project designed, developed and documented by Lorame Bakaboula.

The project is intended to document not only the final result, but also the **process of research, experimentation, data collection and development** behind the prediction engine.

---

## 📄 License

See the [`LICENSE`](LICENSE) file for information about the project's license.
