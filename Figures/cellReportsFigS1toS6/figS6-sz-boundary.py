"""
Figure showing approach for seizure boundary classification at each stim for targeted neurons.


"""



# %%
import sys

from _analysis_._ClassPhotostimResponseQuantificationSLMtargets import PhotostimResponsesSLMtargetsResults, \
    PhotostimResponsesQuantificationSLMtargets
from _exp_metainfo_.exp_metainfo import ExpMetainfo

sys.path.extend(['/home/pshah/Documents/code/reproducible_figures-main'])
from _utils_.alloptical_plotting import save_figure

import reproducible_figures as rfv


SAVE_FOLDER = f'/home/pshah/Documents/figures/alloptical_seizures_draft/4fig/'
fig_items = f'/home/pshah/Documents/figures/alloptical_seizures_draft/figure-items/4fig'
title = "figS6_2p-sz-boundary-RF"
save_path_full=f"{SAVE_FOLDER}/{title}"

save_fig = True

RESULTS = PhotostimResponsesSLMtargetsResults.load()

# %% MAKE FIGURE LAYOUT
fs = ExpMetainfo.figures.fontsize['extraplot']
rfv.set_fontsize(fs)

stim_color = ExpMetainfo.figure_settings['colors']["stim span"]

layout = {
    'A': {'panel_shape': (1, 1),
          'bound': (0.15, 0.80, 0.80, 0.93)},
    'B': {'panel_shape': (4, 1),
          'bound': (0.15, 0.55, 0.85, 0.70),
          'wspace': 0.2},
}

test = 0
save_fig = True if not test else False
dpi = 100 if test else 300

fig, axes, grid = rfv.make_fig_layout(layout=layout, dpi=dpi)

rfv.naked(axes['A'][0])

# rfv.show_test_figure_layout(fig, axes=axes, show=True)  # test what layout looks like quickly, but can also skip and moveon to plotting data.
print('\n\n')

# %% B) target annulus flu vs. photostim responses across baseline, interictal, ictal (split in/out of seizure)


PhotostimResponsesQuantificationSLMtargets.plot__photostim_responses_vs_prestim_targets_annulus_flu(RESULTS, fig=fig, ax=axes['B'], show=False)

# PhotostimResponsesQuantificationSLMtargets.plot__targets_annulus_prestim_Flu_all_points(RESULTS)

# %% add panel labels
rfv.add_label_axes(text='A', ax=axes['A'][0], x_adjust=0.13)
rfv.add_label_axes(text='B', ax=axes['B'][0], y_adjust=0, x_adjust=0.13)


# %%
if save_fig and dpi > 250:
    save_figure(fig=fig, save_path_full=f"{save_path_full}.png")
    save_figure(fig=fig, save_path_full=f"{save_path_full}.pdf")

# fig.show()



