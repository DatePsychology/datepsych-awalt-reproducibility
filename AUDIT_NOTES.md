# Audit notes, reproducibility boundaries, and source-version checks

This package is intended to let readers independently run the calculations illustrated in the companion Substack article. It does **not** imply that the original study results have been replicated from raw data, or that any of the blog essay's disputed claims have been experimentally tested.

## Source provenance and reconstruction types

| Material | Status | Can this code reconstruct it from included inputs? |
| --- | --- | --- |
| Weisberg summary means, SDs and *d* | Reported in original Table 2 | Read as published aggregate statistics; no respondent-level analysis. |
| Pairwise agreeableness probability, point-biserial conversion | Analytical approximation using published rounded values | Yes, with distributional / sample-composition assumptions. |
| Mõttus TACT tertile probabilities | Published illustrative/model-based values | Independently derived by Gaussian quadrature, validated against the published values. |
| Rodrigues logistic coefficients and displayed CIs | Reported from fitted regression | `exp(B)` is recomputed; the original fit and exact CIs cannot be reconstructed without microdata. |
| Hypothetical 90% / 85% prevalence | *Illustration, not empirical evidence* | Plot only; it is not a scientific estimate. |
| Eagly–Hall directional counts, bias counts | Published review statistics | Count-derived percentages independently computed; review's primary coding cannot be recreated without underlying source documents and extraction. |
| Eagly–Hall consensus and magnitude-only correlations | Published review statistics | Transcribed and reported with source locations; not reestimated from study-level estimates. |

## Source version: Eagly & Hall (2025)

This package uses the **peer-reviewed 7-page article** in *Journal of Experimental Social Psychology*, volume 118, article 104713. It does not use the earlier preprint's obsolete 653 directional comparisons or 351/550 (64%) underestimation count.

The published article reports:

- Directional accuracy **570/673 (85%)**; misaligned **103/673 (15%)** (§2.1.1).
- Among eligible, directionally correct comparisons with comparable magnitudes, **329/471 (70%)** were underestimates (§2.1.2; Table 1).
- By domain, occupations **250/277 (90%)** underestimated; traits and behaviors **49/147 (33%)** underestimated, so **98/147 (67%)** overestimated (Table 1).
- Mean consensual sensitivity correlation **.77** overall, **.95** for occupations and **.64** for traits/behaviors (Table 2).
- Mean magnitude-only correlations for traits/behaviors **.26** (criteria higher for men) and **.33** (higher for women) (Table 4).

These are different *statistics*, with different denominators and interpretations. Multiple comparisons may come from the same study and are not 673 independent samples; directional agreement does not imply 85% accuracy predicting individuals. The magnitude-only correlations retain nonzero associations and are affected by restricting the analysis to same-direction attributes, not solely by perceptual errors.

## Conscientiousness / health illustration

Mõttus's **r = .05** for conscientiousness and a latent general-healthiness construct is **hypothesized**, informed by a synthesis of 18 meta-analyses. It is *not* a measured correlation of .05 with a single observed health outcome in a single cohort. The TACT calculations show approximately **34.7%** overall matching-tertile accuracy versus the 33.3% random benchmark. The **35.3% versus 31.4%** high/low conditional comparison is distinct from the net accuracy improvement. The companion critique was revised to acknowledge that Alexander's summary of these numbers is broadly accurate.

## Original graph versus our reconstruction

Weisberg et al. present an agreeableness distribution graphic as **Figure 10**. Alexander reproduced this figure. The independently generated overlap figure supplied here uses published means and SDs with normality and independence assumptions. Do not describe Alexander's original reused graph as though its provenance were unknown, and do not describe our figure as a display of raw participant data.

## Small numerical/rounding nuances

- The article cites approximately **58.1%** same-half agreement for *r* = .25, following Mõttus (2022). Under an exactly bivariate standard normal model with both variables dichotomized at their medians, the analytical formula `0.5 + asin(0.25)/pi` gives **58.043%**, ordinarily **58.0%** to one decimal. This discrepancy is approximately **0.057 percentage points**. It is immaterial to the conclusion, but code and prose should not silently equate the two to the last decimal. It may reflect simulation or approximation conventions; the source does not establish the cause.
- For the TACT plots, displayed percentage-point improvements are computed from the **displayed one-decimal rates**, as in the companion chart. Calculating first from unrounded Gaussian probabilities gives differences of 1.34, 7.14 and 15.83 percentage points, which may round differently (1.3, 7.1 and 15.8) at one decimal. Both express the same underlying results.
- Rodrigues confidence intervals are **rounded printed endpoints**; the sociosexual-desire lower limit 1.00 is not proof that a published *p* = .046 is contradictory.
- The stated odds ratios are **adjusted odds**, not probabilities, correlation coefficients, or AUCs. The retrospective infidelity outcome and highly selected recruitment mean the study is not prospective dating-risk validation.

## Scientific limitations

1. This is a transparent calculation-and-figure archive based on source reports, not an exact reproduction of each researcher's original software, instrument-level data, eligibility decisions, or sampling weights.
2. The sex-difference figure assumes normal curves with equal variances; the paper's empirical Figure 10 and the illustrative model should not be conflated.
3. TACT percent probabilities depend on normally distributed variables, the chosen correlation and equal-tertile thresholds; they do not offer a universal measure of predictive value for binary outcomes.
4. Eagly–Hall's judgments assess the direction/magnitude of **group differences**, sometimes using aggregated ratings and self-report criteria. Their results do not measure how well one person predicts a specific stranger's psychological attributes.
5. The computational package cannot adjudicate nonnumeric interpretive issues (causal claims about outgroup homogeneity, risk aversion or contempt; scope of AWALT; whether a heuristic improves actual decisions). Those questions require additional evidence and conceptual argument.

## Matching the latest article

The package is aligned to the **six numbered figures and published-source statistical discussion** in the latest locally available AWALT Substack HTML (`AWALT_Date_Psychology_Substack_Published_Source_Updated.html`). Some subsequent prose-only edits were made manually in Substack; they are not reproduced here. In particular, this repository should be linked as supporting *calculations and visualizations*, not as an archive of the final prose or of original participants' data. The generated images may differ in typography/layout from earlier Substack embeds but depict the same quantities.
