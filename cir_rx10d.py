#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Spread Spectrum Rx
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time


class cir_rx10d(gr.top_block):

    def __init__(self, alpha=0.5, center_freq=3560e6, gain=20, index=0, samp_rate=24e6):
        gr.top_block.__init__(self, "Spread Spectrum Rx")

        ##################################################
        # Parameters
        ##################################################
        self.alpha = alpha
        self.center_freq = center_freq
        self.gain = gain
        self.index = index
        self.samp_rate = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                samp_rate,
                alpha,
                64))
        self.fir_filter_xxx_0_0 = filter.fir_filter_ccc(1, [1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,-1,-1,1,-1,-1,1,-1,-1,1,1,-1,1,-1,-1,1,1,-1,1,-1,1,1,1,1,1,-1,-1,1,1,-1,-1,-1,1,1,1,1,1,-1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,1,1,-1,-1,-1,-1,1,1,1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,1,1,1,-1,-1,-1,1,-1,-1,1,1,1,-1,1,1,-1,-1,1,-1,1,-1,1,1,1,-1,1,1,1,1,-1,1,-1,1,-1,-1,-1,1,1,1,1,-1,1,-1,-1,1,-1,1,-1,1,-1,-1,-1,-1,-1,1,-1,1,1,1,1,1,1,1,1,-1,1,-1,1,-1,1,-1,1,-1,1,1,1,1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,1,-1,-1,-1,1,1,-1,-1,1,-1,1,1,-1,1,-1,1,1,-1,-1,1,1,1,1,-1,1,-1,1,1,-1,-1,-1,1,1,-1,-1,1,1,1,1,1,1,-1,-1,1,-1,1,-1,1,-1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,-1,1,-1,-1,1,1,1,1,1,-1,1,-1,-1,1,1,1,-1,-1,-1,-1,1,-1,-1,-1,1,1,-1,1,1,-1,-1,1,-1,-1,-1,1,-1,1,-1,-1,1,1,-1,1,1,1,1,-1,1,1,1,-1,1,-1,1,-1,1,1,1,-1,-1,1,1,-1,-1,1,1,1,-1,1,1,1,-1,1,1,1,-1,-1,1,1,1,-1,1,-1,1,-1,-1,1,1,1,-1,1,-1,-1,-1,-1,-1,1,1,1,1,-1,1,1,-1,1,1,1,-1,-1,-1,-1,1,1,-1,-1,-1,1,-1,-1,1,-1,1,-1,-1,1,-1,1,1,-1,-1,1,1,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1,1,1,-1,1,-1,-1,1,-1,1,1,1,-1,1,-1,-1,1,1,-1,-1,-1,1,-1,1,1,-1,-1,-1,-1,-1,-1,1,-1,1,-1,-1,1,-1,-1,1,-1,1,1,1,1,1,-1,1,1,1,1,-1,-1,-1,1,1,-1,-1,-1,1,1,-1,1,1,1,-1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,1,-1,-1,1,1,1,-1,-1,1,-1,1,1,-1,-1,-1,1,-1,-1,-1,-1,1,1,-1,1,1,1,1,1,1,1,-1,-1,1,1,1,-1,-1,-1,1,1,-1,1,-1,1,-1,-1,1,-1,1,-1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,1,-1,1,1,1,1,1,-1,1,-1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,1,-1,-1,-1,-1,1,1,1,1,1,-1,1,1,-1,1,-1,1,-1,1,-1,-1,-1,1,-1,1,1,1,1,-1,1,1,-1,-1,1,1,1,-1,-1,1,1,1,1,1,-1,-1,-1,-1,-1,1,1,1,-1,-1,1,-1,-1,1,-1,1,-1,1,1,-1,-1,1,-1,1,1,1,1,-1,-1,1,-1,1,1,1,-1,-1,-1,-1,-1,1,-1,1,-1,1,1,-1,1,1,-1,-1,1,1,-1,-1,-1,-1,1,1,-1,1,-1,1,1,-1,1,1,1,-1,1,-1,-1,-1,1,-1,1,-1,1,1,1,1,1,1,-1,1,-1,-1,-1,1,1,1,-1,-1,1,1,-1,1,1,1,-1,-1,1,-1,1,-1,-1,-1,1,1,-1,1,-1,-1,-1,-1,-1,-1,1,1,-1,-1,1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,-1,-1,1,-1,-1,1,1,-1,1,1,-1,1,-1,-1,1,1,1,1,-1,-1,1,1,-1,1,-1,1,-1,1,1,-1,-1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,1,-1,-1,-1,-1,1,-1,-1,1,1,1,1,1,1,1,-1,1,1,1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,-1,-1,1,1,1,-1,1,1,-1,1,1,-1,-1,-1,1,-1,1,-1,-1,-1,1,-1,-1,1,1,-1,-1,1,-1,-1,-1,-1,-1,1,1,-1,1,-1,-1,1,-1,-1,1,1,1,1,-1,1,1,1,1,1,-1,-1,-1,1,-1,1,-1,1,-1,1,1,-1,1,-1,-1,-1,-1,1,-1,1,-1,-1,-1,-1,-1,-1,-1,1,-1,1,1,-1,1,1,-1,1,1,1,1,-1,-1,1,1,1,1,-1,-1,-1,1,-1,-1,-1,1,1,1,1,1,1,-1,1,1,-1,-1,-1,1,1,1,-1,1,-1,1,1,-1,1,-1,1,-1,-1,-1,-1,1,1,-1,-1,1,1,-1,1,1,-1,-1,-1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,-1,1,1,-1,1,1,-1,1,-1,1,1,1,-1,1,-1,1,1,1,1,-1,-1,-1,-1,1,-1,1,-1,1,-1,-1,1,-1,-1,-1,-1,1,-1,1,1,-1,-1,1,-1,-1,1,1,-1,-1,-1,-1,-1])
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, 'CIR', False)
        self.blocks_file_sink_1.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.fir_filter_xxx_0_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.root_raised_cosine_filter_0, 0))


    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate, self.alpha, 64))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate, self.alpha, 64))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-a", "--alpha", dest="alpha", type=eng_float, default="500.0m",
        help="Set alpha [default=%(default)r]")
    parser.add_argument(
        "-f", "--center-freq", dest="center_freq", type=eng_float, default="3.56G",
        help="Set center_freq [default=%(default)r]")
    parser.add_argument(
        "-g", "--gain", dest="gain", type=eng_float, default="20.0",
        help="Set gain [default=%(default)r]")
    parser.add_argument(
        "-i", "--index", dest="index", type=eng_float, default="0.0",
        help="Set index [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default="24.0M",
        help="Set samp_rate [default=%(default)r]")
    return parser


def main(top_block_cls=cir_rx10d, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(alpha=options.alpha, center_freq=options.center_freq, gain=options.gain, index=options.index, samp_rate=options.samp_rate)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
