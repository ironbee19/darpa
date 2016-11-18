#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Hurdle 1
# Generated: Wed Nov  2 21:07:30 2016
##################################################

from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import hurdle1


class hurdle_1(gr.top_block):

    def __init__(self, EbNo_dB=15, NumBits=100000, MinGap=2040, MaxGap=4095, frequency_offset_hz=100e3, host='127.0.0.1', iq_filename='iq.dat', iq_port=9094, packet_port=9095, rx_packet_filename='rx_packets.bin', timing_offset_ppm=20, truth_filename='truth.bin', tx_packet_filename='out_packets.bin'):
        gr.top_block.__init__(self, "Hurdle 1")

        ##################################################
        # Parameters
        ##################################################
        self.EbNo_dB = EbNo_dB
        self.NumBits = NumBits
        self.MinGap = MinGap
        self.MaxGap = MaxGap
        self.frequency_offset_hz = frequency_offset_hz
        self.host = host
        self.iq_filename = iq_filename
        self.iq_port = iq_port
        self.packet_port = packet_port
        self.rx_packet_filename = rx_packet_filename
        self.timing_offset_ppm = timing_offset_ppm
        self.truth_filename = truth_filename
        self.tx_packet_filename = tx_packet_filename

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 1000000
        self.samp_rate = samp_rate = 4000000
        self.samps_per_sym = samps_per_sym = samp_rate/symbol_rate
        
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(1.0, samp_rate, symbol_rate, 0.35, 11*4)
          
        
        self.qpsk = qpsk = digital.constellation_calcdist(([-1-1j, -1+1j, 1+1j, 1-1j]), ([0, 1, 3, 2]), 4, 1).base()
        
        self.noise_voltage = noise_voltage = (samp_rate/(2*symbol_rate)*10**(-EbNo_dB/10.0))**0.5

        ##################################################
        # Blocks
        ##################################################
        self.mod = digital.generic_mod(
          constellation=qpsk,
          differential=False,
          samples_per_symbol=samps_per_sym,
          pre_diff_code=True,
          excess_bw=0.7,
          verbose=False,
          log=False,
          )
        self.hurdle1_zero_pad_0 = hurdle1.zero_pad(gr.sizeof_gr_complex, 'zero_pad')
        self.hurdle1_traffic_parser_0 = hurdle1.traffic_parser('pkt_len', 'zero_pad')
        self.hurdle1_tcp_server_source_0 = hurdle1.tcp_server_source(gr.sizeof_char, host, packet_port)
        self.hurdle1_tcp_server_sink_0 = hurdle1.tcp_server_sink(gr.sizeof_gr_complex, host, iq_port)
        self.hurdle1_tag_delay_0 = hurdle1.tag_delay(int(22*samps_per_sym))
        self.hurdle1_random_packet_source_0 = hurdle1.random_packet_source(0x99999999, 0x1ACFFC1D, NumBits, MinGap, MaxGap, truth_filename)
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=noise_voltage,
        	frequency_offset=frequency_offset_hz/samp_rate,
        	epsilon=1+timing_offset_ppm/1e6,
        	taps=(1.0, ),
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, 'symbols_out.bin', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, rx_packet_filename, False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, iq_filename, False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.channels_channel_model_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.channels_channel_model_0, 0), (self.hurdle1_tcp_server_sink_0, 0))    
        self.connect((self.hurdle1_random_packet_source_0, 0), (self.hurdle1_traffic_parser_0, 0))    
        self.connect((self.hurdle1_tag_delay_0, 0), (self.hurdle1_zero_pad_0, 0))    
        self.connect((self.hurdle1_tcp_server_source_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.hurdle1_traffic_parser_0, 0), (self.mod, 0))    
        self.connect((self.hurdle1_zero_pad_0, 0), (self.channels_channel_model_0, 0))    
        self.connect((self.mod, 0), (self.blocks_file_sink_1, 0))    
        self.connect((self.mod, 0), (self.hurdle1_tag_delay_0, 0))    

    def get_EbNo_dB(self):
        return self.EbNo_dB

    def set_EbNo_dB(self, EbNo_dB):
        self.EbNo_dB = EbNo_dB
        self.set_noise_voltage((self.samp_rate/(2*self.symbol_rate)*10**(-self.EbNo_dB/10.0))**0.5)

    def get_frequency_offset_hz(self):
        return self.frequency_offset_hz

    def set_frequency_offset_hz(self, frequency_offset_hz):
        self.frequency_offset_hz = frequency_offset_hz
        self.channels_channel_model_0.set_frequency_offset(self.frequency_offset_hz/self.samp_rate)

    def get_host(self):
        return self.host

    def set_host(self, host):
        self.host = host

    def get_iq_filename(self):
        return self.iq_filename

    def set_iq_filename(self, iq_filename):
        self.iq_filename = iq_filename
        self.blocks_file_sink_0.open(self.iq_filename)

    def get_iq_port(self):
        return self.iq_port

    def set_iq_port(self, iq_port):
        self.iq_port = iq_port

    def get_packet_port(self):
        return self.packet_port

    def set_packet_port(self, packet_port):
        self.packet_port = packet_port

    def get_rx_packet_filename(self):
        return self.rx_packet_filename

    def set_rx_packet_filename(self, rx_packet_filename):
        self.rx_packet_filename = rx_packet_filename
        self.blocks_file_sink_0_0.open(self.rx_packet_filename)

    def get_timing_offset_ppm(self):
        return self.timing_offset_ppm

    def set_timing_offset_ppm(self, timing_offset_ppm):
        self.timing_offset_ppm = timing_offset_ppm
        self.channels_channel_model_0.set_timing_offset(1+self.timing_offset_ppm/1e6)

    def get_truth_filename(self):
        return self.truth_filename

    def set_truth_filename(self, truth_filename):
        self.truth_filename = truth_filename

    def get_tx_packet_filename(self):
        return self.tx_packet_filename

    def set_tx_packet_filename(self, tx_packet_filename):
        self.tx_packet_filename = tx_packet_filename

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_samps_per_sym(self.samp_rate/self.symbol_rate)
        self.set_noise_voltage((self.samp_rate/(2*self.symbol_rate)*10**(-self.EbNo_dB/10.0))**0.5)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samps_per_sym(self.samp_rate/self.symbol_rate)
        self.set_noise_voltage((self.samp_rate/(2*self.symbol_rate)*10**(-self.EbNo_dB/10.0))**0.5)
        self.channels_channel_model_0.set_frequency_offset(self.frequency_offset_hz/self.samp_rate)

    def get_samps_per_sym(self):
        return self.samps_per_sym

    def set_samps_per_sym(self, samps_per_sym):
        self.samps_per_sym = samps_per_sym

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage
        self.channels_channel_model_0.set_noise_voltage(self.noise_voltage)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--EbNo-dB", dest="EbNo_dB", type="eng_float", default=eng_notation.num_to_str(15),
        help="Set EbNo_dB [default=%default]")
    parser.add_option(
        "", "--num-bits", dest="NumBits", type="intx", default=100000,
        help="Set number of info bits to be genrated on tx[default=%default]")
    parser.add_option(
        "", "--min-gap", dest="MinGap", type="intx", default=2050,
        help="Min gap between packets in samples[default=%default]")
    parser.add_option(
        "", "--max-gap", dest="MaxGap", type="intx", default=4095,
        help="Max gap between packets in samples[default=%default]")
    parser.add_option(
        "", "--frequency-offset-hz", dest="frequency_offset_hz", type="eng_float", default=eng_notation.num_to_str(100e3),
        help="Set frequency_offset_hz [default=%default]")
    parser.add_option(
        "", "--host", dest="host", type="string", default='127.0.0.1',
        help="Set host [default=%default]")
    parser.add_option(
        "", "--iq-filename", dest="iq_filename", type="string", default='iq.dat',
        help="Set iq_filename [default=%default]")
    parser.add_option(
        "", "--iq-port", dest="iq_port", type="intx", default=9094,
        help="Set iq_port [default=%default]")
    parser.add_option(
        "", "--packet-port", dest="packet_port", type="intx", default=9095,
        help="Set packet_port [default=%default]")
    parser.add_option(
        "", "--rx-packet-filename", dest="rx_packet_filename", type="string", default='rx_packets.bin',
        help="Set rx_packet_filename [default=%default]")
    parser.add_option(
        "", "--timing-offset-ppm", dest="timing_offset_ppm", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set timing_offset_ppm [default=%default]")
    parser.add_option(
        "", "--truth-filename", dest="truth_filename", type="string", default='truth.bin',
        help="Set truth_filename [default=%default]")
    parser.add_option(
        "", "--tx-packet-filename", dest="tx_packet_filename", type="string", default='out_packets.bin',
        help="Set tx_packet_filename [default=%default]")
    return parser


def main(top_block_cls=hurdle_1, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(EbNo_dB=options.EbNo_dB, NumBits=options.NumBits, MinGap=options.MinGap, MaxGap=options.MaxGap, frequency_offset_hz=options.frequency_offset_hz, host=options.host, iq_filename=options.iq_filename, iq_port=options.iq_port, packet_port=options.packet_port, rx_packet_filename=options.rx_packet_filename, timing_offset_ppm=options.timing_offset_ppm, truth_filename=options.truth_filename, tx_packet_filename=options.tx_packet_filename)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()