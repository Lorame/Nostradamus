# UCL Qualification Scenario Generation Design

## Overview

## Overview

Before implementing the UEFA Champions League draw simulation, Nostradamus must first determine the possible compositions of the 36-team league phase.

At the current stage of the competition, some teams are already guaranteed to participate in the league phase, while others still depend on the outcome of qualifying playoffs.

**(Project status as of August 23, 2026: the UEFA Champions League qualifying playoffs have not yet been completed. The final list of league phase participants is therefore not available. Nostradamus must take into account this real-world constraint and cannot rely on a definitive participant list at this stage.)**

The objective is not to predict the outcome of each playoff randomly, but to generate all mathematically possible qualification scenarios and later identify the scenario corresponding to the real competition state.

---

## Core Principle

Nostradamus separates the problem into two independent steps:

1. Determine the possible league phase participants.
2. Apply UEFA draw rules to generate a valid draw.

The draw engine should never operate directly on uncertain teams.

The input of the draw engine must always be a complete list of 36 confirmed clubs.

---

## Data Model

### Club Identification

All internal calculations use UEFA `club_id` values.

Club names are only used for display purposes.

Using identifiers avoids ambiguity caused by:

- different club naming conventions
- translations
- abbreviations
- historical names

Example:

```text
50037 → Bayern München
50051 → Real Madrid
52747 → Paris Saint-Germain
```

---

## Fixed Teams

Some clubs are already guaranteed to participate in the league phase.

These teams are extracted from the master dataset:

```text
qualification_status = league_phase
```

They represent the immutable part of every possible scenario.

Current logic:

```text
Fixed teams + playoff winners = complete league phase
```

The fixed teams should not be duplicated in another source file.

The master dataset remains the single source of truth.

---

## Playoff Teams

The remaining teams are still dependent on qualifying playoff results.

Each playoff confrontation has two possible outcomes:

```text
Match 1:
Team A OR Team B

Match 2:
Team C OR Team D

...

Match 7:
Team M OR Team N
```

Only the winner of each confrontation will participate in the league phase.

The losing teams are excluded from the corresponding scenario.

---

## Qualification Scenario Generation

There are seven playoff confrontations.

Each confrontation has two possible winners.

Therefore, the number of possible qualification scenarios is:

```text
2^7 = 128
```

Each generated scenario must contain:

```text
29 fixed teams
+
7 playoff winners
=
36 league phase teams
```

---

## Scenario Storage

Qualification scenarios should not be stored as separate files.

A single structured file should contain all possibilities.

Recommended format:

```text
data/processed/ucl_2026_2027_playoff_scenarios.json
```

Each scenario contains:

- scenario identifier
- list of qualified `club_id`

Example structure:

```json
[
  {
    "scenario_id": 1,
    "qualified_clubs": [
      50037,
      50051,
      52747
    ]
  }
]
```

---

## Scenario Validation Rules

The scenario generator must validate its output before being used by the draw engine.

Required checks:

### Number of scenarios

The generator must create exactly:

```text
128 scenarios
```

---

### Scenario uniqueness

All scenarios must be different.

The system must verify that:

```text
number of generated scenarios = number of unique scenarios
```

Expected result:

```text
128 generated scenarios
128 unique scenarios
```

Any duplicate indicates an implementation error.

---

### Team count

Every scenario must contain exactly:

```text
36 clubs
```

---

### Fixed team consistency

Every scenario must contain all guaranteed league phase teams.

---

### Playoff consistency

Each playoff match must contribute exactly one winner.

The system must ensure:

- no playoff loser appears in a scenario
- no club appears twice
- every scenario contains exactly seven playoff winners

---

## Future Workflow

The expected workflow is:

```text
Master dataset
        |
        |
Extract fixed teams
        |
        |
Add playoff matches
        |
        |
Generate 128 qualification scenarios
        |
        |
Validate scenarios
        |
        |
Select real competition scenario after playoffs
        |
        |
Calculate UEFA pots
        |
        |
Run draw simulation
```

---

## Pot Calculation

Pot calculation should not happen before qualification scenarios are resolved.

The reason is that UEFA coefficients determine pot allocation.

A playoff winner can change the ranking distribution and therefore modify pot composition.

The correct sequence is:

```text
Complete list of 36 clubs
        |
        |
Merge UEFA coefficients
        |
        |
Sort by coefficient
        |
        |
Generate Pots 1 to 4
```

The pot calculation function should therefore receive only:

```text
list of 36 club_id
```

and return:

```text
Pot 1
Pot 2
Pot 3
Pot 4
```

---

## Design Philosophy

This architecture ensures that Nostradamus remains:

- deterministic
- reproducible
- explainable
- independent from uncertain competition states

The system does not guess one qualification outcome.

It explores every mathematically possible state and applies the official UEFA rules only once the competition state is known. facile
