### various bits of code that is useful for data inspection

import sys

from _exp_metainfo_.data_paths import results_object_path
from _utils_._alloptical_utils import run_for_loop_across_exps
from _exp_metainfo_.exp_metainfo import import_resultsobj
from _utils_.io import import_expobj

sys.path.append('/home/pshah/Documents/code/PackerLab_pycharm/')
sys.path.append('/home/pshah/Documents/code/')
from _utils_ import alloptical_plotting as aoplot
from _main_.AllOpticalMain import alloptical

import numpy as np
import matplotlib.pyplot as plt

# # import results superobject that will collect analyses from various individual experiments
allopticalResults = import_resultsobj(pkl_path=results_object_path)


# %% list all dates of all experiments
dates = []
@run_for_loop_across_exps(run_pre4ap_trials=True, run_post4ap_trials=True, set_cache=False, supress_print=True, allow_rerun=True)
def list_all_dates(**kwargs):
    expobj = kwargs['expobj']
    dates.append(expobj.date) if expobj.date not in dates else None

list_all_dates()
print(dates)

# %% IMPORT expobj
# expobj, experiment = aoutils.import_expobj(aoresults_map_id='pre h.0')
expobj: alloptical = import_expobj(prep='PS06', trial='t-011')
fig, axs = plt.subplots(2, 1, figsize=(20, 6))
fig, ax = aoplot.plotMeanRawFluTrace(expobj=expobj, stim_span_color=None, x_axis='frames', fig=fig, ax=axs[0], show=False)
fig, ax = aoplot.plotLfpSignal(expobj=expobj, stim_span_color='', x_axis='time', fig=fig, ax=axs[1], show=False)
fig.show()



# %% useful general plots

# aoplot.plotMeanRawFluTrace(expobj=expobj, stim_span_color=None, x_axis='Time', figsize=(20,3))

fig, axs = plt.subplots(2, 1, figsize=(20, 6))
fig, ax = aoplot.plotMeanRawFluTrace(expobj=expobj, stim_span_color=None, x_axis='frames', fig=fig, ax=axs[0], show=False)
fig, ax = aoplot.plotLfpSignal(expobj=expobj, stim_span_color='', x_axis='time', fig=fig, ax=axs[1], show=False)
fig.show()

aoplot.plot_lfp_stims(expobj=expobj, x_axis='Time')


aoplot.plot_SLMtargets_Locs(expobj=expobj, background=expobj.meanFluImg_registered)

expobj.plot_single_frame_tiff(frame_num=2500)
expobj.plot_single_frame_tiff(frame_num=3000)
expobj.plot_single_frame_tiff(frame_num=501)
expobj.plot_single_frame_tiff(frame_num=301)
expobj.plot_single_frame_tiff(frame_num=200)

# %% s2p ROI Flu trace statistics for each cell

print('s2p neu. corrected cell traces statistics: ')
for cell in expobj.s2p_nontargets:
    cell_idx = expobj.cell_id.index(cell)
    print('mean: %s   \t min: %s  \t max: %s  \t std: %s' %
          (np.round(np.mean(expobj.raw[cell_idx]), 2), np.round(np.min(expobj.raw[cell_idx]), 2), np.round(np.max(expobj.raw[cell_idx]), 2),
           np.round(np.std(expobj.raw[cell_idx], ddof=1), 2)))


# %% downsampling of imaging tiff


