from flask import Flask, render_template, send_file, request, session
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == 'POST':
        frequency = request.form['frequency']
        t2star = request.form['t2star']
        print(f'Post Frequency: {frequency}, T2*: {t2star}')
    else:
        frequency = 1
        t2star = 1

    return render_template('index.html', INPUT_T2=f'T2* {t2star}')

@app.route('/plot.png/<string:frequency>/<string:t2star>')
def plot_png(frequency, t2star):
    fig = create_figure(frequency, t2star)
    output = io.BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)
    return send_file(output, mimetype='image/png')

def create_figure(frequency, t2star):

    frequency = float(frequency)
    t2star = float(t2star)

    t = np.linspace(0, 30e-3, 1000)
    print(f'Frequency: {frequency}, T2*: {t2star}')
    mx = np.sin(2.0*np.pi*frequency * t) * np.exp(-t/t2star)
    my = np.cos(2.0*np.pi*frequency * t) * np.exp(-t/t2star)

    fig, ax = plt.subplots()
    ax.plot(t, mx, t, my)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Signal')
    ax.set_ylim(-1, 1)
    ax.set_xlim(0, 30e-3)
    ax.grid

    return fig

@socketio.on('update_frequency')
def update_frequency(data):
    frequency = data['frequency']
    t2star = data['t2star']
    print(f'Frequency: {frequency}, T2*: {t2star}')

    frequency_name = f'Frequency: {float(frequency):.3f} Hz'
    t2star_name = f'T2*: {float(t2star):.3f} s'

    socketio.emit('plot_url', {'url': f'/plot.png/{frequency}/{t2star}'})
    socketio.emit('set_names', {'frequency_name': frequency_name, 't2star_name': t2star_name})

if __name__ == '__main__':
    socketio.run(app, debug=True)
