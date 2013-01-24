#Author : Abhinav Narain 
#Date : 15 Jan, 2012 
#Purpose : Defines all the parsing functions for mac headers and radiotap header 
import sys
import struct
from header import *


count_bad=0
ieee80211= radiotap_rx()
mcs_rate=mcs_flags()
channel_flags=channel_flag()
flags=flag()	 
def parse_radiotap(frame,radiotap_len,present_flag,offset):
	if radiotap_len == 58 :
		frame_element=[]				
		print "@@"
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_TSFT :
			timestamp=struct.unpack('<Q',frame[offset:offset+8])
			frame_element.append(timestamp)
			print timestamp
			offset +=8			
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_FLAGS : 			
			radiotap_flags= list(struct.unpack('B',frame[offset]))[0] #bad fcs; short preamble
			print "flags: ", "offset= " ,offset, "constant ", struct.unpack('B',frame[16]), "var:",  radiotap_flags
			print flags.IEEE80211_RADIOTAP_F_BADFCS
			if radiotap_flags & 0x3f :
				print "fuckign badfcs " 
				global count_bad
				count_bad +=1
			frame_element.append(radiotap_flags)
			offset +=1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RATE :
			radiotap_rate=  struct.unpack('B',frame[offset])
			print "rate =" , radiotap_rate
#			frame_element.append()
			frame_element.append(radiotap_rate)
			offset +=1
		else :
			radiotap_rate=  struct.unpack('B',frame[offset])
			print "Non ht rate =" , radiotap_rate
			offset +=1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_CHANNEL : 			
			print "offset before channel ",offset 
			radiotap_freq=struct.unpack('<H',frame[offset:offset+2]) #18:20
			offset += 2
			print "radiotap freq = " , radiotap_freq 
			radiotap_fhss=struct.unpack('<H',frame[offset:offset+2]) #20:22
			offset += 2 
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_DBM_ANTSIGNAL :
			print "dbm signal offset[22] " ,offset
			radiotap_signal=struct.unpack('B',frame[offset])
			print "signal with sign" ,struct.unpack('b',frame[offset])
			offset += 1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_DBM_ANTNOISE : 
			radiotap_noise=struct.unpack('B',frame[offset]) #23
			print "noise with sign " ,struct.unpack('b',frame[offset]) #23
			offset += 1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_ANTENNA :
			radiotap_antenna= struct.unpack('B',frame[offset])#24
			offset += 1
			#padding 
			offset += 1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RX_FLAGS :
			print "rx flags"
			radiotap_rx_flags= struct.unpack('<H',frame[offset:offset+2])#26:28
			offset += 2
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_MCS :
			print "mcs offset ",offset			
			radiotap_mcs=struct.unpack('B',frame[offset])
			offset += 1 
			radiotap_short_gi=struct.unpack('B',frame[offset])
			print "short gi offset ",offset
			offset += 1 
			radiotap_bw_40=struct.unpack('B',frame[offset])
			offset += 1 
			print "bw 40 offset ",offset
		homesaw_oui_1=struct.unpack('B',frame[offset])
		offset +=1 
		homesaw_oui_2=struct.unpack('B',frame[offset])
		offset +=1 
		homesaw_oui_3=struct.unpack('B',frame[offset])
		offset +=1 
		homesaw_namespace=struct.unpack('B',frame[offset])
		offset +=1 
		skip_len=struct.unpack('>H',frame[offset:offset+2])
		offset +=2
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_PHYERR_COUNT :
			radiotap_phyerr_count = struct.unpack('<I',frame[offset:offset+4])
			print " phy count= ",radiotap_phyerr_count
			offset += 4
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_CCK_PHYERR_COUNT :
			radiotap_cck_phyerr_count = struct.unpack('<I',frame[offset:offset+4])
			print " cck phy count= ",radiotap_cck_phyerr_count 
			offset += 4
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_OFDM_PHYERR_COUNT :
			radiotap_ofdm_phyerr_count = struct.unpack('<I',frame[offset:offset+4])
			offset += 4
			print " ofdm phy count " ,radiotap_ofdm_phyerr_count
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RX_QUEUE_TIME :
			radiotap_rx_queue_time = struct.unpack('<I',frame[offset:offset+4])
			print "rx queue time " ,radiotap_rx_queue_time 
			offset +=4
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_CAPLEN :
			radiotap_caplen= struct.unpack('<H',frame[offset:offset+2])
			print "rx caplen",radiotap_caplen
			offset +=2
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RSSI :
			radiotap_rssi= struct.unpack('B',frame[offset])
			print "rx rssi =", radiotap_rssi
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RADIOTAP_NAMESPACE :
			print "radiotap namespace "
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_VENDOR_NAMESPACE :
			pass 
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_EXT :
			pass
		print "signl=" , radiotap_signal, "noise=" , radiotap_noise 
		print "rssi= " , list(radiotap_signal)[0]-list(radiotap_noise)[0]
		print  "antenna= ", radiotap_antenna ,  "freq=" ,radiotap_freq
		print "homesaw 1,2,3", homesaw_oui_1 , homesaw_oui_2, homesaw_oui_3
		print "homesaw namespace= " ,homesaw_namespace 
	elif radiotap_len == 42:
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_TSFT :
			timestamp=struct.unpack('<Q',frame[offset:offset+8])
			print timestamp
			offset +=8
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_FLAGS : 
			radiotap_flags= frame[offset] #bad fcs; short preamble
			print "flags ",radiotap_flags
			offset +=1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RATE :
			radiotap_rate=struct.unpack('<H',frame[offset:offset+2]) #
			print "rate =",radiotap_rate
			offset +=2
#txflags IEEE80211_RADIOTAP_F_TX_RTS, IEEE80211_TX_RC_USE_RTS_CTS 
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_TX_FLAGS :
			radiotap_tx_flags=struct.unpack('<H',frame[offset:offset+2])
			offset +=2
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_DATA_RETRIES :
			radiotap_data_retries=struct.unpack('B',frame[offset])
			print "Data retries =",radiotap_data_retries 
			offset +=1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_MCS :
			radiotap_mcs=struct.unpack('B',frame[offset])
			offset += 1 
			radiotap_short_gi=struct.unpack('B',frame[offset])
			offset += 1 
			radiotap_bw_40=struct.unpack('B',frame[offset])
			offset += 1 
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_TOTAL_TIME :
			radiotap_total_time = struct.unpack('<I',frame[offset:offset+4])
			print "total time " , radiotap_total_time 
			offset += 4
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_CONTENTION_TIME :
			radiotap_contention_time = struct.unpack('<I',frame[offset:offset+4])
			print " contention time", radiotap_contention_time
			offset += 4
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RATES_TRIED : #10 in number in max			
			rates_tried =frame[offset:offset+10]
#		print "LLLLlast element", struct.unpack('B',frame[offset+10]) # last element location=39
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RADIOTAP_NAMESPACE :
			print "radiotap namespace "
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_VENDOR_NAMESPACE :
			print "vendor namespace " 
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_EXT :
			print "radiotap ext " 


def FC_MORE_FLAG(fc):
        return ((fc) & 0x0400)
def FC_RETRY(fc) :       
	return ((fc) & 0x0800)
def FC_POWER_MGMT(fc):
	return ((fc) & 0x1000)
def FC_MORE_DATA(fc):
        return ((fc) & 0x2000)
def FC_WEP(fc) :
	return ((fc) & 0x4000)
def FC_ORDER(fc):
	return ((fc) & 0x8000)

def FC_TYPE(fc) :
	return (((fc) >> 2) & 0x3)
def FC_SUBTYPE(fc) :
	return (((fc) >> 4) & 0xF)

def parse_frame_control(frame_control) :
	if T_DATA==FC_TYPE(frame_control):
		print "DATA TYPE"		
	if FC_TYPE(frame_control)==T_MGMT:
		print "MGMT TYPE "
		parse_mgmt_header(frame_control)
	if FC_TYPE(frame_control)==T_CTRL :
		print "CTL TYPE" 
		parse_ctrl_header(frame_control)
	if FC_WEP(frame_control):
		print "WEP ENC"
	if FC_RETRY(frame_control):
		print "RETRY "
	if FC_ORDER(frame_control):
		print "ORDER"
	if FC_POWER_MGMT(frame_control):
		print "POWER MGMT"
	if FC_MORE_FLAG(frame_control):
		print "MORE FLAG"
	if FC_MORE_DATA(frame_control):
		print "MORE DATA" 


def parse_mgmt_beacon_frame(frame,radiotap_len):
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	print "pkt_len= ",pkt_len
	offset +=4
	src_mac_address= frame[offset:offset+6]	
	print "src mac " , 
	print hex(list(struct.unpack('B',src_mac_address[0]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[1]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[2]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[3]))[0]),":",	
	print hex(list(struct.unpack('B',src_mac_address[4]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[5]))[0])
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
        offset +=2	
        print "frame control " , frame_control 
	if FC_SUBTYPE(frame_control) ==   ST_BEACON :
		print "BEACON"
	elif FC_SUBTYPE(frame_control) == ST_ASSOC_REQUEST :
		print "ASS REQ"	
	elif FC_SUBTYPE(frame_control) == ST_ASSOC_RESPONSE :
		print "RES"
	elif FC_SUBTYPE(frame_control) == ST_REASSOC_REQUEST :
		print "REASS REQ"
	elif FC_SUBTYPE(frame_control) == ST_REASSOC_RESPONSE :
		print "REASS RESP"
	elif FC_SUBTYPE(frame_control) == ST_PROBE_REQUEST :
		print "PROBE REQ"
	elif FC_SUBTYPE(frame_control) == ST_PROBE_RESPONSE :
		print "PROBE RES"
	elif FC_SUBTYPE(frame_control) == ST_DISASSOC :
		print "DISS "
	elif FC_SUBTYPE(frame_control) == ST_ATIM :
		print "ATIM "
	elif FC_SUBTYPE(frame_control) == ST_AUTH :
		print "AUTH"
	elif FC_SUBTYPE(frame_control) == ST_DEAUTH :
		print " DEAUTH"
	elif FC_SUBTYPE(frame_control) == ST_ACTION :
		print "ACTION "
	
        seq_control = list(struct.unpack('>H',frame[offset:offset+2]))[0]
        print "seq_control " , seq_control
        offset +=2
        ht_support=list(struct.unpack('B',frame[offset]))[0]
	offset +=1 
	cap_info = list(struct.unpack('B',frame[offset]))[0]
	def CAPABILITY_ESS(cap)  :
		((cap) & 0x0001)

	def CAPABILITY_PRIVACY(cap):
		 ((cap) & 0x0010)

	if CAPABILITY_ESS(cap_info):
		print "ESS"
	else :
		print "IBSS" 

	if CAPABILITY_PRIVACY(cap_info):
		print "PRIVACY"
	else:
		print "NOT PRIVATE"

	if (ht_support==1):
		print "I have a fuckign n ap" 
	print "final offset = ", offset, "offset-radiotap =", offset-radiotap_len

def parse_mgmt_common_frame(frame,radiotap_len):
	offset = radiotap_len
	try :	
		pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len 
	except : 
		print offset
		print "frame size is " , len(frame)
		print "max len= " ,MGMT_COMMON_STRUCT_SIZE
		print "fuck "
		
	offset +=4
	src_mac_address= frame[offset:offset+6]	
	print "src mac " , 
	print hex(list(struct.unpack('B',src_mac_address[0]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[1]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[2]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[3]))[0]),":",	
	print hex(list(struct.unpack('B',src_mac_address[4]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[5]))[0])
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
        offset +=2	
        print "frame control " , frame_control 
        seq_control = struct.unpack('>H',frame[offset:offset+2])
        print "seq_control " , seq_control
        offset +=2
                                                                                  
	print "final offset = ", offset, "offset-radiotap =", offset-radiotap_len


def parse_mgmt_err_frame(frame,radiotap_len):
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	offset +=4
	src_mac_address= frame[offset:offset+6]	
	print "src mac " , 
	print hex(list(struct.unpack('B',src_mac_address[0]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[1]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[2]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[3]))[0]),":",	
	print hex(list(struct.unpack('B',src_mac_address[4]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[5]))[0])
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
        offset +=2	
        print "frame control " , frame_control 
        seq_control = struct.unpack('>H',frame[offset:offset+2])
        print "seq_control " , seq_control
        offset +=2
                                                                                  
	print "final offset = ", offset, "offset-radiotap =", offset-radiotap_len


def parse_ctrl_frame(frame,radiotap_len):
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	print "pkt_len= ",pkt_len
	offset +=4
	src_mac_address= frame[offset:offset+6]	
	print "src mac " , 
	print hex(list(struct.unpack('B',src_mac_address[0]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[1]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[2]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[3]))[0]),":",	
	print hex(list(struct.unpack('B',src_mac_address[4]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[5]))[0])
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
        offset +=2	
	if FC_SUBTYPE(frame_control) ==  CTRL_BAR  :
		print "BAR" 
	elif FC_SUBTYPE(frame_control) == CTRL_BA :
		print "BA"
	elif FC_SUBTYPE(frame_control) == CTRL_PS_POLL :
		print "PS POLL"
	elif FC_SUBTYPE(frame_control) == CTRL_RTS :
		print "RTS"
	elif FC_SUBTYPE(frame_control) == CTRL_CTS :
		print "CTS"
	elif FC_SUBTYPE(frame_control) == CTRL_ACK :
		print "ACK"
	elif FC_SUBTYPE(frame_control) == CTRL_CF_END :
		print "CF_END"
	elif FC_SUBTYPE(frame_control) == CTRL_END_ACK :
		print "ACK"
	
def parse_ctrl_err_frame(frame,radiotap_len):
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	print "pkt_len= ",pkt_len
	offset +=4
	src_mac_address= frame[offset:offset+6]	
	print "src mac " , 
	print hex(list(struct.unpack('B',src_mac_address[0]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[1]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[2]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[3]))[0]),":",	
	print hex(list(struct.unpack('B',src_mac_address[4]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[5]))[0])
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
        offset +=2	
	if FC_SUBTYPE(frame_control) ==  CTRL_BAR  :
		print "BAR" 
	elif FC_SUBTYPE(frame_control) == CTRL_BA :
		print "BA"
	elif FC_SUBTYPE(frame_control) == CTRL_PS_POLL :
		print "PS POLL"
	elif FC_SUBTYPE(frame_control) == CTRL_RTS :
		print "RTS"
	elif FC_SUBTYPE(frame_control) == CTRL_CTS :
		print "CTS"
	elif FC_SUBTYPE(frame_control) == CTRL_ACK :
		print "ACK"
	elif FC_SUBTYPE(frame_control) == CTRL_CF_END :
		print "CF_END"
	elif FC_SUBTYPE(frame_control) == CTRL_END_ACK :
		print "ACK"

def parse_data_frame(frame,radiotap_len):
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	print "pkt_len= ",pkt_len
	offset +=4
	src_mac_address= frame[offset:offset+6]	
	print "src mac " , 
	print hex(list(struct.unpack('B',src_mac_address[0]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[1]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[2]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[3]))[0]),":",	
	print hex(list(struct.unpack('B',src_mac_address[4]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[5]))[0])
	offset +=6
	
	dest_mac_address= frame[offset:offset+6]
	print "dest mac " ,
	print hex(list(struct.unpack('B',dest_mac_address[0]))[0]),":",
	print hex(list(struct.unpack('B',dest_mac_address[1]))[0]),":",
	print hex(list(struct.unpack('B',dest_mac_address[2]))[0]),":",
	print hex(list(struct.unpack('B',dest_mac_address[3]))[0]),":",
	print hex(list(struct.unpack('B',dest_mac_address[4]))[0]),":",
	print hex(list(struct.unpack('B',dest_mac_address[5]))[0])
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
	offset +=2	
	print "frame control " , frame_control 
	seq_control = struct.unpack('>H',frame[offset:offset+2])
	print "seq_control " , seq_control
	offset +=2

	print "final offset = ", offset, "offset-radiotap =", offset-radiotap_len

	
def parse_err_data_frame(frame,radiotap_len):
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	print "pkt_len= ",pkt_len
	offset +=4
	src_mac_address= frame[offset:offset+6]
	
	print "src mac " , 
	print hex(list(struct.unpack('B',src_mac_address[0]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[1]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[2]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[3]))[0]),":",	
	print hex(list(struct.unpack('B',src_mac_address[4]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[5]))[0])
	offset +=6
	
	if int(list(struct.unpack('B',src_mac_address[3]))[0])!=0 &  int(list(struct.unpack('B',src_mac_address[4]))[0]) != 0  & int(list(struct.unpack('B',src_mac_address[5]))[0]) == 0  :
		print "FCIL" 
		sys.exit(1)
	dest_mac_address= frame[offset:offset+6]
	print "dest mac " ,
	print hex(list(struct.unpack('B',dest_mac_address[0]))[0]),":",
	print hex(list(struct.unpack('B',dest_mac_address[1]))[0]),":",
	print hex(list(struct.unpack('B',dest_mac_address[2]))[0]),":",
	print hex(list(struct.unpack('B',dest_mac_address[3]))[0]),":",
	print hex(list(struct.unpack('B',dest_mac_address[4]))[0]),":",
	print hex(list(struct.unpack('B',dest_mac_address[5]))[0])
	offset +=6
	
	if int(list(struct.unpack('B',dest_mac_address[3]))[0]) !=0 &  int(list(struct.unpack('B',dest_mac_address[4]))[0]) != 0 &  int(list(struct.unpack('B',dest_mac_address[5]))[0]) !=0 :
		print "fACA"
		sys.exit(1) 
       

	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
	offset +=2	
	print "frame control " , frame_control 
	seq_control = list(struct.unpack('>H',frame[offset:offset+2]))[0]
	print "seq_control " , seq_control
	offset +=2
	print "final offset = ", offset, "offset-radiotap =", offset-radiotap_len
	parse_frame_control(frame_control)

