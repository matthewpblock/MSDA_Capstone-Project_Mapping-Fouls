# Metric Definitions: Strategic Geometry & EWE-v3.8

This document provides the mathematical definitions and logic for the proprietary metrics used in the **Expected-Whistle-Engine (EWE-v3.8)**. [cite_start]These metrics are designed to move beyond descriptive spatial analysis into prescriptive tactical optimization[cite: 315, 535].

---

## 1. Expected Whistle Probability ($P(W)$)

[cite_start]The baseline expectancy for a foul call at a specific coordinate on the hardwood[cite: 331, 348]. [cite_start]It is the primary output of the **EWE-v3.8 Dual-Branch Neural Network** and is composed of two sub-factors [cite: 501-505]:

* [cite_start]**Geography Effect:** The baseline probability derived from the **Spatial CNN Branch**, accounting for "rim gravity" and localized officiating tendencies at specific coordinates[cite: 502, 503].
* [cite_start]**Profile Boost:** The marginal probability adjustment derived from the **Tabular MLP Branch**, incorporating player height, weight, experience, and FT% to control for physical leverage and tactical "Hack-a-Shaq" bias[cite: 504, 505].

---

## 2. Signature Delta ($\delta$)

[cite_start]The **Signature Delta** isolates a player's idiosyncratic foul-drawing skill from the geographic and physical signal of their shot selection[cite: 314, 506]. [cite_start]It represents the "skill residual" that remains after the engine has established the expected baseline[cite: 330, 333].

**Formula:**
$$\delta = F_{actual} - E[F]$$

* [cite_start]**$F_{actual}$**: The observed frequency of fouls drawn by the player[cite: 314].
* **$E[F]$**: The expected foul frequency as predicted by the EWE-v3.8[cite: 314].

**Interpretation:**
* [cite_start]**Signature Specialists:** Players with high, persistent positive deltas who possess repeatable techniques for contact provocation[cite: 511, 512].
* [cite_start]**System Beneficiaries:** Players with deltas near zero whose foul volume is almost entirely dictated by their shot location and physical profile[cite: 509, 510].

---

## 3. Residual Capacity ($RC$)

[cite_start]**Residual Capacity** quantifies the "headroom" or untapped potential for increased offensive usage at a specific coordinate[cite: 315, 360, 533].

**Formula:**
$$RC = \frac{1}{Volume_{current}}$$

* **Logic:** High Residual Capacity identifies zones where a player has the highest potential for increased usage with the lowest expected decay in efficiency[cite: 351, 550]. It serves as the prescriptive inverse to traditional shot charts[cite: 350, 551].

---

## 4. Strategic Opportunity Value ($SOV$)

The **SOV** is the central composite metric of the Strategic Geometry framework. It ranks every hexbin on the floor by its untapped potential for a given player[cite: 343, 344, 543].

**Formula:**
$$SOV = \eta \times P(W) \times RC$$

* [cite_start]**$\eta$ (Localized Efficiency):** The baseline probability of a successful field goal at a specific coordinate[cite: 346, 546].
* [cite_start]**$P(W)$ (Whistle Expectancy):** The foul probability predicted by the EWE-v3.8, incorporating the player's Signature Delta[cite: 348, 349, 546].
* **$RC$ (Residual Capacity):** The inverse of the player's current shot frequency [cite: 350, 546-548].

---

## 5. Critical Sections

**Critical Sections** are the primary output of the **Optimization Blueprints**[cite: 352, 560, 561]. They are defined as the specific geospatial zones where high efficiency and high whistle expectancy intersect with high Residual Capacity[cite: 352, 541]. 

* [cite_start]**Tactical Use:** Attacking these sections allows a player to maximize their scoring floor by intentionally shifting usage into coordinates where the EWE identifies an untapped expectancy for whistles[cite: 339, 564, 571].

---