import os

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

from _utils_._alloptical_utils import run_for_loop_across_exps
from _analysis_._ClassPhotostimAnalysisSlmTargets import PhotostimAnalysisSlmTargets
from _analysis_.sz_analysis._ClassExpSeizureAnalysis import ExpSeizureAnalysis
from _main_.AllOpticalMain import alloptical
from _main_.Post4apMain import Post4ap
from funcsforprajay import plotting as pplot

import xml.etree.ElementTree as ET


# expobj: Union[alloptical, Post4ap] = import_expobj(exp_prep='RL108 t-009')
SAVE_FIG = "/home/pshah/Documents/figures/alloptical-photostim-responses-traces/"

# %% B) individual Ca+ traces for pre4ap + post4ap - with corresponding LFP trace
main = PhotostimAnalysisSlmTargets

main.plot_photostim_traces_stacked_LFP_pre4ap_post4ap()

# %% F) Radial plot of Mean FOV for photostimulation trials, with period equal to that of photostimulation timing period

# run data analysis
exp_sz_occurrence = ExpSeizureAnalysis.collectSzOccurrenceRelativeStim()

# %%
for exp, values in exp_sz_occurrence.items():
    print(values.shape)


# make plot
bin_width = int(1 * expobj.fps) if expobj.fps == 15 else int(0.5 * expobj.fps)
# period = len(np.arange(0, (expobj.stim_interval_fr / bin_width)))
period = 10
theta = (2 * np.pi) * np.arange(0, (expobj.stim_interval_fr / bin_width)) / period

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, dpi=300)
for exp, values in exp_sz_occurrence.items():
    plot = values
    ax.bar(theta, plot, width=(2 * np.pi) / period, bottom=0.0, alpha=0.5)
ax.set_rmax(1.1)
# ax.set_rticks([1])  # Less radial ticks
ax.set_rlabel_position(-35.5)  # Move radial labels away from plotted line
ax.grid(True)
ax.set_xticks((2 * np.pi) * np.arange(0, (expobj.stim_interval_fr / bin_width)) / period)
ax.set_title("sz probability occurrence (binned every 1s)", va='bottom')
ax.spines['polar'].set_visible(False)
fig.show()




# %% C) baseline
# collect avg traces across all exps
@run_for_loop_across_exps(run_pre4ap_trials=True, run_post4ap_trials=False, allow_rerun=True)
def collect_avg_photostim_traces(**kwargs):
    expobj: alloptical = kwargs['expobj']

    pre_sec = expobj.PhotostimAnalysisSlmTargets.pre_stim_sec
    post_sec = expobj.PhotostimAnalysisSlmTargets.post_stim_sec
    pre_fr = expobj.PhotostimAnalysisSlmTargets.pre_stim_fr
    post_fr = expobj.PhotostimAnalysisSlmTargets.post_stim_fr

    stim_dur = 0.5  # for making adjusted traces below


    ## targets
    targets_traces = expobj.SLMTargets_stims_dff
    target_traces_adjusted = []
    for trace_snippets in targets_traces:
        trace = np.mean(trace_snippets, axis=0)
        pre_stim_trace = trace[:pre_fr]
        post_stim_trace = trace[-post_fr:]
        stim_trace = [0] * int(expobj.fps * stim_dur)  # frames

        new_trace = np.concatenate([pre_stim_trace, stim_trace, post_stim_trace])
        if expobj.fps > 20:
            new_trace = new_trace[::2][:67]

        target_traces_adjusted.append(new_trace)

    avg_photostim_trace_targets = np.mean(target_traces_adjusted, axis=0)


    ## fakestims
    targets_traces = expobj.fake_SLMTargets_tracedFF_stims_dff
    fakestims_target_traces_adjusted = []
    for trace_snippets in targets_traces:
        trace = np.mean(trace_snippets, axis=0)
        pre_stim_trace = trace[:pre_fr]
        post_stim_trace = trace[-post_fr:]
        stim_trace = [0] * int(expobj.fps * stim_dur)  # frames

        new_trace = np.concatenate([pre_stim_trace, stim_trace, post_stim_trace])
        if expobj.fps > 20:
            new_trace = new_trace[::2][:67]

        fakestims_target_traces_adjusted.append(new_trace)

    avg_fakestim_trace_targets = np.mean(fakestims_target_traces_adjusted, axis=0)


    # make corresponding time array
    time_arr = np.linspace(-pre_sec, post_sec + stim_dur, len(avg_photostim_trace_targets))

    # # plotting
    # plt.plot(time_arr, avg_photostim_trace)
    # plt.show()

    print('length of traces; ', len(time_arr))

    return target_traces_adjusted, fakestims_target_traces_adjusted, time_arr

func_collector = collect_avg_photostim_traces()

targets_average_traces_baseline = []
fakestim_targets_average_traces = []
for results in func_collector:
    traces = results[0]
    for trace in traces:
        targets_average_traces_baseline.append(trace)
    traces = results[1]
    for trace in traces:
        fakestim_targets_average_traces.append(trace)

time_arr = func_collector[0][2]

# %% C) interictal
# collect avg traces across all exps
@run_for_loop_across_exps(run_pre4ap_trials=False, run_post4ap_trials=True, allow_rerun=True)
def collect_avg_photostim_traces_interictal(**kwargs):
    expobj: Post4ap = kwargs['expobj']

    pre_sec = expobj.PhotostimAnalysisSlmTargets.pre_stim_sec
    post_sec = expobj.PhotostimAnalysisSlmTargets.post_stim_sec
    pre_fr = expobj.PhotostimAnalysisSlmTargets.pre_stim_fr
    post_fr = expobj.PhotostimAnalysisSlmTargets.post_stim_fr

    stim_dur = 0.5  # for making adjusted traces below


    ## targets
    targets_traces = expobj.SLMTargets_stims_dff[:, expobj.stim_idx_outsz, :]
    target_traces_adjusted = []
    for trace_snippets in targets_traces:
        trace = np.mean(trace_snippets, axis=0)
        pre_stim_trace = trace[:pre_fr]
        post_stim_trace = trace[-post_fr:]
        stim_trace = [0] * int(expobj.fps * stim_dur)  # frames

        new_trace = np.concatenate([pre_stim_trace, stim_trace, post_stim_trace])
        if expobj.fps > 20:
            new_trace = new_trace[::2][:67]

        target_traces_adjusted.append(new_trace)

    avg_photostim_trace_targets = np.mean(target_traces_adjusted, axis=0)


    ## fakestims
    targets_traces = expobj.fake_SLMTargets_tracedFF_stims_dff
    fakestims_target_traces_adjusted = []
    for trace_snippets in targets_traces:
        trace = np.mean(trace_snippets, axis=0)
        pre_stim_trace = trace[:pre_fr]
        post_stim_trace = trace[-post_fr:]
        stim_trace = [0] * int(expobj.fps * stim_dur)  # frames

        new_trace = np.concatenate([pre_stim_trace, stim_trace, post_stim_trace])
        if expobj.fps > 20:
            new_trace = new_trace[::2][:67]

        fakestims_target_traces_adjusted.append(new_trace)

    avg_fakestim_trace_targets = np.mean(fakestims_target_traces_adjusted, axis=0)


    # make corresponding time array
    time_arr = np.linspace(-pre_sec, post_sec + stim_dur, len(avg_photostim_trace_targets))

    # # plotting
    # plt.plot(time_arr, avg_photostim_trace)
    # plt.show()

    print('length of traces; ', len(time_arr))

    return target_traces_adjusted, fakestims_target_traces_adjusted, time_arr

func_collector = collect_avg_photostim_traces_interictal()

targets_average_traces_interictal = []
fakestim_targets_average_traces = []
for results in func_collector:
    traces = results[0]
    for trace in traces:
        targets_average_traces_interictal.append(trace)
    traces = results[1]
    for trace in traces:
        fakestim_targets_average_traces.append(trace)

time_arr = func_collector[0][2]

# %% C) ictal stims
# collect avg traces across all exps
@run_for_loop_across_exps(run_pre4ap_trials=False, run_post4ap_trials=True, allow_rerun=True)
def collect_avg_photostim_traces_ictal(**kwargs):
    expobj: Post4ap = kwargs['expobj']

    pre_sec = expobj.PhotostimAnalysisSlmTargets.pre_stim_sec
    post_sec = expobj.PhotostimAnalysisSlmTargets.post_stim_sec
    pre_fr = expobj.PhotostimAnalysisSlmTargets.pre_stim_fr
    post_fr = expobj.PhotostimAnalysisSlmTargets.post_stim_fr

    stim_dur = 0.5  # for making adjusted traces below


    ## targets
    targets_traces = expobj.SLMTargets_stims_dff[:, expobj.stim_idx_insz, :]
    target_traces_adjusted = []
    for trace_snippets in targets_traces:
        trace = np.mean(trace_snippets, axis=0)
        pre_stim_trace = trace[:pre_fr]
        post_stim_trace = trace[-post_fr:]
        stim_trace = [0] * int(expobj.fps * stim_dur)  # frames

        new_trace = np.concatenate([pre_stim_trace, stim_trace, post_stim_trace])
        if expobj.fps > 20:
            new_trace = new_trace[::2][:67]

        target_traces_adjusted.append(new_trace)

    avg_photostim_trace_targets = np.mean(target_traces_adjusted, axis=0)


    ## fakestims
    targets_traces = expobj.fake_SLMTargets_tracedFF_stims_dff
    fakestims_target_traces_adjusted = []
    for trace_snippets in targets_traces:
        trace = np.mean(trace_snippets, axis=0)
        pre_stim_trace = trace[:pre_fr]
        post_stim_trace = trace[-post_fr:]
        stim_trace = [0] * int(expobj.fps * stim_dur)  # frames

        new_trace = np.concatenate([pre_stim_trace, stim_trace, post_stim_trace])
        if expobj.fps > 20:
            new_trace = new_trace[::2][:67]

        fakestims_target_traces_adjusted.append(new_trace)

    avg_fakestim_trace_targets = np.mean(fakestims_target_traces_adjusted, axis=0)


    # make corresponding time array
    time_arr = np.linspace(-pre_sec, post_sec + stim_dur, len(avg_photostim_trace_targets))

    # # plotting
    # plt.plot(time_arr, avg_photostim_trace)
    # plt.show()

    print('length of traces; ', len(time_arr))

    return target_traces_adjusted, fakestims_target_traces_adjusted, time_arr

func_collector = collect_avg_photostim_traces_ictal()

targets_average_traces_ictal = []
fakestim_targets_average_traces = []
for results in func_collector:
    traces = results[0]
    for trace in traces:
        targets_average_traces_ictal.append(trace)
    traces = results[1]
    for trace in traces:
        fakestim_targets_average_traces.append(trace)

time_arr = func_collector[0][2]

# %% -- C -- ) baseline - make figure
fig, ax = plt.subplots(figsize=(3, 4), dpi=300)
# photostims - targets
avg_ = np.mean(targets_average_traces_baseline, axis=0)
sem_ = stats.sem(targets_average_traces_baseline, axis=0, ddof=1, nan_policy='omit')
ax.plot(time_arr, avg_, color='black', lw=1)
ax.fill_between(x=time_arr, y1=avg_ + sem_, y2=avg_ - sem_, alpha=0.5, zorder=2, color='lightgreen')

# # fakestims - targets
# avg_ = np.mean(fakestim_targets_average_traces, axis=0)
# std_ = np.std(fakestim_targets_average_traces, axis=0, ddof=1)
# ax.plot(time_arr, avg_, color='black', lw=1.5)
# ax.fill_between(x=time_arr, y1=avg_ + std_, y2=avg_ - std_, alpha=0.3, zorder=2, color='gray')

# span over stim frames
stim_ = np.where(sem_ == 0)[0]
ax.axvspan(time_arr[stim_[0]-1], time_arr[stim_[-1] + 2], color='hotpink', zorder = 5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(False)
ax.set_ylim([-1.5, 40])
ax.set_ylabel('dFF')
ax.set_xlabel('Time (secs) rel. to stim')
ax.set_title('grand average all cells, all exps - baseline', wrap=True, fontsize='small')
fig.tight_layout(pad=1)
fig.show()




# %% -- C -- ) interictal - make figure
fig, ax = plt.subplots(figsize=(3, 4), dpi=300)
# photostims - targets
avg_ = np.mean(targets_average_traces_interictal, axis=0)
sem_ = stats.sem(targets_average_traces_interictal, axis=0, ddof=1, nan_policy='omit')
ax.plot(time_arr, avg_, color='black', lw=1)
ax.fill_between(x=time_arr, y1=avg_ + sem_, y2=avg_ - sem_, alpha=0.5, zorder=2, color='lightgreen')

# # fakestims - targets
# avg_ = np.mean(fakestim_targets_average_traces, axis=0)
# std_ = np.std(fakestim_targets_average_traces, axis=0, ddof=1)
# ax.plot(time_arr, avg_, color='black', lw=1.5)
# ax.fill_between(x=time_arr, y1=avg_ + std_, y2=avg_ - std_, alpha=0.3, zorder=2, color='gray')

# span over stim frames
stim_ = np.where(sem_ == 0)[0]
ax.axvspan(time_arr[stim_[0]-1], time_arr[stim_[-1] + 2], color='hotpink', zorder = 5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(False)
ax.set_ylim([-1.5, 40])
ax.set_ylabel('dFF')
ax.set_xlabel('Time (secs) rel. to stim')
ax.set_title('grand average all cells, all exps - interictal stims', wrap=True, fontsize='small')
fig.tight_layout(pad=1)
fig.show()




# %% -- C --) ictal stims - make figure
fig, ax = plt.subplots(figsize=(3, 4), dpi=300)
# photostims - targets
avg_ = np.mean(targets_average_traces_ictal, axis=0)
sem_ = stats.sem(targets_average_traces_ictal, axis=0, ddof=1, nan_policy='omit')
ax.plot(time_arr, avg_, color='black', lw=1)
ax.fill_between(x=time_arr, y1=avg_ + sem_, y2=avg_ - sem_, alpha=0.5, zorder=2, color='lightgreen')

# # fakestims - targets
# avg_ = np.mean(fakestim_targets_average_traces, axis=0)
# std_ = np.std(fakestim_targets_average_traces, axis=0, ddof=1)
# ax.plot(time_arr, avg_, color='black', lw=1.5)
# ax.fill_between(x=time_arr, y1=avg_ + std_, y2=avg_ - std_, alpha=0.3, zorder=2, color='gray')

# span over stim frames
stim_ = np.where(sem_ == 0)[0]
ax.axvspan(time_arr[stim_[0]-1], time_arr[stim_[-1] + 2], color='hotpink', zorder = 5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(False)
ax.set_ylim([-1.5, 40])
ax.set_ylabel('dFF')
ax.set_xlabel('Time (secs) rel. to stim')
ax.set_title('grand average all cells, all exps - ictal stims', wrap=True, fontsize='small')
fig.tight_layout(pad=1)
fig.show()


# %% C) all conditions - grand average photostim average of targets - make figure
fig, ax = plt.subplots(figsize=(3, 4), dpi=300)

# photostims - targets
avg_ = np.mean(targets_average_traces_baseline, axis=0)
sem_ = stats.sem(targets_average_traces_baseline, axis=0, ddof=1, nan_policy='omit')
ax.plot(time_arr, avg_, color='royalblue', lw=1)
ax.fill_between(x=time_arr, y1=avg_ + sem_, y2=avg_ - sem_, alpha=0.3, zorder=2, color='royalblue')

avg_ = np.mean(targets_average_traces_interictal, axis=0)
sem_ = stats.sem(targets_average_traces_interictal, axis=0, ddof=1, nan_policy='omit')
ax.plot(time_arr, avg_, color='mediumseagreen', lw=1)
ax.fill_between(x=time_arr, y1=avg_ + sem_, y2=avg_ - sem_, alpha=0.3, zorder=2, color='forestgreen')

avg_ = np.mean(targets_average_traces_ictal, axis=0)
sem_ = stats.sem(targets_average_traces_ictal, axis=0, ddof=1, nan_policy='omit')
ax.plot(time_arr, avg_, color='blueviolet', lw=1)
ax.fill_between(x=time_arr, y1=avg_ + sem_, y2=avg_ - sem_, alpha=0.3, zorder=2, color='purple')

# # fakestims - targets
# avg_ = np.mean(fakestim_targets_average_traces, axis=0)
# std_ = np.std(fakestim_targets_average_traces, axis=0, ddof=1)
# ax.plot(time_arr, avg_, color='black', lw=1.5)
# ax.fill_between(x=time_arr, y1=avg_ + std_, y2=avg_ - std_, alpha=0.3, zorder=2, color='gray')

# span over stim frames
stim_ = np.where(sem_ == 0)[0]
ax.axvspan(time_arr[stim_[0]-1], time_arr[stim_[-1] + 2], color='lightcoral', zorder = 5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(False)
ax.set_ylim([-1.5, 30])
ax.set_ylabel('dFF')
ax.set_xlabel('Time (secs) rel. to stim')
ax.set_title('grand average all cells, all exps - baseline', wrap=True, fontsize='small')
fig.tight_layout(pad=1)
fig.show()
# fig.savefig('alloptical_targets_grand_avg_photostim_responses_allconditions.svg')
save_path_full = f'{SAVE_FIG}/alloptical_targets_grand_avg_photostim_responses_allconditions.svg'
os.makedirs(os.path.dirname(save_path_full), exist_ok=True)
fig.savefig(save_path_full)


# %% B) alloptical traces




# %% E) BAR PLOT OF AVG PHOTOSTIMULATION FOV RAW FLU ACROSS CONDITIONS

# 1.1) plot the first sz frame for each seizure from each expprep, label with the time delay to sz invasion
@run_for_loop_across_exps(run_pre4ap_trials=True, run_post4ap_trials=False, allow_rerun=1)
def collect_avg_prestimf_baseline(**kwargs):
    expobj: alloptical = kwargs['expobj']
    fov_flu = np.mean(expobj.PhotostimResponsesSLMTargets.adata.var['pre_stim_FOV_Flu'])
    return fov_flu

@run_for_loop_across_exps(run_pre4ap_trials=False, run_post4ap_trials=True, allow_rerun=1)
def collect_avg_prestimf_interictal(**kwargs):
    expobj: Post4ap = kwargs['expobj']
    fov_flu = np.mean(expobj.PhotostimResponsesSLMTargets.adata.var['pre_stim_FOV_Flu'][expobj.stim_idx_outsz])
    return fov_flu

@run_for_loop_across_exps(run_pre4ap_trials=False, run_post4ap_trials=True, allow_rerun=1)
def collect_avg_prestimf_ictal(**kwargs):
    expobj: Post4ap = kwargs['expobj']
    fov_flu = np.mean(expobj.PhotostimResponsesSLMTargets.adata.var['pre_stim_FOV_Flu'][expobj.stim_idx_insz])
    return fov_flu

baseline_prestimf = collect_avg_prestimf_baseline()
interictal_prestimf = collect_avg_prestimf_interictal()
ictal_prestimf = collect_avg_prestimf_ictal()


# %% E) pre stim F across conditions

pplot.plot_bar_with_points(data=[baseline_prestimf, interictal_prestimf, ictal_prestimf],
                           bar = False, title='avg prestim F - targets',
                           x_tick_labels=['Baseline', 'Interictal', 'Ictal'],
                           colors=['royalblue', 'mediumseagreen', 'blueviolet'], figsize=(4, 4),
                           y_label='Fluorescence (a.u.)',
                           ylims=[0, 2000], alpha=1)



# %% D) BAR PLOT OF AVG PHOTOSTIMULATION RESPONSE OF TARGETS ACROSS CONDITIONS

@run_for_loop_across_exps(run_pre4ap_trials=True, run_post4ap_trials=False, allow_rerun=1)
def collect_avg_photostim_response_baseline(**kwargs):
    expobj: alloptical = kwargs['expobj']

    avg_response = np.mean(expobj.PhotostimResponsesSLMTargets.adata.X, axis=1)
    return np.mean(avg_response)

@run_for_loop_across_exps(run_pre4ap_trials=False, run_post4ap_trials=True, allow_rerun=1)
def collect_avg_photostim_response_interictal(**kwargs):
    expobj: Post4ap = kwargs['expobj']

    interictal_avg_response = np.mean(expobj.PhotostimResponsesSLMTargets.adata.X[:, expobj.stim_idx_outsz], axis=1)
    return np.mean(interictal_avg_response)

@run_for_loop_across_exps(run_pre4ap_trials=False, run_post4ap_trials=True, allow_rerun=1)
def collect_avg_photostim_response_ictal(**kwargs):
    expobj: Post4ap = kwargs['expobj']

    ictal_avg_response = np.mean(expobj.PhotostimResponsesSLMTargets.adata.X[:, expobj.stim_idx_insz], axis=1)
    return np.mean(ictal_avg_response)

baseline_responses = collect_avg_photostim_response_baseline()
interictal_responses = collect_avg_photostim_response_interictal()
ictal_responses = collect_avg_photostim_response_ictal()

save_path_full = f'{SAVE_FIG}/alloptical_avg_photoresponses_allexps.svg'
os.makedirs(os.path.dirname(save_path_full), exist_ok=True)

pplot.plot_bar_with_points(data=[baseline_responses, interictal_responses, ictal_responses],
                           bar = False, title='avg photostim responses - targets',
                           x_tick_labels=['Baseline', 'Interictal', 'Ictal'],
                           colors=['royalblue', 'mediumseagreen', 'blueviolet'], figsize=(4,4), y_label='dFF',
                           s=35, alpha=1, ylims=[-19, 90], savepath=save_path_full)

# fig.savefig(save_path_full)


# %% A) getting num pixels for scale bar

# using RL108 for example gcamp c1v1 image

def _getPVStateShard(path, key):
    '''
    Used in function PV metadata below
    '''

    value = []
    description = []
    index = []

    xml_tree = ET.parse(path)  # parse xml from a path
    root = xml_tree.getroot()  # make xml tree structure

    pv_state_shard = root.find('PVStateShard')  # find pv state shard element in root

    for elem in pv_state_shard:  # for each element in pv state shard, find the value for the specified key

        if elem.get('key') == key:

            if len(elem) == 0:  # if the element has only one subelement
                value = elem.get('value')
                break

            else:  # if the element has many subelements (i.e. lots of entries for that key)
                for subelem in elem:
                    value.append(subelem.get('value'))
                    description.append(subelem.get('description'))
                    index.append(subelem.get('index'))
        else:
            for subelem in elem:  # if key not in element, try subelements
                if subelem.get('key') == key:
                    value = elem.get('value')
                    break

        if value:  # if found key in subelement, break the loop
            break

    if not value:  # if no value found at all, raise exception
        raise Exception('ERROR: no element or subelement with that key')

    return value, description, index

pixelSize, _, index = _getPVStateShard('/home/pshah/mnt/qnap/Data/2021-01-11/2021-01-11_s-003/2021-01-11_s-003.xml', 'micronsPerPixel')
for pixelSize, index in zip(pixelSize, index):
    if index == 'XAxis':
        pix_sz_x = float(pixelSize)

print(f'100um in pixels: {int(100 / pix_sz_x)}')







