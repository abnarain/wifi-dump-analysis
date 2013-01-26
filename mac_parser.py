#Author : Abhinav Narain 
#Date : 15 Jan, 2012 
#Purpose : Defines all the parsing functions for mac headers and radiotap header 
import sys
import struct
from header import *


ieee80211= radiotap_rx()
mcs_rate=mcs_flags()
channel_flags=channel_flag()
flags=flag()	 

def print_hex_mac(src_mac_address,string):
	print string , "  ",
	print hex(list(struct.unpack('B',src_mac_address[0]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[1]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[2]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[3]))[0]),":",	
	print hex(list(struct.unpack('B',src_mac_address[4]))[0]),":",
	print hex(list(struct.unpack('B',src_mac_address[5]))[0])

#defines used in C for bits

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



def parse_radiotap(frame,radiotap_len,present_flag,offset):
	if radiotap_len == 58 :
		frame_element=[]				
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_TSFT :
			timestamp=list(struct.unpack('<Q',frame[offset:offset+8]))[0]
			frame_element.append(timestamp)
			print timestamp
			offset +=8			
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_FLAGS : 			
			radiotap_flags= list(struct.unpack('B',frame[offset]))[0] #bad fcs; short preamble
			#print "flags: ", "offset= " ,offset, "constant ", struct.unpack('B',frame[16]), "var:",  radiotap_flags
			if radiotap_flags & 0x3f :
				count =1 
			frame_element.append(radiotap_flags)
			offset +=1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RATE :
			radiotap_rate=  list(struct.unpack('B',frame[offset]))[0]
			if radiotap_rate >= 0x80 and radiotap_rate <=0x8f :
							print "rate = ", radiotap_rate & 0x7f
			else:
							print " %0.1f" % (radiotap_rate /2)
			frame_element.append(radiotap_rate)
			offset +=1
		else :
			radiotap_rate=  struct.unpack('B',frame[offset])
			#print "Non ht rate =" , radiotap_rate
			offset +=1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_CHANNEL : 			
			#print "offset before channel ",offset 
			radiotap_freq=struct.unpack('<H',frame[offset:offset+2]) #18:20
			offset += 2
			#print "radiotap freq = " , radiotap_freq 
			radiotap_fhss=struct.unpack('<H',frame[offset:offset+2]) #20:22
			offset += 2 
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_DBM_ANTSIGNAL :
			#print "dbm signal offset[22] " ,offset
			radiotap_signal=struct.unpack('B',frame[offset])
			#print "signal with sign" ,struct.unpack('b',frame[offset])
			offset += 1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_DBM_ANTNOISE : 
			radiotap_noise=struct.unpack('B',frame[offset]) #23
			#print "noise with sign " ,radiotap_noise
			offset += 1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_ANTENNA :
			radiotap_antenna= struct.unpack('B',frame[offset])#24
			offset += 1
			#padding 
			offset += 1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RX_FLAGS :
			radiotap_rx_flags= list(struct.unpack('<H',frame[offset:offset+2]))[0]#26:28
			if radiotap_rx_flags & flags.IEEE80211_RADIOTAP_F_RX_BADPLCP:
				print "bad plcp"
			offset += 2
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_MCS :
			#print "mcs offset ",offset			
			radiotap_mcs=list(struct.unpack('B',frame[offset]))[0]
			offset += 1 
			radiotap_short_gi=list(struct.unpack('B',frame[offset]))[0]
			#print "short gi offset ",offset
			offset += 1 
			radiotap_bw_40=list(struct.unpack('B',frame[offset]))[0]
			offset += 1 
			#print "bw 40 offset ",offset
#			print "ht rate " , ht_rates[radiotap_mcs][][]
		homesaw_oui_1=list(struct.unpack('B',frame[offset]))[0]
		offset +=1 
		homesaw_oui_2=list(struct.unpack('B',frame[offset]))[0]
		offset +=1 
		homesaw_oui_3=list(struct.unpack('B',frame[offset]))[0]
		offset +=1 
		homesaw_namespace=list(struct.unpack('B',frame[offset]))[0]
		offset +=1 
		skip_len=int(list(struct.unpack('>H',frame[offset:offset+2]))[0])
		offset +=2
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_PHYERR_COUNT :
			radiotap_phyerr_count = list(struct.unpack('<I',frame[offset:offset+4]))[0]
			#print " phy count= ",radiotap_phyerr_count
			offset += 4
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_CCK_PHYERR_COUNT :
			radiotap_cck_phyerr_count = list(struct.unpack('<I',frame[offset:offset+4]))[0]
			#print " cck phy count= ",radiotap_cck_phyerr_count 
			offset += 4
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_OFDM_PHYERR_COUNT :
			radiotap_ofdm_phyerr_count = list(struct.unpack('<I',frame[offset:offset+4]))[0]
			offset += 4
			#print " ofdm phy count " ,radiotap_ofdm_phyerr_count
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RX_QUEUE_TIME :
			radiotap_rx_queue_time =  list(struct.unpack('<I',frame[offset:offset+4]))[0]
			#print "rx queue time " ,radiotap_rx_queue_time 
			offset +=4
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_CAPLEN :
			radiotap_caplen=  int(list(struct.unpack('<H',frame[offset:offset+2]))[0])
			#print "rx caplen",radiotap_caplen
			offset +=2
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RSSI :
			radiotap_rssi= int(list(struct.unpack('B',frame[offset]))[0])
			#print "rx rssi =", radiotap_rssi
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RADIOTAP_NAMESPACE :
			pass #print "radiotap namespace "
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_VENDOR_NAMESPACE :
			pass 
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_EXT :
			pass
#		print "signl=" , radiotap_signal, "noise=" , radiotap_noise 
#		print "rssi= " , list(radiotap_signal)[0]-list(radiotap_noise)[0]
#		print  "antenna= ", radiotap_antenna ,  "freq=" ,radiotap_freq
#		print "homesaw 1,2,3", homesaw_oui_1 , homesaw_oui_2, homesaw_oui_3
		radoptap_calc_rssi =list(radiotap_signal)[0]-list(radiotap_noise)[0] 
		if (not( homesaw_oui_1 ==11 and homesaw_oui_2 ==11 and  homesaw_oui_3 ==11 )):
			print homesaw_oui_1, homesaw_oui_2,  homesaw_oui_3 
			print "homesaw oui are corrupted " 
			print "homesaw namespace= " ,homesaw_namespace 
			sys.exit(1)
		if homesaw_namespace != 1:
							print "homesaw namespace is 1 " 
							sys.exit(1) 
	elif radiotap_len == 42:
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_TSFT :
			timestamp=struct.unpack('<Q',frame[offset:offset+8])
			#print timestamp
			offset +=8
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_FLAGS : 
			radiotap_flags= frame[offset] #bad fcs; short preamble
			#print "flags ",radiotap_flags
			offset +=1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RATE :
			radiotap_rate=struct.unpack('<H',frame[offset:offset+2]) #
			#print "rate =",radiotap_rate
			offset +=2
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_TX_FLAGS :
			radiotap_tx_flags=list(struct.unpack('<H',frame[offset:offset+2]))[0]
			if radiotap_tx_flags & flags.IEEE80211_RADIOTAP_F_TX_RTS:
				print " TX RTS SHIIIIT " 
			if radiotap_tx_flags & flags.IEEE80211_RADIOTAP_F_TX_RTS:
				print "TX CTS shhiiiit "
			offset +=2
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_DATA_RETRIES :
			radiotap_data_retries=struct.unpack('B',frame[offset])
			#print "Data retries =",radiotap_data_retries 
			offset +=1
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_MCS :
			radiotap_mcs=struct.unpack('B',frame[offset])
			offset += 1 
			radiotap_short_gi=struct.unpack('B',frame[offset])
			offset += 1 
			radiotap_bw_40=struct.unpack('B',frame[offset])
			offset += 1 
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_TOTAL_TIME :
			radiotap_rx_total_time =  int(list(struct.unpack('<I',frame[offset:offset+4]))[0])
			#print "total time " , radiotap_rx_total_time 
			offset += 4
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_CONTENTION_TIME :
			radiotap_rx_contention_time =  int(list(struct.unpack('<I',frame[offset:offset+4]))[0])
			#print " contention time", radiotap_rx_contention_time
			offset += 4
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RATES_TRIED : #10 in number in max			
			rates_tried =frame[offset:offset+10]
#		print "LLLLlast element", struct.unpack('B',frame[offset+10]) # last element location=39
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_RADIOTAP_NAMESPACE :
			pass
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_VENDOR_NAMESPACE :
			pass
		if present_flag & 1<<ieee80211.IEEE80211_RADIOTAP_EXT :
			pass

def parse_mgmt_fc(frame_control):
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
def parse_data_fc(fc):
	def FC_TO_DS(fc) :
		return ((fc) & 0x0100)
	def FC_FROM_DS(fc) :
		return ((fc) & 0x0200)
	if ( not(FC_TO_DS(fc)) and not(FC_FROM_DS(fc))) :
#		ADDR2 , 1 
		print "Fuckniog shit " 
	elif ( not(FC_TO_DS(fc)) and  FC_FROM_DS(fc)) :
#		ADDR3,2
		print "this is the mac address to look for "		
	elif (FC_TO_DS(fc) and not(FC_FROM_DS(fc))) :
#		ADDR 2,3
		print "fucking some other shit " 
	elif (FC_TO_DS(fc) and (FC_FROM_DS(fc))) :
#		ADDR4,3
		print " ffucking hte last shit on the code planet "
def parse_ctrl_fc(frame_control):
	if FC_SUBTYPE(frame_control) ==  CTRL_BAR  :
		pass
	elif FC_SUBTYPE(frame_control) == CTRL_BA :
		pass
	elif FC_SUBTYPE(frame_control) == CTRL_PS_POLL :
		pass
	elif FC_SUBTYPE(frame_control) == CTRL_RTS :
		pass
	elif FC_SUBTYPE(frame_control) == CTRL_CTS :
		pass
	elif FC_SUBTYPE(frame_control) == CTRL_ACK :
		pass
	elif FC_SUBTYPE(frame_control) == CTRL_CF_END :
		pass
	elif FC_SUBTYPE(frame_control) == CTRL_END_ACK :
		pass


def parse_frame_control(frame_control) :	
	if FC_TYPE(frame_control)==T_DATA:
		print "Data"
		parse_data_fc(frame_control)
	if FC_TYPE(frame_control)==T_MGMT:
		print "Mgmt "
		parse_mgmt_fc(frame_control)
	if FC_TYPE(frame_control)==T_CTRL :
		print "ctrl " 
		parse_ctrl_fc(frame_control)
	if FC_WEP(frame_control):
		pass
	if FC_RETRY(frame_control):
		print "RETRY "
	if FC_ORDER(frame_control):
		pass 
	if FC_POWER_MGMT(frame_control):
		pass
	if FC_MORE_FLAG(frame_control):
		pass
	if FC_MORE_DATA(frame_control):
		pass

def seqctl_frag_number(x) : 
	return (x) & 0x00f		

def seqctl_seq_number(x):
	return 	(((x) & 0xfff0) >> 4 )
def parse_data_frame(frame,radiotap_len):
	print "radiotap len =" , radiotap_len
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	offset +=4
	src_mac_address= frame[offset:offset+6]	
	print_hex_mac(src_mac_address,"src mac")
	offset +=6
	dest_mac_address= frame[offset:offset+6]
	print_hex_mac(dest_mac_address,"dest mac")
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
	parse_frame_control(frame_control)
	offset +=2
	sequence_control_bytes = list(struct.unpack('>H',frame[offset:offset+2]))[0]
	frame_fragment_number=seqctl_frag_number(sequence_control_bytes)
	frame_sequence_number =seqctl_seq_number(sequence_control_bytes )
	print "seq no.", frame_sequence_number
	print "fragment no." ,frame_fragment_number
	offset +=2 


def parse_err_data_frame(frame,radiotap_len):
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	offset +=4
	src_mac_address= frame[offset:offset+6]
	print_hex_mac(src_mac_address,"src mac")	
	offset +=6
	
	if int(list(struct.unpack('B',src_mac_address[3]))[0])!=0 &  int(list(struct.unpack('B',src_mac_address[4]))[0]) != 0  & int(list(struct.unpack('B',src_mac_address[5]))[0]):
		sys.exit(1)
	dest_mac_address= frame[offset:offset+6]
	print_hex_mac(dest_mac_address,"dest mac")
	offset +=6
	
	if int(list(struct.unpack('B',dest_mac_address[3]))[0]) !=0 &  int(list(struct.unpack('B',dest_mac_address[4]))[0]) != 0 &  int(list(struct.unpack('B',dest_mac_address[5]))[0]) !=0 :
		print "this should not happen with all the frames btw ..."
		sys.exit(1) 
       
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
	parse_frame_control(frame_control)
	offset +=2	
	sequence_control_bytes = list(struct.unpack('>H',frame[offset:offset+2]))[0]
	frame_fragment_number=seqctl_frag_number(sequence_control_bytes)
	frame_sequence_number =seqctl_seq_number(sequence_control_bytes )
	print "seq no.", frame_sequence_number
	print "fragment no." ,frame_fragment_number
	

def parse_mgmt_beacon_frame(frame,radiotap_len):
	def CAPABILITY_ESS(cap)  :
		((cap) & 0x0001)

	def CAPABILITY_PRIVACY(cap):
		 ((cap) & 0x0010)

	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	offset +=4
	src_mac_address= frame[offset:offset+6]	
	print_hex_mac(src_mac_address,"src mac address")
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
        offset +=2	
	parse_frame_control(frame_control)	
	sequence_control_bytes = list(struct.unpack('>H',frame[offset:offset+2]))[0]
	frame_fragment_number=seqctl_frag_number(sequence_control_bytes)
	frame_sequence_number =seqctl_seq_number(sequence_control_bytes )
	print "seq no.", frame_sequence_number
	print "fragment no." ,frame_fragment_number
	offset +=2
	ht_support=list(struct.unpack('B',frame[offset]))[0]
	offset +=1 
	cap_info = list(struct.unpack('B',frame[offset]))[0]

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
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len 
	offset +=4
	src_mac_address= frame[offset:offset+6]	
	print_hex_mac(src_mac_address, "src mac ")
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
	offset +=2	
	parse_frame_control(frame_control)
	sequence_control_bytes = list(struct.unpack('>H',frame[offset:offset+2]))[0]
	frame_fragment_number=seqctl_frag_number(sequence_control_bytes)
	frame_sequence_number =seqctl_seq_number(sequence_control_bytes )
	print "seq no.", frame_sequence_number
	print "fragment no." ,frame_fragment_number
	offset +=2 

def parse_mgmt_err_frame(frame,radiotap_len):
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	offset +=4
	src_mac_address= frame[offset:offset+6]	
	print_hex_mac(src_mac_address,"src mac address" )
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
	offset +=2	
	print "frame control " , frame_control 
	sequence_control_bytes = list(struct.unpack('>H',frame[offset:offset+2]))[0]
	frame_fragment_number=seqctl_frag_number(sequence_control_bytes)
	frame_sequence_number =seqctl_seq_number(sequence_control_bytes )
	print "seq no.", frame_sequence_number
	print "fragment no." ,frame_fragment_number
	offset +=2 



def parse_ctrl_frame(frame,radiotap_len):
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	offset +=4
	src_mac_address= frame[offset:offset+6]	 
	print_hex_mac(src_mac_address, "src mac address")
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
	offset +=2	
	parse_frame_control(frame_control)


def parse_ctrl_err_frame(frame,radiotap_len):
	offset = radiotap_len
	pkt_len =list(struct.unpack('>I',frame[offset:offset+4]))[0]-FCS_LEN-radiotap_len
	offset +=4
	src_mac_address= frame[offset:offset+6]		      
	print_hex_mac(src_mac_address,"src_mac")
	offset +=6
	frame_control= list(struct.unpack('>H',frame[offset:offset+2]))[0]
        offset +=2	
	parse_frame_control(frame_control)
