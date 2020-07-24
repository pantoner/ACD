import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# def format_axes(fig):
#     for i, ax in enumerate(fig.axes):
#         ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
#         ax.tick_params(labelbottom=False, labelleft=False)

# fig = plt.figure(constrained_layout=True)

# gs = GridSpec(3, 3, figure=fig)
# ax1 = fig.add_subplot(gs[0, :])
# # identical to ax1 = plt.subplot(gs.new_subplotspec((0, 0), colspan=3))
# #ax2 = fig.add_subplot(gs[1, :-1])
# ax2 = fig.add_subplot(gs[1, :])
# #ax3 = fig.add_subplot(gs[1:, -1])
# ax3 = fig.add_subplot(gs[2, :])

# ax4 = fig.add_subplot(gs[-1, 0])
# ax5 = fig.add_subplot(gs[-1, -2])

# fig.suptitle("GridSpec")
# format_axes(fig)

# plt.show()

import matplotlib.pyplot as plt
from matplotlib import gridspec

def addalertline(failure,top,now):

	fig2 = plt.figure(constrained_layout=True)
	spec2 = gridspec.GridSpec(ncols=1, nrows=5, figure=fig2)
	f2_ax1 = fig2.add_subplot(spec2[0, 0])
	f2_ax2 = fig2.add_subplot(spec2[1, 0])
	f2_ax3 = fig2.add_subplot(spec2[2, 0])
	f2_ax4 = fig2.add_subplot(spec2[3, 0])
	f2_ax5 = fig2.add_subplot(spec2[4, 0])


	f2_ax1.get_xaxis().set_ticks([])
	f2_ax1.get_yaxis().set_ticks([])
	f2_ax2.get_xaxis().set_ticks([])
	f2_ax2.get_yaxis().set_ticks([])
	f2_ax3.get_xaxis().set_ticks([])
	f2_ax3.get_yaxis().set_ticks([])
	f2_ax4.get_xaxis().set_ticks([])
	f2_ax4.get_yaxis().set_ticks([])
	f2_ax5.get_xaxis().set_ticks([])
	f2_ax5.get_yaxis().set_ticks([])

	if failure == 1:
		f2_ax1.axhline(y=0.25, color='r', linestyle='-')
		f2_ax1.axhline(y=0.5, color='r', linestyle='-')
		f2_ax1.axhline(y=1, color='r', linestyle='-')
		f2_ax1.axhline(y=0.75, color='r', linestyle='-')

	if failure == 5:
		f2_ax5.axhline(y=0.25, color='r', linestyle='-')
		f2_ax5.axhline(y=0.5, color='r', linestyle='-')
		f2_ax5.axhline(y=1, color='r', linestyle='-')
		f2_ax5.axhline(y=0.75, color='r', linestyle='-')

	if failure == 6:
		f2_ax5.axhline(y=0.25, color='r', linestyle='-')
		f2_ax5.axhline(y=0.5, color='r', linestyle='-')
		f2_ax5.axhline(y=1, color='r', linestyle='-')
		f2_ax5.axhline(y=0.75, color='r', linestyle='-')

		f2_ax1.axhline(y=0.25, color='r', linestyle='-')
		f2_ax1.axhline(y=0.5, color='r', linestyle='-')
		f2_ax1.axhline(y=1, color='r', linestyle='-')
		f2_ax1.axhline(y=0.75, color='r', linestyle='-')

	if top == 'cup':
		f2_ax1.set_facecolor('lightblue')
	if top == 'cdwn':
		f2_ax5.set_facecolor('lightblue')
	if top == 'aup':
		f2_ax1.set_facecolor('lightgreen')
	if top == 'adwn':
		f2_ax5.set_facecolor('lightgreen')
	if top == 'cupadwn':
		f2_ax1.set_facecolor('lightblue')
		f2_ax5.set_facecolor('lightgreen')
	if top == 'cdwnaup':
		f2_ax5.set_facecolor('lightblue')
		f2_ax1.set_facecolor('lightgreen')

	if now == 1:
		f2_ax1.set_facecolor('green')
	if now == 2:
		f2_ax2.set_facecolor('green')
	if now == 3:
		f2_ax3.set_facecolor('green')
	if now == 4:
		f2_ax5.set_facecolor('green')
	if now == 5:
		f2_ax5.set_facecolor('green')
	if now == 6:
		f2_ax1.set_facecolor('blue')
	if now == 7:
		f2_ax5.set_facecolor('blue')
	plt.show()


# failure = 0
# top = 'cdwnaup'
# now = 7

# addalertline(failure,top,now)