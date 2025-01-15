#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: music_transmit
# Author: jwhit
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import sip



class music_transmit(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "music_transmit", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("music_transmit")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "music_transmit")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 0.5
        self.samp_rate = samp_rate = 10e6
        self.noise = noise = 0
        self.music_rate = music_rate = 48000
        self.gain = gain = 1
        self.channel_width = channel_width = 200e3
        self.channel_freq = channel_freq = 0
        self.center_freq = center_freq = 108.9e6
        self.audio_rate = audio_rate = 1411

        ##################################################
        # Blocks
        ##################################################

        self._volume_range = qtgui.Range(0, 1, 0.01, 0.5, 200)
        self._volume_win = qtgui.RangeWidget(self._volume_range, self.set_volume, "Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._volume_win)
        self._music_rate_range = qtgui.Range(16e3, 128e4, 4e3, 48000, 200)
        self._music_rate_win = qtgui.RangeWidget(self._music_rate_range, self.set_music_rate, "'music_rate'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._music_rate_win)
        self._gain_range = qtgui.Range(1, 10, 1, 1, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self._center_freq_range = qtgui.Range(1, 2e9, 1e7, 108.9e6, 200)
        self._center_freq_win = qtgui.RangeWidget(self._center_freq_range, self.set_center_freq, "'center_freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._center_freq_win)
        self.rational_resampler_xxx_0_0_2 = filter.rational_resampler_fff(
                interpolation=160,
                decimation=147,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0_1_0 = filter.rational_resampler_ccc(
                interpolation=10000000,
                decimation=192000,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=5,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            48000, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0_0_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            channel_freq, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_1_win)
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(center_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(gain, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
        self._noise_range = qtgui.Range(0, 1, 0.01, 0, 200)
        self._noise_win = qtgui.RangeWidget(self._noise_range, self.set_noise, "noise", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_win)
        self.low_pass_filter_0_1 = filter.fir_filter_ccf(
            (int(samp_rate/channel_width)),
            firdes.low_pass(
                1,
                samp_rate,
                100e3,
                25e3,
                window.WIN_HAMMING,
                6.76))
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\jwhit\\OneDrive\\Documents\\FYP\\GRC\\Bad Apple Music.wav', True)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_ff(volume)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(0.7071)
        self.audio_sink_0_1 = audio.sink(48000, '', True)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=music_rate,
        	quad_rate=(music_rate*4),
        	tau=(75e-6),
        	max_dev=75e3,
        	fh=(-1.0),
        )
        self.analog_wfm_rcv_0_0 = analog.wfm_rcv(
        	quad_rate=480e3,
        	audio_decimation=10,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0_0_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.audio_sink_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_freq_sink_x_0_0_1, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.rational_resampler_xxx_0_0_2, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_wfm_rcv_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_1_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_1_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_2, 0), (self.blocks_multiply_const_vxx_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "music_transmit")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0_1.set_k(self.volume)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 25e3, window.WIN_HAMMING, 6.76))
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0_0_1.set_frequency_range(self.channel_freq, self.samp_rate)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise

    def get_music_rate(self):
        return self.music_rate

    def set_music_rate(self, music_rate):
        self.music_rate = music_rate

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_sink_0.set_gain(self.gain, 0)

    def get_channel_width(self):
        return self.channel_width

    def set_channel_width(self, channel_width):
        self.channel_width = channel_width

    def get_channel_freq(self):
        return self.channel_freq

    def set_channel_freq(self, channel_freq):
        self.channel_freq = channel_freq
        self.qtgui_freq_sink_x_0_0_1.set_frequency_range(self.channel_freq, self.samp_rate)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_sink_0.set_center_freq(self.center_freq, 0)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate




def main(top_block_cls=music_transmit, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
