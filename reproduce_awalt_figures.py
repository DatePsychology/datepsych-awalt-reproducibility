#!/usr/bin/env python3
"""Reproduce six AWALT-critique figures and supporting statistical checks.

Inputs: plain CSV transcriptions of published summary statistics (no microdata).
Outputs: six PNGs and a plain-text results report, in this script's folder.
Python 3.10+; dependencies in requirements.txt. No network is required.

This reproduces the *quantities* represented in the companion critique's
figures; PNG appearance can vary with fonts and Matplotlib version.
"""
from __future__ import annotations

import csv
from pathlib import Path
from math import exp, asin, pi, sqrt

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import ticker
from scipy.integrate import quad
from scipy.stats import norm

ROOT = Path(__file__).resolve().parent
DARK = '#294d60'
TEAL = '#65969c'
LIGHT = '#d6e2e3'
ORANGE = '#c68b46'
INK = '#14293b'
GREY = '#596b7b'


def read_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def bivariate_cell_probability(r: float, xlo: float, xhi: float,
                                 ylo: float, yhi: float) -> float:
    """Deterministic conditional-normal integration; no simulated microdata."""
    cond_sd = sqrt(1 - r * r)

    def integrand(x: float) -> float:
        return norm.pdf(x) * (norm.cdf((yhi - r*x) / cond_sd)
                              - norm.cdf((ylo - r*x) / cond_sd))
    value, err = quad(integrand, xlo, xhi, epsabs=1e-11, epsrel=1e-11, limit=150)
    if err > 1e-7:
        raise RuntimeError(f'Integration numerical uncertainty: {err}')
    return value


def theoretical_tact(r: float) -> np.ndarray:
    t = norm.ppf(1/3)
    edges = [-np.inf, t, -t, np.inf]
    # Rows: outcome low/medium/high; columns: predictor low/medium/high.
    joint = np.array([[bivariate_cell_probability(r, edges[j], edges[j+1],
                                                  edges[i], edges[i+1])
                       for j in range(3)] for i in range(3)])
    assert np.allclose(joint.sum(axis=0), 1/3, atol=1e-8)
    return joint * 300.0  # conditional percentages, given each predictor tertile


def title_axes(ax, title: str = ''):
    if title:
        ax.set_title(title, fontsize=15, color=INK, pad=15, loc='center')
    ax.tick_params(colors=GREY, labelsize=10)
    for edge in ('top', 'right'):
        ax.spines[edge].set_visible(False)
    ax.spines['left'].set_color('#9ba8b1')
    ax.spines['bottom'].set_color('#9ba8b1')


def save(fig, basename: str):
    fig.savefig(ROOT / basename, dpi=170, facecolor='white', bbox_inches='tight')
    plt.close(fig)


def fig1(weisberg):
    male, female = f(weisberg, 'male_mean'), f(weisberg, 'female_mean')
    sd_m, sd_f = f(weisberg, 'male_sd'), f(weisberg, 'female_sd')
    d = f(weisberg, 'reported_cohens_d')
    pairwise = norm.cdf((female-male) / sqrt(sd_m*sd_m + sd_f*sd_f))
    xs = np.linspace(2.35, 5.25, 700)
    dm, df = norm.pdf(xs, male, sd_m), norm.pdf(xs, female, sd_f)
    fig, ax = plt.subplots(figsize=(11.5, 5.3))
    ax.plot(xs, dm, color=DARK, lw=2.7, label=f'Men: mean {male:.2f}')
    ax.plot(xs, df, color=TEAL, lw=2.7, label=f'Women: mean {female:.2f}')
    ax.fill_between(xs, dm, color=DARK, alpha=.12)
    ax.fill_between(xs, df, color=TEAL, alpha=.14)
    ax.axvline(male, linestyle=':', color=DARK, alpha=.65)
    ax.axvline(female, linestyle=':', color=TEAL, alpha=.65)
    ax.text(0.035, .94, f'd = {d:.2f}  |  {pairwise*100:.1f}% pairwise probability',
            transform=ax.transAxes, va='top', weight='bold', color=INK, fontsize=14)
    ax.set_xlabel('Agreeableness score (illustrative normal distributions)')
    ax.set_ylabel('Density')
    ax.set_xlim(2.35, 5.25)
    ax.set_ylim(bottom=0)
    ax.legend(loc='upper right', frameon=False)
    title_axes(ax)
    fig.tight_layout()
    save(fig, 'figure_01_agreeableness_overlap.png')
    return pairwise


def fig2(tact_rows, tactical):
    rs = [f(r, 'correlation') for r in tact_rows]
    ref = [f(r, 'matching_tertile_percent') for r in tact_rows]
    calc = [np.trace(tactical[r])/3 for r in rs]
    for v, published in zip(calc, ref):
        assert abs(v-published) <= .09, (v, published)
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    xx = np.arange(3)
    bars = ax.bar(xx, calc, width=.50, color=[TEAL, TEAL, DARK])
    ax.axhline(100/3, ls='--', color=ORANGE, lw=2,
               label='Random baseline: 33.3%')
    for bar, value in zip(bars, calc):
        ax.text(bar.get_x()+bar.get_width()/2, value+.8, f'{value:.1f}%',
                ha='center', va='bottom', weight='bold', fontsize=15, color=INK)
        ax.text(bar.get_x()+bar.get_width()/2, 25, f'+{round(value,1)-33.3:.1f} pts',
                ha='center', va='center', weight='bold', fontsize=12, color='white')
    ax.set_xticks(xx, [f'r = {r:.2f}' for r in rs])
    ax.set_ylim(0, 57)
    ax.set_yticks(np.arange(0, 60, 10), [f'{x}%' for x in range(0, 60, 10)])
    ax.set_ylabel('Correct matching-tertile classification')
    ax.legend(frameon=False, loc='upper left')
    title_axes(ax)
    fig.tight_layout()
    save(fig, 'figure_02_tact_accuracy.png')
    return calc


def fig3(tact_table, tact_theory):
    matrix = np.array([[f(row, col) for col in ('conscientiousness_low',
                                                'conscientiousness_medium',
                                                'conscientiousness_high')]
                       for row in tact_table])
    assert np.allclose(matrix.sum(axis=0),100,atol=.03)
    assert np.max(abs(matrix - tact_theory)) < .08
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('teals',[ '#eaf0f0','#a6c1c4','#65969c'])
    fig, ax = plt.subplots(figsize=(9.4, 6))
    im = ax.imshow(matrix, cmap=cmap, vmin=22, vmax=45, aspect='auto')
    for (i,j), val in np.ndenumerate(matrix):
        ax.text(j,i,f'{val:.1f}%',ha='center',va='center',weight='bold',
                fontsize=15,color=INK)
    ax.set_xticks(range(3), ['Low','Medium','High'])
    ax.set_yticks(range(3), [r['job_performance_tertile'] for r in tact_table])
    ax.set_xlabel('Conscientiousness tertile')
    ax.set_ylabel('Job-performance tertile')
    title_axes(ax, 'Where people fall when r = .25')
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.tight_layout()
    save(fig, 'figure_03_tact_grid.png')
    return matrix


def fig4(rodrigues_rows):
    fig, ax = plt.subplots(figsize=(12.2, 5.4))
    n=len(rodrigues_rows)
    yt=np.arange(n)[::-1]
    for i,(pos,row) in enumerate(zip(yt,rodrigues_rows)):
        low,high = f(row,'ci_low'), f(row,'ci_high')
        reported=f(row,'reported_adjusted_odds_ratio')
        c = TEAL if i<2 else DARK
        ax.plot([low,high],[pos,pos],c=c,lw=2.6,solid_capstyle='round')
        ax.scatter([reported],[pos],s=87,c=c,zorder=3,edgecolors='white')
        ax.text(3.45,pos,f'{reported:.2f}  [{low:.2f}–{high:.2f}]',
                va='center',ha='left',fontsize=11.5,color=INK)
        if row['variable']=='Sociosexual desire':
            ax.text(3.45,pos-.29,'reported p = .046; CI lower bound rounded',
                    va='center',fontsize=9.5,color=GREY)
    ax.set_xscale('log')
    ax.axvline(1,color=ORANGE,ls='--',lw=2)
    ax.set_xlim(.38,5.5)
    ax.set_xticks([.5,1,2,4],['0.5','1','2','4'])
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax.set_yticks(yt,[r['variable'] for r in rodrigues_rows])
    ax.set_ylim(-.65,n-.35)
    ax.set_xlabel('Adjusted odds ratio per 1 SD increase (95% confidence interval)')
    ax.grid(axis='x',alpha=.10)
    title_axes(ax)
    fig.tight_layout()
    save(fig,'figure_04_odds_ratios.png')


def fig5(prevalence_rows):
    fig, ax=plt.subplots(figsize=(11.5,4.6))
    yy=np.arange(len(prevalence_rows))[::-1]
    rates=[f(r,'percent_with_trait') for r in prevalence_rows]
    cols=[TEAL,DARK]
    for k,(y,rate) in enumerate(zip(yy,rates)):
        ax.barh(y,rate,color=cols[k],height=.52)
        ax.barh(y,100-rate,left=rate,color=LIGHT,alpha=.75,height=.52)
        ax.text(rate-1.5,y,f'{rate:.0f}%',color='white',weight='bold',
                fontsize=15,va='center',ha='right')
        ax.text(rate+(100-rate)/2,y,f'{100-rate:.0f}% do not',
                color=GREY,va='center',ha='center',fontsize=9)
    ax.set_xlim(0,100)
    ax.set_yticks(yy,[r['group'] for r in prevalence_rows])
    ax.set_xticks([0,25,50,75,100],[f'{i}%' for i in [0,25,50,75,100]])
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y',length=0)
    title_axes(ax,'Hypothetical prevalence of behavior X')
    fig.tight_layout()
    save(fig,'figure_05_hypothetical_prevalence.png')


def fig6(report_rows):
    obj={r['measure']:r for r in report_rows}
    matched=int(f(obj['Directional matches'],'value'))
    unmatched=int(f(obj['Directional mismatches'],'value'))
    n=matched+unmatched
    pct=100*matched/n
    fig,ax=plt.subplots(figsize=(11.6,3.6))
    ax.barh([0],[pct],color=TEAL,height=.48)
    ax.barh([0],[100-pct],left=[pct],color=LIGHT,height=.48)
    ax.text(pct/2,0,f'{pct:.0f}% direction matched',color='white',
            fontsize=17,weight='bold',ha='center',va='center')
    ax.text(pct+(100-pct)/2,0,f'{100-pct:.0f}%',color=INK,
            fontsize=12,weight='bold',ha='center',va='center')
    ax.set_xlim(0,100)
    ax.set_yticks([])
    ax.set_xticks([0,25,50,75,100],[f'{i}%' for i in [0,25,50,75,100]])
    title_axes(ax,f'Published review: {n} comparisons of estimated vs observed group differences')
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.tight_layout()
    save(fig,'figure_06_direction_accuracy.png')
    return matched,n,pct


def main():
    wei=read_csv('weisberg_summary_inputs.csv')[0]
    tacts=read_csv('mottus_tact_reference.csv')
    matrix=read_csv('mottus_table2_reference.csv')
    logr=read_csv('rodrigues_logistic_inputs.csv')
    eigbias=read_csv('eagly_hall_published_inputs.csv')
    eigreported=read_csv('eagly_hall_published_reported.csv')
    hypo=read_csv('hypothetical_prevalence.csv')
    sample={r['measure']:r for r in read_csv('rodrigues_sample_reported.csv')}
    auxiliary={r['measure']:r for r in read_csv('mottus_auxiliary_reported.csv')}

    # Independent numerical reconstruction of the Gaussian TACT proportions.
    tact_theory={f(row,'correlation'):theoretical_tact(f(row,'correlation')) for row in tacts}
    pair=fig1(wei)
    accuracies=fig2(tacts,tact_theory)
    matrix_plot=fig3(matrix,tact_theory[.25])
    fig4(logr)
    fig5(hypo)
    matched,n,pct=fig6(eigreported)

    assert abs(pair*100-63.3)<.07
    assert n==673 and matched==570 and round(pct)==85
    assert round(100*sum(int(x['underestimates']) for x in eigbias) /
                 sum(int(x['eligible_bias_comparisons']) for x in eigbias))==70
    assert sum(int(x['underestimates']) for x in eigbias)==329
    assert sum(int(x['eligible_bias_comparisons']) for x in eigbias)==471
    assert len(eigbias)==5
    assert int(f(sample['Total participants'],'value')) == int(f(sample['Men'],'value'))+int(f(sample['Women'],'value')) == 252
    assert round(100*f(sample['Reported past infidelity'],'value')/252,1)==f(sample['Reported past infidelity percent'],'value')
    assert abs((f(auxiliary['Health example high-high conditional probability'],'value')-f(auxiliary['Health example low-conscientiousness vs high-health conditional probability'],'value'))-3.9)<1e-8
    assert abs(f(auxiliary['Median-split same-half agreement at r 0.25'],'value') - 100*(.5+asin(.25)/pi))<.06
    assert [(r['variable'],round(exp(f(r,'standardized_logit_coefficient')),2)) for r in logr] == [
        ('Sociosexual behavior',2.25),('Sociosexual desire',1.28),('Commitment',.65)]

    nmen,nwomen=int(wei['male_n']),int(wei['female_n'])
    p=nwomen/(nmen+nwomen)
    d=f(wei,'reported_cohens_d')
    rpb=d*sqrt(p*(1-p))/sqrt(1+d*d*p*(1-p))
    besd=100*(.5+asin(.25)/pi)
    b2=[r for r in eigbias if r['criterion_category']=='Traits and behaviors'][0]
    lines=[
        'AWALT CRITIQUE — RECONSTRUCTION RESULTS',
        '=======================================',
        'Inputs: published aggregate statistics + clearly hypothetical values; not participant-level data.',
        '',
        'Weisberg et al. (2011), Agreeableness',
        f'  Male n={nmen}, female n={nwomen}; male mean={f(wei,"male_mean"):.2f}, female mean={f(wei,"female_mean"):.2f}; both SDs={f(wei,"male_sd"):.2f}.',
        f'  Published Cohen d: {d:.2f}; rounded-mean/SD d: {(f(wei,"female_mean")-f(wei,"male_mean"))/f(wei,"male_sd"):.2f}.',
        f'  Approximate point-biserial r using sample proportions and d: {rpb:.4f}.',
        f'  Normal independent-draw P(woman > man): {pair*100:.4f}% (article rounds to 63.3%).',
        '',
        'Mottus (2022), normal-model TACT',
    ]
    for row,acc in zip(tacts,accuracies):
        lines.append(f'  r={f(row,"correlation"):.2f}: computed matching accuracy={acc:.4f}%; published rounded={f(row,"matching_tertile_percent"):.1f}%; baseline=33.3333%.')
    lines += [
        f'  At r=.25, low→low/high→high={matrix_plot[0,0]:.2f}%; medium→medium={matrix_plot[1,1]:.2f}%.',
        f'  Median-split analytical agreement at r=.25: {besd:.4f}% (Mottus reports 58.1%; see AUDIT_NOTES).',
        '  Hypothetical healthiness example: 35.3% vs 31.4% = 3.9 percentage points; 34.7% matching-tertile accuracy is a different quantity.',
        '',
        'Rodrigues et al. (2017), Table 2, adjusted logistic coefficients',
    ]
    for row in logr:
        lines.append(f'  {row["variable"]}: B={f(row,"standardized_logit_coefficient"):.2f}, exp(B)={exp(f(row,"standardized_logit_coefficient")):.4f}, reported OR={f(row,"reported_adjusted_odds_ratio"):.2f}, displayed 95% CI=[{f(row,"ci_low"):.2f}, {f(row,"ci_high"):.2f}].')
    lines += [
        f'  Selected sample n=252, men=201, women=51; past infidelity: 172/252={172/252*100:.4f}%.',
        '  Note: the reported rounded 1.00 CI endpoint for desire is compatible with printed p=.046.',
        '',
        'Hypothetical prevalence illustration: women 90%, men 85%; these are NOT observations.',
        '',
        'Eagly & Hall (2025), FINAL peer-reviewed publication',
        f'  Directional agreement: {matched}/{n} = {pct:.4f}% (reported rounded 85%).',
    ]
    all_n=sum(int(x['eligible_bias_comparisons']) for x in eigbias)
    all_under=sum(int(x['underestimates']) for x in eigbias)
    lines.append(f'  Eligible bias comparisons: {all_under}/{all_n} = {all_under/all_n*100:.4f}% underestimates (reported 70%).')
    for row in eigbias:
        un=int(row['underestimates']); den=int(row['eligible_bias_comparisons'])
        lines.append(f'    {row["criterion_category"]}: underestimates={un}/{den}={un/den*100:.2f}%; overestimates={(den-un)/den*100:.2f}%.')
    for row in eigreported:
        if not row['numerator']:
            lines.append(f'  Reported (not independently reestimated) {row["measure"]}: {row["value"]}.')
    lines += ['','All validation checks passed. Figures 1–6 generated.']
    report='\n'.join(lines)+'\n'
    (ROOT/'reconstruction_results.txt').write_text(report,encoding='utf-8')
    print(report)


if __name__=='__main__':
    main()
