#%% DATA ANALYSIS + PLOTTING FOR ONE-P PHOTOSTIM EXPERIMENTS
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from _exp_metainfo_.data_paths import onePresults_object_path
from archive import alloptical_utils_pj as aoutils
from _utils_ import alloptical_plotting as aoplot
from funcsforprajay import funcs as pj

import onePexperiment.OnePhotonStimMain as oneP
from onePexperiment.OnePhotonStimAnalysis_main import OnePhotonStimResults
from onePexperiment.OnePhotonStimMain import OnePhotonStimPlots as onepplots

Results: OnePhotonStimResults = OnePhotonStimResults.load()
from funcsforprajay.plotting.plotting import plot_bar_with_points

# import onePstim superobject that will collect analyses from various individual experiments
onePresults = aoutils.import_resultsobj(pkl_path=onePresults_object_path)

# %% 3.0) PLOT OF PHOTOSTIM RESPONSES <30SEC PRE SZ ONSET AND <30SEC POST SZ OFFSET

interictal_response_magnitudes_midsz = Results.photostim_responses['interictal - mid']
interictal_response_magnitudes_presz = Results.photostim_responses['interictal - presz']
interictal_response_magnitudes_postsz = Results.photostim_responses['interictal - postsz']
interictal_response_magnitudes_szexclude = Results.photostim_responses['interictal - sz excluded']
baseline_response_magnitudes = Results.photostim_responses['baseline']


# BASELINE
baseline_resposnes = []
for trial, responses in baseline_response_magnitudes.items():
    baseline_resposnes.extend(list(responses))

baseline_response_magnitudes_exp = {}
for exp in OnePhotonStimResults.expids:
    _responses = []
    for trial, responses in baseline_response_magnitudes.items():
        if exp in trial:
            _responses.extend(responses)
    baseline_response_magnitudes_exp[exp] = np.mean(_responses)


# INTERICTAL - 
interictal_resposnes_szexclude = []
for trial, responses in interictal_response_magnitudes_szexclude.items():
    interictal_resposnes_szexclude.extend(list(responses))

interictal_response_magnitudes_exp = {}
for exp in OnePhotonStimResults.expids:
    _responses = []
    for trial, responses in interictal_response_magnitudes_szexclude.items():
        if exp in trial:
            _responses.extend(responses)
    interictal_response_magnitudes_exp[exp] = np.mean(_responses)


# INTERICTAL - mid SZ
interictal_resposnes_midsz = []
for trial, responses in interictal_response_magnitudes_midsz.items():
    interictal_resposnes_midsz.extend(list(responses))

interictal_response_magnitudes_midsz_exp = {}
for exp in OnePhotonStimResults.expids:
    _responses = []
    for trial, responses in interictal_response_magnitudes_midsz.items():
        if exp in trial:
            _responses.extend(responses)
    interictal_response_magnitudes_midsz_exp[exp] = np.mean(_responses)


# INTERICTAL - PRE SZ
interictal_resposnes_presz = []
for trial, responses in interictal_response_magnitudes_presz.items():
    interictal_resposnes_presz.extend(list(responses))

interictal_response_magnitudes_presz_exp = {}
for exp in OnePhotonStimResults.expids:
    _responses = []
    for trial, responses in interictal_response_magnitudes_presz.items():
        if exp in trial:
            _responses.extend(responses)
    interictal_response_magnitudes_presz_exp[exp] = np.mean(_responses)



# INTERICTAL - POST SZ
interictal_resposnes_postsz = []
for trial, responses in interictal_response_magnitudes_postsz.items():
    interictal_resposnes_postsz.extend(list(responses))

interictal_response_magnitudes_postsz_exp = {}
for exp in OnePhotonStimResults.expids:
    _responses = []
    for trial, responses in interictal_response_magnitudes_postsz.items():
        if exp in trial:
            _responses.extend(responses)
    interictal_response_magnitudes_postsz_exp[exp] = np.mean(_responses)



fig, ax = plt.subplots(figsize=[2, 3], dpi = 100)
plot_bar_with_points(data=[interictal_resposnes_midsz, interictal_resposnes_presz, interictal_resposnes_postsz, interictal_resposnes_szexclude,
                           baseline_resposnes],
                     x_tick_labels=['Mid', 'Pre-sz', 'Post-sz', 'Interictal', 'Baseline'],
                     points=True, bar=False, colors=['steelblue', 'orange', 'red', 'green', 'gray'], fig=fig, ax=ax, show=False, s=10,
                     x_label='', y_label='Avg. dFF', alpha=0.7, lw=0.5)
fig.tight_layout(pad=0.2)
fig.show()


fig, ax = plt.subplots(figsize=[2, 3], dpi = 100)
plot_bar_with_points(data=[list(interictal_response_magnitudes_presz_exp.values()), list(interictal_response_magnitudes_postsz_exp.values()),
                           list(interictal_response_magnitudes_exp.values()), list(baseline_response_magnitudes_exp.values())],
                     x_tick_labels=['Pre-sz', 'Post-sz', 'Interictal', 'Baseline'],
                     points=True, bar=False, colors=['orange', 'red', 'green', 'gray'], fig=fig, ax=ax, show=False, s=10,
                     x_label='', y_label='Avg. dFF', alpha=0.7, lw=1, ylims=[-0.2, 3])
fig.tight_layout(pad=0.2)
fig.show()


print(f"P(t-test - (indiv. trials) response - baseline vs. interictal): {stats.ttest_ind(baseline_resposnes, interictal_resposnes_szexclude)[1]:.3e}")
print(f"P(t-test - (indiv. trials) response - baseline vs. postsz): {stats.ttest_ind(baseline_resposnes, interictal_resposnes_postsz)[1]:.3e}")
print(f"P(t-test - (indiv. trials) response - baseline vs. presz): {stats.ttest_ind(baseline_resposnes, interictal_resposnes_presz)[1]:.3e}")
print(f"P(t-test - (indiv. trials) response - presz vs. interictal): {stats.ttest_ind(interictal_resposnes_szexclude, interictal_resposnes_presz)[1]:.3e}")
print(f"P(t-test - (indiv. trials) response - postsz vs. interictal): {stats.ttest_ind(interictal_resposnes_szexclude, interictal_resposnes_postsz)[1]:.3e}")
print(f"P(t-test - (indiv. trials) response - postsz vs. presz): {stats.ttest_ind(interictal_resposnes_presz, interictal_resposnes_postsz)[1]:.3e}")


# %% 2.0) TIME TO SZ ONSET VS.: PRE-STIM FLU, AND PHOTOSTIM RESPONSES - PLOT - time to seizure onset vs. pre-stim Flu

fig, ax = plt.subplots(figsize=(2.5,4))
onepplots.plotTimeToOnset_preStimFlu(fig=fig, ax=ax, run_pre4ap_trials=True, run_post4ap_trials=False, x_lim=[-4, 5], alpha=0.1, lw=5, s=50)
fig.show()

fig, ax = plt.subplots(figsize=(4,4))
onepplots.plotTimeToOnset_preStimFlu(fig=fig, ax=ax, run_pre4ap_trials=False, run_post4ap_trials=True, alpha=0.1, lw=5, s=50, y_lim=[0, 2000])
fig.show()

# %% 2.1) PLOT - time to seizure onset vs. photostim response Flu

fig, ax = plt.subplots(figsize=(2.5,4))
onepplots.plotTimeToOnset_photostimResponse(fig=fig, ax=ax, run_pre4ap_trials=True, run_post4ap_trials=False, x_lim=[-4, 5], alpha=0.1, lw=5, s=50)
fig.show()

fig, ax = plt.subplots(figsize=(4,4))
onepplots.plotTimeToOnset_photostimResponse(fig=fig, ax=ax, run_pre4ap_trials=False, run_post4ap_trials=True, alpha=0.1, lw=5, s=50, y_lim=[-0.4,2.5])
fig.show()


# %% 1.0) pre-stim Flu vs. Photostim Responses

fig, ax = plt.subplots(figsize=[3.5,3])
oneP.OnePhotonStimPlots.plotPrestimF_photostimFlu(fig=fig, ax=ax, run_pre4ap_trials=True, run_post4ap_trials=False, alpha=0.25,
                                                  x_lim=[0, 2000], y_lim=[-0.5, 3.0], s=50)
ax.set_title('(baseline: gray)', wrap=True)
fig.show()

fig, ax = plt.subplots(figsize=[3.5,3])
oneP.OnePhotonStimPlots.plotPrestimF_photostimFlu(fig=fig, ax=ax, run_pre4ap_trials=False, run_post4ap_trials=True, alpha=0.25,
                                                  x_lim=[0, 2000], y_lim=[-0.5, 3.0], interictal=True, ictal=False, s=50)
ax.set_title('(inter-ictal: green)', wrap=True)
fig.show()

fig, ax = plt.subplots(figsize=[3.5,3])
oneP.OnePhotonStimPlots.plotPrestimF_photostimFlu(fig=fig, ax=ax, run_pre4ap_trials=False, run_post4ap_trials=True, alpha=0.25,
                                                  x_lim=[0, 2000],  y_lim=[-0.5, 3.0], ictal=True, interictal=False, s=50)
ax.set_title('(ictal: purple)', wrap=True)
fig.show()


# %% 1.1) pre-stim Flu  vs. decay constant

fig, ax = plt.subplots(figsize=[3.5,3])
oneP.OnePhotonStimPlots.plotPrestimF_decayconstant(fig=fig, ax=ax, run_pre4ap_trials=True, run_post4ap_trials=False, x_lim=[-150, 150],
                                                   y_lim=[0, 1500], alpha=0.25)
# ax.set_title('(baseline: gray)', wrap=True)
fig.show()

fig, ax = plt.subplots(figsize=[3.5,3])
oneP.OnePhotonStimPlots.plotPrestimF_decayconstant(fig=fig, ax=ax, run_pre4ap_trials=False, run_post4ap_trials=True, ignore_cache=True, run_trials=[], skip_trials=[])
# ax.set_title('(ictal: purple, inter-ictal: green)', wrap=True)
fig.show()






# %% ## collection plots of many trials sub divided as specified - avg flu trace 1p stim plots
# pre-4ap trials plot
nrows = 4
ncols = 3
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 5))
counter = 0; write_full_text=True
for pkl_path in onePresults.mean_stim_responses['pkl_list']:
    if list(onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses['pkl_list'] == pkl_path, 'pre-4ap response'])[0] != '-':

        expobj, experiment = aoutils.import_expobj(pkl_path=pkl_path, verbose=False)
        ax = axs[counter//ncols, counter % ncols]

        fig, ax, flu_list, mean_response, decay_constant = aoplot.plot_flu_1pstim_avg_trace(expobj, x_axis='time', individual_traces=True, stim_span_color=None, y_axis='dff', quantify=True,
                                                                                            show=False, fig=fig, ax=ax, write_full_text=write_full_text, shrink_text=1.25)
        # fig, ax = aoplot.plot_lfp_1pstim_avg_trace(expobj, x_axis='time', individual_traces=False, pre_stim_sec=0.25, post_stim_sec=0.75, optoloopback=True, show=False)

        axs[counter // ncols, counter % ncols] = ax

        counter += 1
        write_full_text = False  # switch off write full text option after the first plot

fig.suptitle('Pre-4ap trials only, avg flu trace for 1p stim', y=0.995)
fig.show()


# post-4ap stims out of sz trials plot
nrows = 4
ncols = 3
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 5))
counter = 0; write_full_text=True
for pkl_path in onePresults.mean_stim_responses['pkl_list']:
    if list(onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses['pkl_list'] == pkl_path, 'post-4ap response (outside sz)'])[0] != '-':
        expobj, experiment = aoutils.import_expobj(pkl_path=pkl_path, verbose=False)
        ax = axs[counter//ncols, counter % ncols]

        title = 'Avg. trace - stims out of sz -'

        fig, ax, flu_list, mean_response, decay_constant = aoplot.plot_flu_1pstim_avg_trace(expobj, x_axis='time', individual_traces=True, stim_span_color=None, y_axis='dff', quantify=True,
                                                                                            show=False, fig=fig, ax=ax, write_full_text=write_full_text, shrink_text=1.25, stims_to_analyze=expobj.stims_out_sz,
                                                                                            title=title)
        # fig, ax = aoplot.plot_lfp_1pstim_avg_trace(expobj, x_axis='time', individual_traces=False, pre_stim_sec=0.25, post_stim_sec=0.75, optoloopback=True, show=False)

        axs[counter // ncols, counter % ncols] = ax

        counter += 1
        write_full_text = False  # switch off write full text option after the first plot

fig.suptitle('Post-4ap trials, stims out of sz, avg flu trace for 1p stim', y=0.995)
fig.show()



# post-4ap stims during sz trials plot
nrows = 4
ncols = 3
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 5))
counter = 0; write_full_text = True
for pkl_path in onePresults.mean_stim_responses['pkl_list']:
    if list(onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses['pkl_list'] == pkl_path, 'post-4ap response (during sz)'])[0] != '-':
        expobj, experiment = aoutils.import_expobj(pkl_path=pkl_path, verbose=False)
        ax = axs[counter//ncols, counter % ncols]

        title = 'Avg. trace - stims in sz -'

        fig, ax, flu_list, mean_response, decay_constant = aoplot.plot_flu_1pstim_avg_trace(expobj, x_axis='time', individual_traces=True, stim_span_color=None, y_axis='dff', quantify=True,
                                                                                            show=False, fig=fig, ax=ax, write_full_text=write_full_text, shrink_text=1.25, stims_to_analyze=expobj.stims_in_sz,
                                                                                            title=title)
        # fig, ax = aoplot.plot_lfp_1pstim_avg_trace(expobj, x_axis='time', individual_traces=False, pre_stim_sec=0.25, post_stim_sec=0.75, optoloopback=True, show=False)

        axs[counter // ncols, counter % ncols] = ax

        counter += 1
        write_full_text = False  # switch off write full text option after the first plot

fig.suptitle('Post-4ap trials, stims in sz, avg flu trace for 1p stim', y=0.995)
fig.show()

# %% ## avg LFP trace 1p stim plots
# pre-4ap trials plot
nrows = 4
ncols = 3
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 5))
counter = 0; write_full_text=True
for pkl_path in onePresults.mean_stim_responses['pkl_list']:
    if list(onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses['pkl_list'] == pkl_path, 'pre-4ap response'])[0] != '-':

        expobj = aoutils.import_expobj(pkl_path=pkl_path, verbose=False)
        ax = axs[counter//ncols, counter % ncols]

        fig, ax = aoplot.plot_lfp_1pstim_avg_trace(expobj, x_axis='time', individual_traces=False, pre_stim=0.25, post_stim=0.75, optoloopback=True, show=False, fig=fig, ax=ax,
                                                   write_full_text=write_full_text)

        axs[counter // ncols, counter % ncols] = ax

        counter += 1
        write_full_text = False  # switch off write full text option after the first plot

fig.suptitle('Pre-4ap trials only, avg LFP trace for 1p stim', y=0.995)
fig.show()


# post-4ap stims out of sz trials plot
nrows = 4
ncols = 3
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 5))
counter = 0; write_full_text=True
for pkl_path in onePresults.mean_stim_responses['pkl_list']:
    if list(onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses['pkl_list'] == pkl_path, 'post-4ap response (outside sz)'])[0] != '-':
        expobj = aoutils.import_expobj(pkl_path=pkl_path)
        ax = axs[counter//ncols, counter % ncols]

        title = 'Avg. trace - stims out of sz -'

        fig, ax = aoplot.plot_lfp_1pstim_avg_trace(expobj, x_axis='time', individual_traces=False, pre_stim=0.25, post_stim=0.75, optoloopback=True, show=False, fig=fig, ax=ax,
                                                   write_full_text=write_full_text, stims_to_analyze=expobj.stims_out_sz)

        axs[counter // ncols, counter % ncols] = ax

        counter += 1
        write_full_text = False  # switch off write full text option after the first plot

fig.suptitle('Post-4ap trials, stims out of sz, avg LFP trace for 1p stim', y=0.995)
fig.show()



# post-4ap stims during sz trials plot
nrows = 4
ncols = 3
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 5))
counter = 0; write_full_text = True
for pkl_path in onePresults.mean_stim_responses['pkl_list']:
    if list(onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses['pkl_list'] == pkl_path, 'post-4ap response (during sz)'])[0] != '-':
        expobj = aoutils.import_expobj(pkl_path=pkl_path, verbose=False)
        ax = axs[counter//ncols, counter % ncols]

        title = 'Avg. trace - stims in sz -'

        fig, ax = aoplot.plot_lfp_1pstim_avg_trace(expobj, x_axis='time', individual_traces=False, pre_stim=0.25, post_stim=0.75, optoloopback=True, show=False, fig=fig, ax=ax,
                                                   write_full_text=write_full_text, stims_to_analyze=expobj.stims_in_sz)

        axs[counter // ncols, counter % ncols] = ax

        counter += 1
        write_full_text = False  # switch off write full text option after the first plot

fig.suptitle('Post-4ap trials, stims in sz, avg LFP trace for 1p stim', y=0.995)
fig.show()




# %% ## LFP + stims plots
# aoplot.plot_lfp_stims(expobj, x_axis='time', figsize=[30, 3], sz_markings=True)


# Mean Raw Flu whole trace plots
nrows = 21
ncols = 1
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 15, nrows * 3))
counter = 0
for pkl_path in onePresults.mean_stim_responses['pkl_list']:
    expobj, experiment = aoutils.import_expobj(pkl_path=pkl_path, verbose=False)
    ax = axs[counter]

    fig, ax = aoplot.plotMeanRawFluTrace(expobj, stim_span_color='lightgrey', x_axis='time', title='raw Flu trace, stims shown - ',
                                         show=False, fig=fig, ax=ax, stim_lines=False)

    counter += 1
fig.suptitle('All trials, 1p photostim experiments', y=0.995)
fig.show()


# %% ## ADD DECAY CONSTANTS TO THE mean_stim_responses dataframe

# pre-4ap trials
for pkl_path in onePresults.mean_stim_responses['pkl_list']:
    if list(onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses['pkl_list'] == pkl_path, 'pre-4ap response'])[0] != '-':

        expobj, experiment = aoutils.import_expobj(pkl_path=pkl_path)

        flu_list, mean_response, decay_constant = aoplot.plot_flu_1pstim_avg_trace(expobj, x_axis='time', y_axis='dff', show=False, quantify=True)
        onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses[
                                                'pkl_list'] == expobj.pkl_path, 'Decay constant pre-4ap (secs.)'] = decay_constant




# post-4ap stims out of sz trials
for pkl_path in onePresults.mean_stim_responses['pkl_list']:
    if list(onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses['pkl_list'] == pkl_path, 'post-4ap response (outside sz)'])[0] != '-':

        expobj, experiment = aoutils.import_expobj(pkl_path=pkl_path)

        flu_list, mean_response, decay_constant = aoplot.plot_flu_1pstim_avg_trace(expobj, x_axis='time', y_axis='dff', stims_to_analyze=expobj.stims_out_sz, show=False, quantify=True)
        onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses[
                                                'pkl_list'] == expobj.pkl_path, 'Decay constant post-4ap outside sz (secs.)'] = decay_constant



# post-4ap stims during sz trials
for pkl_path in onePresults.mean_stim_responses['pkl_list']:
    if list(onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses['pkl_list'] == pkl_path, 'post-4ap response (during sz)'])[0] != '-':

        expobj, experiment = aoutils.import_expobj(pkl_path=pkl_path)

        flu_list, mean_response, decay_constant = aoplot.plot_flu_1pstim_avg_trace(expobj, x_axis='time', y_axis='dff', stims_to_analyze=expobj.stims_in_sz, show=False, quantify=True)
        onePresults.mean_stim_responses.loc[onePresults.mean_stim_responses[
                                                'pkl_list'] == expobj.pkl_path, 'Decay constant post-4ap during sz (secs.)'] = decay_constant
onePresults.save()

# %% BAR PLOT OF RESPONSE MAGNITUDE FOR 1P STIM EXPERIMENTS

data = [[rp for rp in onePresults.mean_stim_responses.iloc[:, 1] if rp != '-']]
data.append([rp for rp in onePresults.mean_stim_responses.iloc[:,2] if rp != '-'])
# data.append([rp for rp in onePresults.mean_stim_responses.iloc[:,3] if rp != '-'])

fig, ax = plt.subplots(figsize=[3, 5])
pj.plot_bar_with_points(data=data, title='response magnitudes - 1p stim experiments', x_tick_labels=['pre-4ap', 'post-4ap'],
                        points=True, bar=False, colors=['black', 'green', 'purple'], fig=fig, ax=ax, show=False,
                        x_label='experiment groups', y_label='Avg. dFF (across all stim trials)', alpha=0.4,
                        expand_size_x=0.5, expand_size_y=1.3, shrink_text=1.35)
save_path = '/home/pshah/mnt/qnap/Analysis/' + 'onePstim_response_quant'
print('saving fig to: ', save_path)
fig.savefig(fname=save_path + '.png', transparent=True, format='png')
fig.savefig(fname=save_path + '.svg', transparent=True, format='svg')



# %% BAR PLOT OF DECAY CONSTANT FOR 1P STIM EXPERIMENTS

data = [list(onePresults.mean_stim_responses[onePresults.mean_stim_responses.iloc[:, -3].notnull()].iloc[:, -3])]
data.append(list(onePresults.mean_stim_responses[onePresults.mean_stim_responses.iloc[:, -2].notnull()].iloc[:, -2]))
# data.append(ls(onePresults.mean_stim_responses[onePresults.mean_stim_responses.iloc[:, -1].notnull()].iloc[:, -1]))

fig, ax = plt.subplots(figsize=[3, 5])
pj.plot_bar_with_points(data=data, title='decay constants - 1p stim experiments', legend_labels=list(onePresults.mean_stim_responses.columns[-3:]),
                        points=True, bar=False, colors=['black', 'green', 'purple'], fig=fig, ax=ax, show=False,
                        x_label='experiment groups', y_label='Avg. Decay constant (secs.)', alpha=0.4,
                        expand_size_x=0.9, expand_size_y=1.2, shrink_text=1.35)
save_path = '/home/pshah/mnt/qnap/Analysis/' + 'onePstim_decay_quant'
print('saving fig to: ', save_path)
fig.savefig(fname=save_path + '.png', transparent=True, format='png')
fig.savefig(fname=save_path + '.svg', transparent=True, format='svg')


