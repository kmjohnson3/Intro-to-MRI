import numpy as np
import subprocess
import matplotlib.pyplot as plt
import math
#subprocess.call('git clone https://github.com/mikgroup/sigpy.git')
#subprocess.call('pip install sigpy')
import sigpy as sp
import sigpy.mri
import matplotlib.animation as manimation

Tpe = 0.1*1e-3 # Time for blipped PE
Tread = 30.0*1e-3 # Readout time in ms
Npe = 128
Nfreq = 128
t_offset = 0.0

t = []
kx = []
ky = []

t = np.linspace(0, Tread,Nfreq*Nfreq)
tt = np.sqrt(t/Tread)
kx = Nfreq/2*tt*np.cos( 2*math.pi*Nfreq/2*tt)
ky = Nfreq/2*tt*np.sin( 2*math.pi*Nfreq/2*tt)

#kx,ky = -ky,kx
ky = -ky

# Create gradients as triangles
plt.figure()
plt.plot(kx,ky)
plt.show()

# Create gradients as triangles
plt.figure()
plt.plot(t,kx)
plt.plot(t,ky)

sl_amps = [1.0,-1.0]
sl_scales = [[.6900, .920, .810],  # white big
             [.6624, .874, .780]]  # gray big
sl_offsets = [[0., 0., 0],
              [0., -.0184, 0]]
sl_angles = [[0, 0, 0],
             [0, 0, 0]]
fat = sp.sim.phantom([256,256], sl_amps, sl_scales, sl_offsets, sl_angles,dtype=np.complex64)


plt.figure()
plt.imshow(np.abs(fat))


sl_amps = [0.2, 1., 1.2, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1]

sl_scales = [[.6624, .874, .780],  # gray big
             [.1100, .310, .220],  # right black
             [.1600, .410, .280],  # left black
             [.2100, .250, .410],  # gray center blob
             [.0460, .046, .050],
             [.0460, .046, .050],
             [.0460, .046, .050],  # left small dot
             [.0230, .023, .020],  # mid small dot
             [.0230, .023, .020]]

sl_offsets = [[0., -.0184, 0],
              [.22, 0., 0],
              [-.22, 0., 0],
              [0., .35, -.15],
              [0., .1, .25],
              [0., -.1, .25],
              [-.08, -.605, 0],
              [0., -.606, 0],
              [.06, -.605, 0]]

sl_angles = [[0, 0, 0],
             [-18, 0, 10],
             [18, 0, 10],
             [0, 0, 0],
             [0, 0, 0],
             [0, 0, 0],
             [0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]


# Get complex phantom
water = sp.sim.phantom([256,256], sl_amps, sl_scales, sl_offsets, sl_angles,dtype=np.complex64)
[x,y] = np.meshgrid(np.linspace(-0.5,0.5,256),np.linspace(-0.5,0.5,256))
x0 = 0.0
y0 = 0.4
wY = 0.3
wX = 0.2
offmap = np.exp( -((x-x0)**2/(wX**2) + (y-y0)**2/(wY**2))**2)

# Subtract off mean
offmap -= np.mean(offmap)
offmap /= np.max(offmap)

offmap = np.flipud(offmap)
water = np.flipud(water)
fat = np.flipud(fat)


# Create gradients as triangles
plt.figure()
plt.imshow(offmap)
plt.draw()
plt.colorbar()


FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='spiral_without_fat', artist='KMJ',
                comment='EPI simulation with off-resonance')
writer = FFMpegWriter(fps=10, metadata=metadata)

# Do this on GPU
device = sp.backend.Device(0)
xp = device.xp
kx = sp.backend.to_device(kx,device)
ky = sp.backend.to_device(ky,device)
t = sp.backend.to_device(t,device)
water = sp.backend.to_device(water,device)
fat = sp.backend.to_device(fat,device)

offmap = sp.backend.to_device(offmap,device)

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(20, 10))

with writer.saving(fig, "spiral_without_fat.mp4", 100):
    for fmax in xp.linspace(-200.0,200.0,41):

        print(fmax)
        with device:

            s = xp.zeros(kx.shape, xp.complex64)
            img_est = xp.zeros(water.shape, xp.complex64)

            # Now do the DFT
            [x,y] = xp.meshgrid(xp.linspace(-0.5,0.5,256),xp.linspace(-0.5,0.5,256))
            for pos in range(kx.shape[0]):
                Gphase = xp.exp(1j*2.0*math.pi*(kx[pos]*x + ky[pos]*y))
                Ophase = xp.exp(1j*2.0*math.pi*t[pos]*offmap*fmax)
                s[pos] = xp.sum((water+0.0*fat*xp.exp(2j*math.pi*t[pos]*440))*Gphase*Ophase)

                fr = 0.9*Nfreq/2.0
                fw = 0.1*Nfreq/2.0

                kr = xp.abs(kx[pos])
                wx = 1. / (1. + xp.exp( (kr-fr)/fw))
                kr = xp.abs(ky[pos])
                wy = 1. / (1. + xp.exp( (kr-fr)/fw))

                img_est += s[pos]*xp.conj(Gphase)*wx*wy


        #s = sp.backend.to_device(s,sp.cpu_device)
        #s = np.reshape(s,[Npe,Nfreq+2])

        # Get Images
        img_est_cpu = sp.backend.to_device(img_est,sp.cpu_device)
        offmap_cpu = sp.backend.to_device(offmap,sp.cpu_device)
        fmax_cpu = sp.backend.to_device(fmax,sp.cpu_device)

        from mpl_toolkits.axes_grid1 import make_axes_locatable
        def colorbar(mappable):
            ax = mappable.axes
            fig = ax.figure
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            return fig.colorbar(mappable, cax=cax)

        img1 = ax1.imshow(fmax_cpu*offmap_cpu,cmap='Spectral')
        img1.set_clim(-150,150)
        colorbar(img1)
        ax1.set_title('Off Resonance [Hz]')
        ax1.axis('off')


        img2 = ax2.imshow(np.abs(img_est_cpu),cmap='gray')
        ax2.set_title('Estimated Image')
        ax2.axis('off')

        plt.tight_layout(h_pad=1)
        plt.draw()
        plt.pause(0.0001)
        writer.grab_frame()


plt.show()





