# Nostradamus Football — Data Requirements

**Project:** Nostradamus  
**Scope:** Football  
**Competition:** UEFA Champions League  
**Target edition:** 2026–2027  
**Document status:** Initial data requirements  
**Date:** August 2026

---

## 1. Purpose of this document

This document defines the data that Nostradamus needs in order to produce its first football predictions.

At this stage, the objective is **only to define the required data**. Data sources, collection methods, scraping, APIs, data processing and technical implementation will be documented separately.

The purpose of this phase is to answer a simple question:

> **What does Nostradamus need to know in order to make a coherent prediction of the UEFA Champions League draw and subsequently estimate the final league-phase ranking?**

The initial scope focuses on the **2026–2027 UEFA Champions League**.

---

# 2. Data required for draw prediction

The first objective of Nostradamus is to predict the opponents that each team will face during the league phase of the UEFA Champions League, as well as the order and home/away configuration of those encounters.

To reproduce this process, Nostradamus needs information about previous draws as well as the teams participating in the upcoming edition.

---

## 2.1. Historical draws under the new league format

Nostradamus needs data describing the draws from the **two most recent UEFA Champions League editions using the current league-phase format**.

> « Données sur les tirages de rencontres des deux dernières éditions de la Ligue des Champions lors du premier tour (celles avec le nouveau système de ligue à la place de la phase de poules). »

These editions are particularly relevant because they use the same general competition format that Nostradamus will attempt to reproduce.

The historical draw data should make it possible to identify, for every participating team:

- its opponents;
- the order in which each opponent was encountered;
- whether the match was played at home or away.

These historical draws will allow Nostradamus to study the structure of previous draws and later verify whether its own predictions respect the same structural constraints.

The exact date or day on which a match was played is **not part of Nostradamus' prediction scope**.

---

## 2.2. Teams participating in the 2026–2027 competition

Nostradamus needs to know which teams are expected to participate in the 2026–2027 UEFA Champions League.

For each team, information relevant to the draw will need to be collected, including:

- team identity;
- country;
- national association;
- competition status;
- information used to determine the team's position in the draw.

The exact information required will depend on the official UEFA rules governing the 2026–2027 competition.

This information is necessary because Nostradamus cannot reproduce a draw without first knowing **who is participating in it**.

---

## 2.3. Information used to determine the draw groups

Nostradamus needs the information required to determine how participating teams are distributed before the draw.

This includes, where applicable:

- UEFA coefficient or other ranking information used by the competition;
- draw pots;
- team position within the relevant pot;
- any other information used by UEFA to organise the draw.

This information is necessary because the possible opponents of a team depend on its position in the draw structure.

---

## 2.4. Team association and country information

Nostradamus needs to know the national association to which each participating team belongs.

This information is particularly important because the draw may contain restrictions concerning teams belonging to the same association.

For example, if two teams from the same national association cannot meet during a particular stage of the competition, Nostradamus must have the information necessary to identify this situation before generating a prediction.

---

## 2.5. Home and away information

Nostradamus must be able to determine which encounters are played at home and which are played away.

This information is required because the home/away configuration forms part of the prediction and because the competition rules may impose constraints on the distribution of home and away encounters.

The prediction should therefore not simply state:

> Paris Saint-Germain vs Liverpool

but should be able to specify:

> Paris Saint-Germain — Liverpool  
> Encounter 4 — Home

The corresponding prediction for Liverpool must remain coherent:

> Liverpool — Paris Saint-Germain  
> Encounter 4 — Away

This reflects the **Draw Consistency Principle** defined in the Nostradamus project vision.

---

# 3. Historical data for league-phase ranking prediction

The second objective of Nostradamus is to estimate the ranking of teams at the end of the league phase.

Unlike the draw itself, this prediction requires information about the sporting performance of the participating teams.

---

## 3.1. Match results from previous Champions League editions

Nostradamus should collect match results from the **six most recent Champions League editions** for the teams participating in the upcoming competition.

> « Données sur les résultats de match au premier tour de Ligue des champions pour l'ensemble des équipes participantes à la prochaine édition.(sur les six dernières éditions car même si le format n'est plus le même, les équipes qui participent restent très majoritairement identiques). »

The reason for using several editions is that the clubs participating in the Champions League are relatively stable over time, even though the competition format has changed.

These historical results can provide information about the recent performance of the teams and can later contribute to estimating their potential performance during the upcoming league phase.

The collected information should include, where available:

- opponents;
- match result;
- goals scored;
- goals conceded;
- home or away status;
- competition edition.

The historical results will not be used to reproduce the draw itself. Their primary purpose is to provide historical sporting information for the **league-phase ranking prediction**.

---

## 3.2. Final league-phase rankings

Nostradamus needs the final rankings from the **two most recent editions using the current league-phase format**.

> « Données sur les classements à l'issue de la neuvième journée de phase de ligue des deux dernières éditions. »

These rankings are particularly relevant because they correspond to the current competition format.

The collected information should include, where available:

- final position;
- points;
- matches played;
- wins;
- draws;
- losses;
- goals scored;
- goals conceded;
- goal difference;
- other official ranking criteria used to separate teams.

These data will help Nostradamus understand the relationship between match results and the final league-phase ranking under the current format.

---

# 4. Team information

Nostradamus may also require information describing the composition and evolution of the participating teams.

These data are primarily intended to support the future prediction of sporting performance rather than the draw itself.

---

## 4.1. Squad information

For each participating team, Nostradamus may collect information about its squad.

The initial scope includes:

- number of international players;
- player market valuation, where available;
- player experience;
- length of time players have been at the club.

> « Données sur les équipes (nombre de joueurs internationaux, si possible leur valorisation et leur ancienneté dans le club ) »

These data are intended to provide information about the strength and stability of a team at the beginning of the competition.

They are not considered mandatory information for reproducing the Champions League draw.

---

## 4.2. Changes affecting teams

Nostradamus may also collect information concerning significant changes affecting participating teams between the previous season and the beginning of the new Champions League season.

The initial period considered is:

> **September of the previous year → 15 August**

Potentially relevant changes include:

- changes of head coach;
- significant player arrivals;
- significant player departures;
- major changes affecting the squad.

The objective is to determine whether the evolution of a team before the competition should be considered when estimating its potential performance.

This information is therefore primarily related to the **prediction of the final league-phase ranking**, rather than to the draw itself.

---

# 5. Distinction between draw data and performance data

The data identified so far serve two different purposes.

### Draw prediction

The draw prediction primarily requires information concerning:

- participating teams;
- draw structure;
- pots;
- associations;
- UEFA rankings or coefficients where relevant;
- home/away constraints;
- order of encounters;
- historical draws.

### League-phase ranking prediction

The ranking prediction may additionally require:

- historical match results;
- previous league-phase rankings;
- squad information;
- team evolution;
- other information related to sporting performance.

This distinction is important because **predicting the draw and predicting the final ranking are two separate problems** within Nostradamus.

---

# 6. Data currently considered essential

Based on the initial project design, the following data are currently considered essential for the first football implementation:

### Draw-related data

- Historical draws from the two most recent Champions League editions using the league-phase format.
- Participating teams for the 2026–2027 edition.
- Information required to determine the draw structure and pots.
- National associations of participating teams.
- Home/away information.
- Order of encounters.
- Official information describing the competition structure.

### Ranking-related data

- Match results from the six most recent Champions League editions for the participating teams.
- Final league-phase rankings from the two most recent editions using the current format.

### Team-related data

- Squad information.
- Number of international players.
- Player market valuation where available.
- Player experience and time at the club.
- Significant changes affecting teams before the competition.

This list is an **initial scope** and may be refined after the official UEFA rules and the precise requirements of the prediction mechanism have been analysed.

---

# 7. Data intentionally not defined at this stage

Some potentially useful information has deliberately not been included as a requirement yet.

In particular, Nostradamus will not automatically collect every available statistic about the teams or their players.

The project will only retain additional data when there is a clear reason to believe that the information can contribute to one of its prediction objectives.

For example, detailed performance statistics may become relevant later for estimating match results and the final ranking, but they are not required simply to reproduce the draw.

Likewise, the exact dates, days of the week and kick-off times of matches are outside the current prediction scope.

This approach aims to keep the first version of Nostradamus focused on its primary objective:

> **Predicting the structure and order of future encounters rather than predicting sporting outcomes without a specific purpose.**

---

# 8. Initial scope

The first implementation will focus on the **2026–2027 UEFA Champions League**.

The data requirements defined in this document are therefore designed primarily around this competition.

The requirements may later be adapted to other football competitions such as:

- UEFA European Championship;
- Africa Cup of Nations;
- FIFA World Cup.

Each competition will require its own analysis because its rules, draw mechanisms and available data may differ.

---

# 9. Next step

Once the data requirements have been validated, the next phase will focus on identifying **where and how each required piece of information can be obtained**.

This will be documented separately and will cover:

- potential data sources;
- official sources;
- APIs;
- downloadable datasets;
- scraping;
- data availability;
- historical coverage;
- data quality;
- limitations and missing information.

No data collection method is assumed at this stage.