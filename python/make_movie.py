import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from map import Map
import matplotlib.cm as cm

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Particle Filter', artist='Matt Barnes')
writer = FFMpegWriter(fps=15, metadata=metadata)

map_object = Map('../data/map/wean.dat')
fig = plt.figure()
plt.imshow(map_object._occupancy_grid, cmap=cm.Greys_r)
p, = plt.plot([], [], 'r.')
plt.axis([0, map_object._occupancy_grid.shape[0], 0, map_object._occupancy_grid.shape[1]])

data_path = '../data/results/robotdata1.log'
data = open('../data/results/robotdata1.log', 'r')
data.next()  # skip header line
with writer.saving(fig, "writer_test.mp4", 100):  #num_lines):
    for counter, line in enumerate(data):
        print 'Processing frame', counter
        x = list()
        y = list()
        xy = line.split(';')
        for loc in xy:
            _x, _y = loc.split(',')
            x.append(float(_y))
            y.append(float(_x))
        p.set_data(x, y)
        writer.grab_frame()