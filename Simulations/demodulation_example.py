import numpy as np
import matplotlib.pyplot as plt

# Makeup a signal with a fast and slow component
time = np.linspace(0,10,10000)
s_fast = np.exp(1j*time*25*np.pi)
s_slow = np.exp(1j*time*1*np.pi)*np.exp(-(time-3)/0.5)
s_total = s_fast*s_slow

def plot_signal(signal):
    if np.any(np.iscomplex(signal)):
        plt.plot(time, np.real(signal))
        plt.plot(time, np.imag(signal))
        plt.plot(time, np.abs(signal),'k')
        plt.legend(('Real', 'Imag', 'Mag'))
    else:
        plt.plot(time, signal,'k')

    plt.xlim(3,4)
    plt.ylim(-1.1,1.1)


# Plot the fast B0 modulation
plt.figure()
plot_signal(s_fast)
plt.title('B_0 Modulation')
plt.xlabel("Time")
plt.ylabel("Signal")
plt.show()

# Plot the slow modulation
plt.figure()
plot_signal(s_slow)
plt.title('Rotating Frame Signal')
plt.xlabel("Time")
plt.ylabel("Signal")
plt.show()

plt.figure()
plot_signal(s_total)
plt.title('Lab Frame Signal')
plt.xlabel("Time")
plt.ylabel("Signal")
plt.show()

plt.figure()
plot_signal(np.real(s_total))
plt.xlabel("Time")
plt.ylabel("Voltage")
plt.show()



plt.figure()
s_mod = np.real(s_total)*s_fast
plot_signal(s_mod)
plt.xlabel("Time")
plt.ylabel("Signal")
plt.show()

plt.figure()
s_mod = np.real(s_total)*np.conj(s_fast)
x = np.linspace(-1,1,201)
filter = np.exp( -x**2/0.25)
filter = 2*filter / np.sum(filter)
s_mod = np.convolve(s_mod,filter,'same')
plot_signal(s_mod)
plt.xlabel("Time")
plt.ylabel("Signal")
plt.show()

