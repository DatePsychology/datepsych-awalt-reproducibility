# Are Gender Generalizations Really Wrong Most of the Time? — Reproducibility Materials

Code, traceable source-statistic transcriptions, numerical checks, and six figures accompanying a [methodological review](https://datepsych.substack.com/p/what-can-gender-differences-really) of Date Psychology's 2022 essay [“Why AWALT Will Be Wrong Most of the Time”](https://datepsychology.com/why-awalt-will-be-wrong-most-of-the-time/).

**Scope.** This is a *published-statistic reconstruction*, not an independent replication of the original studies using participant-level data. The Gaussian plots and TACT calculations depend on explicitly stated distributional assumptions. The illustrative 90%/85% prevalence example is **hypothetical**, not evidence of the prevalence of any actual behavior. The Eagly–Hall results are from the **final 2025 peer-reviewed paper**, not an earlier manuscript. See [AUDIT_NOTES.md](AUDIT_NOTES.md) for caveats and verification boundaries.

## Repository contents

| File | What it does |
| --- | --- |
| `reproduce_awalt_figures.py` | Single entry point: computes checks, generates all six figures, and writes a plain-text report. |
| `weisberg_summary_inputs.csv` | Weisberg et al. (2011), sample composition, agreeableness means, SDs, and reported Cohen's *d*. |
| `mottus_tact_reference.csv` | Published/model-based TACT matching-tertile accuracies for correlations .05, .25, and .50. |
| `mottus_table2_reference.csv` | Mottus (2022), published 3 × 3 conditional percentages for *r* = .25. |
| `mottus_auxiliary_reported.csv` | Additional published health and median-split numerical examples discussed in the critique. |
| `rodrigues_sample_reported.csv` | Reported sample sizes and retrospective infidelity counts, for denominator checks. |
| `rodrigues_logistic_inputs.csv` | Rodrigues et al. (2017), Table 2 coefficients, adjusted odds ratios, displayed confidence limits, and reported *p* value. |
| `eagly_hall_published_inputs.csv` | Published Eagly & Hall (2025), Table 1 underestimation counts by criterion category. |
| `eagly_hall_published_reported.csv` | Published Eagly & Hall headline and subgroup results from sections 2.1–2.2 and Tables 2/4. |
| `hypothetical_prevalence.csv` | Fictional 90% women / 85% men illustration, explicitly not observed data. |
| `figure_01_agreeableness_overlap.png` | Separate normal-model reconstruction of overlapping agreeableness distributions. |
| `figure_02_tact_accuracy.png` | Matching-tertile accuracy versus the 33.3% chance benchmark. |
| `figure_03_tact_grid.png` | Conditional 3 × 3 TACT percentages for *r* = .25. |
| `figure_04_odds_ratios.png` | Adjusted odds ratios, published rounded 95% CIs, and null line at OR = 1. |
| `figure_05_hypothetical_prevalence.png` | Hypothetical difference between within-group prevalence and discrimination. |
| `figure_06_direction_accuracy.png` | Published Eagly–Hall: 570 of 673 directionally correct comparisons. |
| `reconstruction_results.txt` | Expected output for the numeric reconstruction and validation checks. |
| `AUDIT_NOTES.md` | Sources, assumptions, limitations, version audit, and a small rounding nuance. |
| `requirements.txt` | Python dependencies. |

## Reproduce the results

Use Python **3.10 or newer**. From this repository's root directory:

```bash
python -m pip install -r requirements.txt
python reproduce_awalt_figures.py
```

The command prints the derived quantities, runs validation checks, and overwrites the six figure PNGs and `reconstruction_results.txt` in the repository directory. It does **not** fetch anything online or need proprietary research datasets. A failed assertion indicates a disagreement with a reported rounded value or an input-integrity check.

The numerical values should reproduce across supported software versions within the stated rounding tolerances. Pixel-by-pixel figure layout is **not** guaranteed across plotting-library versions, operating systems, or installed fonts.

## Figure-by-figure methods

**Figure 1 — Agreeableness overlap.** Uses the 2011 paper's reported means 3.65 and 3.89, SDs .50 and .50, and *d* = .48. Normal distributions with published summary parameters are plotted; they are **not the actual respondents' data**. For independent draws, the pairwise probability is `norm.cdf((3.89-3.65)/sqrt(.5**2+.5**2)) = 63.285%`. The original Alexander article reproduced Weisberg et al.'s *own Figure 10*; our Figure 1 is a separate model-based illustration.

**Figure 2 — TACT accuracy.** Reconstructs the expected 3-tertile diagonal-matching rate by numerically integrating a bivariate normal with correlations `.05`, `.25`, and `.50`. Those expected values round to the published figures **34.7%, 40.5%, and 49.2%**. The chance rate for independent, evenly populated thirds is 33⅓%, **not 50%**. The labels for percentage-point improvements subtract displayed one-decimal rates for consistency with the companion article (+1.4, +7.2, +15.9 points).

**Figure 3 — Conditional TACT grid.** Displays the nine numbers in Mõttus's published Table 2, reversing the outcome-row order to show *low → medium → high* from top to bottom. The program also independently computes the Gaussian cell probabilities by deterministic quadrature and verifies that they agree to within rounding. The columns total ~100%.

**Figure 4 — Infidelity-model odds ratios.** The script also checks the source sample composition (201 men and 51 women) and the reported 172/252 (68.3%) past-infidelity count.  Takes *B* = .81, .25, −.43 from the published adjusted logistic-regression table and checks `exp(B) = OR` against reported ORs 2.25, 1.28, 0.65. It plots reported, **rounded** confidence limits rather than trying to infer exact standard errors. It does not fit a new model, calculate individual predictive accuracy, or turn coefficients into correlations. The reported *p* = .046 for sociosexual desire is compatible with a lower 95% CI endpoint printed as 1.00 after rounding.

**Figure 5 — Hypothetical illustration.** The 90% versus 85% within-group prevalence rates were invented solely to demonstrate a mathematical possibility: a trait may be common among both groups even though group membership has little discriminatory value. Neither percentage is a measured population estimate.

**Figure 6 — Gender-stereotype direction accuracy.** Uses Eagly & Hall's **published 2025** counts, 570 agreement and 103 disagreement comparisons; `570/673 = 84.695%`, rounded to 85%. This is the direction of **group-average differences**, not accuracy at classifying individuals. The script also checks the published underestimation subgroup counts, 329/471 (70%) overall, and preserves the published but *not independently recomputed* sensitivity correlations in the results text.

## Core sources

1. [Alexander (2022), “Why AWALT Will Be Wrong Most of the Time”](https://datepsychology.com/why-awalt-will-be-wrong-most-of-the-time/) — article under review.
2. Weisberg, Y. J., DeYoung, C. G., & Hirsh, J. B. (2011). [“Gender Differences in Personality across the Ten Aspects of the Big Five.”](https://doi.org/10.3389/fpsyg.2011.00178) *Frontiers in Psychology*, 2, 178. **Participants, Table 2, Figure 10.**
3. Mõttus, R. (2022). [“What Correlations Mean for Individual People: A Tutorial for Researchers, Students and the Public.”](https://doi.org/10.5964/ps.7467) *Personality Science*, 3. **TACT, Table 2, and examples.**
4. Rodrigues, D., Lopes, D., & Pereira, M. (2017). [“Sociosexuality, Commitment, Sexual Infidelity, and Perceptions of Infidelity: Data From the Second Love Web Site.”](https://doi.org/10.1080/00224499.2016.1145182) *Journal of Sex Research*, 54(2), 241–253. **Table 2.** [Open university-hosted copy](https://repositorio.iscte-iul.pt/entities/publication/8f9ecdd4-081f-4bf8-95a1-01263421c85b).
5. Eagly, A. H., & Hall, J. A. (2025). [“The Kernel of Truth in Gender Stereotypes: Consider the Avocado, Not the Apple.”](https://doi.org/10.1016/j.jesp.2024.104713) *Journal of Experimental Social Psychology*, 118, 104713. **Final published manuscript, sections 2.1–2.2, Tables 1–4.**

The companion article contains additional references for its qualitative and methodological discussion. Those claims are not computationally reproduced by this package.

**No participant records, copyrighted PDFs, or third-party article copies are distributed in this repository.** CSVs contain brief, explicitly attributed transcriptions of reported aggregate figures, and all figures and scripts are newly generated for the accompanying critique.
