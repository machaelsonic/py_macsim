#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

class Powermesh_Timing():
    def __init__(self):
        self.bpsk_bit_timing = 24*38/5e6
        self.ds15_bit_timing = 24*38/5e6*15
        self.ds63_bit_timing = 24*38/5e6*63
        
        self.bpsk_bit_rate = 5e6/(24*38)
        self.ds15_bit_rate = 5e6/(24*38)/15
        self.ds63_bit_rate = 5e6/(24*38)/63
        
        self.phy_framing_cost = 24+11+22            # 物理层同步头,同步码,EOP开销
        self.scan_interval = 0.010                  # scan包之间间隔
    
    def basic_bit_timing(self, rate):
        if rate is 'bpsk':
            return self.bpsk_bit_timing
        elif rate is 'ds15':
            return self.ds15_bit_timing
        elif rate is 'ds63':
            return self.ds63_bit_timing
        else:
            raise ValueError('Error rate %s' % rate)
    
    def phy_basic_bit_rate(self, rate):
        if rate is 'bpsk':
            return self.bpsk_bit_rate
        elif rate is 'ds15':
            return self.ds15_bit_rate
        elif rate is 'ds63':
            return self.ds63_bit_rate
        else:
            raise ValueError('Error rate %s' % rate)
    
        
    def phy_packet_bits(self, phy_bytes):
            return self.phy_framing_cost + phy_bytes * 11

    def phy_packet_timing(self, phy_bytes, rate='bpsk', scan=False):
        timing = self.phy_packet_bits(phy_bytes) * self.basic_bit_timing(rate)
        if scan:
            timing = timing * 4 + self.scan_interval * 3    # scan数据包重复4遍
        return timing

    def phy_srf_timing(self, rate='bpsk', scan=False):
        return self.phy_packet_timing(4, rate, scan)                # 基本srf 4字节
        
    def app_psr_timing(self, apdu_bytes, rate):
        return self.phy_packet_timing(apdu_bytes + 18 + 3 + 1)
    
    def app_dst_timing(self, apdu_bytes, rate, scan):
        return self.phy_packet_timing(apdu_bytes + 18 + 6 + 1, rate, scan)
        

if __name__=='__main__':
    tim = Powermesh_Timing()
    
    print tim.phy_packet_bits(11)
    print 'srf timing:', tim.phy_srf_timing(rate='bpsk', scan=True)
    print 'app psr timing:', tim.app_dst_timing(40, rate='ds63', scan=True)
    
    print 'Timing Test Exit'
