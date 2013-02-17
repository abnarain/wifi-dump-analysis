#Author : Abhinav Narain
#Date : Feb 9, 2012
#Purpose : To read the binary files with data from BISmark deployment in homes

import os,sys,re
import gzip
import struct 


from  header import *
from mac_parser import * 
from stats import *

try:
    import cPickle as pickle
except ImportError:
    import pickle

missing_files=[]
tx_time_series= []
rx_time_series= []
if len(sys.argv) !=5:	
	print len(sys.argv)
	print "Usage : python reader.py data/<data.gz> mgmt/<mgmt.gz> ctrl/<ctrl.gz> <output station filename> <t1> <t2>"
	sys.exit(1)
#compare regular expression for filenameif argv[1] for the lexicographic /time ordering so that we load them in order in the first place
t1= 
t2=
data_f_dir=sys.argv[1]
mgmt_f_dir=sys.argv[2]
ctrl_f_dir=sys.argv[3]
output_station_filename=sys.argv[4]

data_fs=os.listdir(data_f_dir)
ctrl_fs=os.listdir(ctrl_f_dir)

data_file_header_byte_count=0
ctrl_file_header_byte_count=0
mgmt_file_header_byte_count=0
file_counter=0
file_timestamp=0
filename_list=[]
unix_time=set()
for data_f_n in data_fs :
    filename_list.append(data_f_n.split('-'))
    unix_time.add(int(data_f_n.split('-')[1]))
    if not (data_f_n.split('-')[2]=='d'):
        print "its not a data file ; skip "
        continue 

filename_list.sort(key=lambda x : int(x[3]))
filename_list.sort(key=lambda x : int(x[1]))

for data_f_name_list in filename_list : #data_fs :    
    data_f_name="-".join(data_f_name_list)
    data_f= gzip.open(data_f_dir+data_f_name,'rb')
    data_file_content=data_f.read()
    data_f.close()
    data_file_current_timestamp=0
    data_file_seq_n=0
    bismark_id_data_file=0
    start_64_timestamp_data_file=0
    for i in xrange(len(data_file_content )):
        if data_file_content[i]=='\n':
            bismark_data_file_header = str(data_file_content[0:i])
            ents= bismark_data_file_header.split(' ')
            bismark_id_data_file=ents[0]
            start_64_timestamp_data_file= int(ents[1])
            data_file_seq_no= int(ents[2])
            data_file_current_timestamp=int(ents[3])
            data_file_header_byte_count =i
            break

    data_contents=data_file_content.split('\n----\n')
    header_and_correct_data_frames = data_contents[0]
    err_data_frames = data_contents[1]
    correct_data_frames_missed=data_contents[2]
    err_data_frames_missed=data_contents[3]

    ctrl_f_name = data_f_name
    ctrl_f_name =re.sub("-d-","-c-",ctrl_f_name)

    try :
        ctrl_f= gzip.open(ctrl_f_dir+ctrl_f_name,'rb')	
        ctrl_file_content=ctrl_f.read()
    except :
        print  "CTRL file not present ", ctrl_f_name 
        missing_files.append([ctrl_f_name,data_file_current_timestamp])
        continue 
    ctrl_f.close()
    
    
    mgmt_f_name = data_f_name
    mgmt_f_name = re.sub("-d-","-m-",mgmt_f_name)
    try : 
        mgmt_f= gzip.open(mgmt_f_dir+mgmt_f_name,'rb')
        mgmt_file_content=mgmt_f.read()
    except :
        print "MGMT file not present ",mgmt_f_name 
        missing_files.append([mgmt_f_name,data_file_current_timestamp])
        continue 

    mgmt_f.close()

    mgmt_file_current_timestamp=0
    mgmt_file_seq_no=0
    bismark_id_mgmt_file=0
    start_64_timestamp_mgmt_file=0
	
    ctrl_file_current_timestamp=0
    ctrl_file_seq_no=0
    bismark_id_ctrl_file=0
    start_64_timestamp_ctrl_file=0

    for i in xrange(len(mgmt_file_content )):
        if mgmt_file_content[i]=='\n':
            bismark_mgmt_file_header = str(mgmt_file_content[0:i])
            ents= bismark_mgmt_file_header.split(' ')
            bismark_id_mgmt_file=ents[0]
            start_64_timestamp_mgmt_file=int(ents[1])
            mgmt_file_seq_no= int(ents[2])
            mgmt_file_current_timestamp= int(ents[3])
            mgmt_file_header_byte_count =i
            break
    mgmt_contents=mgmt_file_content.split('\n----\n')
    header_and_beacon_mgmt_frames = mgmt_contents[0] 
    common_mgmt_frames = mgmt_contents[1]
    err_mgmt_frames=mgmt_contents[2]
    beacon_mgmt_frames_missed=mgmt_contents[3]
    common_mgmt_frames_missed=mgmt_contents[4]
    err_mgmt_frames_missed=mgmt_contents[5]

    for i in xrange(len(ctrl_file_content )):
        if ctrl_file_content[i]=='\n':
            bismark_ctrl_file_header = str(ctrl_file_content[0:i])
            ents= bismark_ctrl_file_header.split(' ')
            bismark_id_ctrl_file= ents[0]
            start_64_timestamp_ctrl_file= int(ents[1])
            ctrl_file_seq_no= int(ents[2])
            ctrl_file_current_timestamp=int(ents[3])
            ctrl_file_header_byte_count =i
            break
    ctrl_contents=ctrl_file_content.split('\n----\n')
    header_and_correct_ctrl_frames = ctrl_contents[0]
    err_ctrl_frames = ctrl_contents[1]
    correct_ctrl_frames_missed=ctrl_contents[2]
    err_ctrl_frames_missed=ctrl_contents[3]
    #done with reading the binary blobs from file ; now check for timestamps are correct
    if (not (ctrl_file_current_timestamp == mgmt_file_current_timestamp == data_file_current_timestamp )) :
        print "timestamps don't match " 		
        sys.exit(1)
    else :
        file_timestamp=ctrl_file_current_timestamp	
    if (not (ctrl_file_seq_no == mgmt_file_seq_no == data_file_seq_no)):
        print "sequence number don't match "
        sys.exit(1)

	
    if (len(ctrl_contents) != 4 or  len(data_contents) != 4 or len(mgmt_contents) !=6) :
        print "for ctrl " ,len (ctrl_contents) ,"for data", len(data_contents), "for mgmt", len(mgmt_contents) 
        print "file is malformed or the order of input folders is wrong "
        continue 
    
    if  (data_file_current_timestamp < t1-1):
        continue 


    if (data_file_current_timestamp >t2-1):
        break 
    print t1, data_file_current_timestamp, t2
    
        #The following code block parses the data file 	
	#print "----------done with missed .. now with actual data "
    correct_data_frames=header_and_correct_data_frames[data_file_header_byte_count+1:]
    data_index=0
    for idx in xrange(0,len(correct_data_frames)-DATA_STRUCT_SIZE ,DATA_STRUCT_SIZE ):	
        global file_timestamp
        frame=correct_data_frames[data_index:data_index+DATA_STRUCT_SIZE]
        offset,success,tsf= 8,-1,0
        header = frame[:offset]
        frame_elem=defaultdict(list)
        monitor_elem=defaultdict(list)        
        (version,pad,radiotap_len,present_flag)=struct.unpack('<BBHI',header)
        (success,frame_elem,monitor_elem)=parse_radiotap(frame,radiotap_len,present_flag,offset,monitor_elem,frame_elem)       
        if success:
            for key in frame_elem.keys():
                tsf=key                                    
            parse_data_frame(frame,radiotap_len,frame_elem)
            temp=frame_elem[tsf]
            temp.insert(0,tsf)
            if radiotap_len == 58 :
                rx_time_series.append(temp)                
            elif radiotap_len ==42 :
                tx_time_series.append(temp)
            else :
                print "impossible radiotap len detected ; Report CERN" 
            
        else:
            print "success denied; correct data frame"                    
        data_index=data_index+DATA_STRUCT_SIZE
        del frame_elem
        del monitor_elem
    '''
    data_index=0
    for idx in xrange(0,len(err_data_frames)-DATA_ERR_STRUCT_SIZE,DATA_ERR_STRUCT_SIZE ):	
        frame=err_data_frames[data_index:data_index+DATA_ERR_STRUCT_SIZE]
        offset,success,tsf= 8,-1,0
        header = frame[:offset]
        frame_elem=defaultdict(list)
        monitor_elem=defaultdict(list)
        (version,pad,radiotap_len,present_flag)=struct.unpack('<BBHI',header)
        (success,frame_elem,monitor_elem)=parse_radiotap(frame,radiotap_len,present_flag,offset,monitor_elem,frame_elem)
        if success:
            for key in frame_elem.keys():
                tsf=key
            parse_err_data_frame(frame,radiotap_len,frame_elem)
            temp=frame_elem[tsf]
            temp.insert(0,tsf)
            if radiotap_len == 58 :                
                rx_time_series.append(temp)
            elif radiotap_len ==42 :
                print "342"
                tx_time_series.append(temp)
            else :
                print "impossible radiotap len detected ; Report CERN" 
            
        else :
            print "success denied; incorrect data frame" 
                   
        data_index= data_index+DATA_ERR_STRUCT_SIZE
        del frame_elem
        del monitor_elem
        '''

    #The following code block parses the mgmt files 
    '''
    beacon_mgmt_frames=header_and_beacon_mgmt_frames[mgmt_file_header_byte_count+1:]
    mgmt_index=0
    for idx in xrange(0,len(beacon_mgmt_frames)-MGMT_BEACON_STRUCT_SIZE ,MGMT_BEACON_STRUCT_SIZE ):
        global file_timestamp
        frame=beacon_mgmt_frames[mgmt_index:mgmt_index+MGMT_BEACON_STRUCT_SIZE]
        offset,success,tsf= 8,-1,0
        header = frame[:offset]
        frame_elem,monitor_elem=defaultdict(list),defaultdict(list)
        (version,pad,radiotap_len,present_flag)=struct.unpack('<BBHI',header)
        if not( radiotap_len ==58 or  radiotap_len == 42) :
            print "the radiotap header is not correct "
            sys.exit(1)
        (success,frame_elem,monitor_elem)=parse_radiotap(frame,radiotap_len,present_flag,offset,monitor_elem,frame_elem)
        if success :
            for key in frame_elem.keys():
                tsf=key
            Frame_count[file_timestamp][1][0] = Frame_count[file_timestamp][1][0] + 1
            if len(monitor_elem)>0:
                Monitor[file_timestamp].append(monitor_elem[tsf][0])
                Physical_errs[file_timestamp].append([tsf,monitor_elem[tsf]])
            parse_mgmt_beacon_frame(frame,radiotap_len,frame_elem)
            if radiotap_len== 58:
                frame_elem[tsf].insert(0,tsf)
                temp={}
                temp[file_timestamp]=frame_elem[tsf]
                Access_point[frame_elem[tsf][12]]=temp
        else :
            print "success denied"
        mgmt_index=mgmt_index+MGMT_BEACON_STRUCT_SIZE
        del frame_elem
        del monitor_elem

    mgmt_index=0
    for idx in xrange(0,len(err_mgmt_frames)-MGMT_ERR_STRUCT_SIZE,MGMT_ERR_STRUCT_SIZE ):
        global file_timestamp
        frame=err_mgmt_frames[mgmt_index:mgmt_index+MGMT_ERR_STRUCT_SIZE]
        offset,success,tsf= 8,-1,0
        header = frame[:offset]
        frame_elem,monitor_elem=defaultdict(list),defaultdict(list)
        (version,pad,radiotap_len,present_flag)=struct.unpack('<BBHI',header)
        if not( radiotap_len ==58 or  radiotap_len == 42) :
            print "the radiotap header is not correct "
            sys.exit(1)
        (success,frame_elem,monitor_elem)=parse_radiotap(frame,radiotap_len,present_flag,offset,monitor_elem,frame_elem)
        if success==1 :
            for key in frame_elem.keys():
                tsf=key
            parse_mgmt_err_frame(frame,radiotap_len,frame_elem)                                                                                            
            temp=frame_elem[tsf]
            temp.insert(0,tsf)
            time_series.append(temp)
        else:
            print "success denied"
        mgmt_index= mgmt_index+MGMT_ERR_STRUCT_SIZE
        del frame_elem
        del monitor_elem


    #print "----------done with missed .. now with actual ctrl data "

    correct_ctrl_frames=header_and_correct_ctrl_frames[ctrl_file_header_byte_count+1:]
    ctrl_index=0
    for idx in xrange(0,len(correct_ctrl_frames)-CTRL_STRUCT_SIZE ,CTRL_STRUCT_SIZE ):			
        global file_timestamp
        frame=correct_ctrl_frames[ctrl_index:ctrl_index+CTRL_STRUCT_SIZE]
        offset,success,tsf= 8,-1,0
        header = frame[:offset]
        frame_elem, monitor_elem=defaultdict(list),defaultdict(list)
        (version,pad,radiotap_len,present_flag)=struct.unpack('<BBHI',header)
        if not( radiotap_len ==58 or  radiotap_len == 42) :
            print "the radiotap header is not correct "		
            sys.exit(1)
        (success,frame_elem,monitor_elem)=parse_radiotap(frame,radiotap_len,present_flag,offset,monitor_elem,frame_elem)
        if success :
            for key in frame_elem.keys():
                tsf=key
            parse_ctrl_frame(frame,radiotap_len,frame_elem)
            temp=frame_elem[tsf]
            temp.insert(0,tsf)
            if radiotap_len == 58 :
                rx_time_series.append(temp)
            elif radiotap_len ==42 :
                tx_time_series.append(temp)

        else :
            print "success denied"
        ctrl_index=ctrl_index+CTRL_STRUCT_SIZE
        del frame_elem
        del monitor_elem                    

    ctrl_index=0
    for idx in xrange(0,len(err_ctrl_frames)-CTRL_ERR_STRUCT_SIZE,CTRL_ERR_STRUCT_SIZE):			
        global file_timestamp
        frame=err_ctrl_frames[ctrl_index:ctrl_index+CTRL_ERR_STRUCT_SIZE]
        offset,success,tsf= 8,-1,0
        header = frame[:offset]
        frame_elem,monitor_elem=defaultdict(list),defaultdict(list)
        (version,pad,radiotap_len,present_flag)=struct.unpack('<BBHI',header)
        if not( radiotap_len ==58 or  radiotap_len == 42) :	
            print "the radiotap header is not correct "		
            sys.exit(1)
        (success,frame_elem,monitor_elem)=parse_radiotap(frame,radiotap_len,present_flag,offset,monitor_elem,frame_elem)
        if success ==1:
            for key in frame_elem.keys():
                tsf=key
            parse_ctrl_err_frame(frame,radiotap_len,frame_elem)
            temp=frame_elem[tsf]
            temp.insert(0,tsf)
            if radiotap_len == 58 :
                rx_time_series.append(temp)
            elif radiotap_len ==42 :
                tx_time_series.append(temp)
        else :
            print "success denied"
        ctrl_index= ctrl_index+CTRL_ERR_STRUCT_SIZE
        del frame_elem
        del monitor_elem
        '''
    file_counter +=1
    if file_counter %10 == 0:
        print file_counter


print "now processing the files to calculate time "
rx_time_series.sort(key=lambda x:x[0])
tx_time_series.sort(key=lambda x:x[0])

Station_list=list(Station)
Station_tx_retx_count = defaultdict(list)
print Station_list

print "in tx looping "

Station_tx_series=defaultdict(list)
for j in range(0,len(Station_list)):
    frame_count = 0 
    retransmission_count =0
    for i in range(0,len(tx_time_series)):
        frame = tx_time_series[i]
        if frame[8]==Station_list[j] :            
            prop_time=(frame[-1]*8.0 *1000000)/ (frame[3] *1000000)
            Station_tx_series[frame[8]].append([frame[0],frame[1],frame[2],frame[3],frame[4],frame[5],frame[6],frame[9],frame[10],frame[-1],prop_time]) 
            #time [0],flags[1],retx[2],success_rate[3],total_time[4],contention time[5],retx_list[6],seq no[9],fragment no[10],framesize[-1],prop time 
            frame_count =frame_count +1 
            retx_count =0
            if int(frame[2]) -1 <0  :
                retx_count =0
            else :
                retx_count =int (frame[2]) -1
            retransmission_count = retransmission_count + retx_count 

    Station_tx_retx_count[Station_list[j]].append([retransmission_count, frame_count])

Station_tx_retx_succ_delay=defaultdict(list)
Station_tx_cont_succ_delay=defaultdict(list)
Station_tx_overall_succ_delay=[]

Station_tx_retx_contention_delay=defaultdict(list)
Station_tx_cont_contention_delay=defaultdict(list)
Station_tx_overall_contention_delay=[]
co=0
for j in Station_tx_series.keys():
    #j is the station name 
    list_of_frames= Station_tx_series[j]
    for i in range(1,len(list_of_frames)):        
        frame=list_of_frames[i]
        previous_frame=list_of_frames[i-1]
        #frame time[0],frame_flags[1],retx[2],success_rate[3],total time[4],retx_list[5],contentn time[5],seq no [9], fragment no[10], framesize[-1],prop time 
        #[time,retx,rate,total time,contention time, retx_list,sequence no, fragment no, framesize, prop time ]
        delay = -1
        if int(frame[2]) -1 <0  :
            c_frame_departure=frame[0]
            p_frame_departure=previous_frame[0]    
            c_frame_contention_time =frame[5]
            p_frame_contention_time=previous_frame[5]
            c_frame_total_time=frame[4]
            p_frame_total_time=previous_frame[4]
            c_frame_seq_no=frame[7]            
            p_frame_seq_no=previous_frame[7]
            c_frame_size= frame[-2]
            p_frame_size= previous_frame[-2]
            if ((c_frame_seq_no - p_frame_seq_no)<2) and c_frame_size >1300 and p_frame_size > 1300:
                if c_frame_departure - p_frame_departure == 0 :
                    delay = -0.1
                    print "n",c_frame_departure
                    print "how is it 00-1"
                else :
                    delay=(c_frame_departure)- p_frame_departure
                    if delay <0 :
                        print frame 
                        print previous_frame
                        print "negatve delay for cont frames "
                        sys.exit(1)
                    Station_tx_cont_succ_delay[j].append(delay)            
                    Station_tx_overall_succ_delay.append(delay)

            if c_frame_contention_time < c_frame_total_time :
                Station_tx_cont_contention_delay[j].append(c_frame_contention_time)
                Station_tx_overall_contention_delay.append(c_frame_contention_time)

        elif int(frame[2]) -1 > 0 :   
            c_frame_departure=frame[0]
            p_frame_departure=previous_frame[0]            
            c_frame_contention_time =frame[5]
            p_frame_contention_time=previous_frame[5]
            c_frame_total_time=frame[4]
            p_frame_total_time=previous_frame[4]
            c_frame_seq_no=frame[7]            
            p_frame_seq_no=previous_frame[7]
            c_frame_size= frame[-2]
            p_frame_size= previous_frame[-2]
            if not ((c_frame_seq_no - p_frame_seq_no)>3) :
                if c_frame_departure - p_frame_departure == 0 :
                    global co 
                    co=co+1
                    #print "c",j, frame[0],frame[1],frame[2],frame[6],c_frame_seq_no,c_frame_total_time,c_frame_contention_time, frame[-2],frame[1]
                    #print "p",j, previous_frame[0],previous_frame[1],previous_frame[2],previous_frame[6], p_frame_seq_no,p_frame_total_time, p_frame_contention_time,frame[-2],frame[1]
                    delay = 0.0
                    #print "how is it 000 !!! " 
                else :
                    delay=(c_frame_departure)- p_frame_departure
                    if delay <0 :
                        print "fucking negative delay for retx frames "
                        sys.exit(1)
                    Station_tx_retx_succ_delay[j].append(delay)
                    Station_tx_overall_succ_delay.append(delay)

            if c_frame_contention_time < c_frame_total_time :
                Station_tx_retx_contention_delay[j].append(c_frame_contention_time)
                Station_tx_overall_contention_delay.append(c_frame_contention_time)

print "retx count " 
print Station_tx_retx_count
overall_retx =0
overall_frame_count =0
for i in Station_tx_retx_count.keys() :
    l_c_list= Station_tx_retx_count[i]
    overall_retx = overall_retx +l_c_list[0][0]
    overall_frame_count = overall_frame_count +l_c_list[0][1] 
print overall_retx, overall_frame_count 
print overall_retx*1.0/overall_frame_count 

print "Contention: tx cont delay"
for station in Station_tx_cont_contention_delay :    
    print station, percentile(Station_tx_cont_contention_delay[station],50)
print "Contention :tx retx delay"
for station in Station_tx_retx_contention_delay :
    print station, percentile(Station_tx_retx_contention_delay[station],50)



print "Successive:  cont "
for station in Station_tx_cont_succ_delay :
    print station, percentile(Station_tx_cont_succ_delay[station],50)

print "Successive:  retx " 
for station in Station_tx_retx_succ_delay : 
    print station, percentile(Station_tx_retx_succ_delay[station],50)


print "Overall "
print "Contention:tx overall contention delay" 
print percentile(Station_tx_overall_contention_delay,50)
print "Contention:tx overall successive frame delay"
print percentile(Station_tx_overall_succ_delay,50)


sys.exit(1)
'''
print "in rx_looping "


Station_rx_series=defaultdict(list)

Station_rx_retx_frames=defaultdict(list)
Station_rx_cont_frames=defaultdict(list)
print "RECIVED FRAMES "
for i in range(0,len(rx_time_series)):
    frame = rx_time_series[i]
    for i in range(0,len(Station_list)):
        if frame[12]==Station_list[i] :
            prop_time=(frame[10]*8.0 *1000000)/ (frame[8] *1000000)
            Station_rx_series[frame[12]].append([frame[0],frame[8],frame[10],frame[11],frame[14],frame[15],frame[16][1],prop_time]) 
            #print frame[12],frame[0],frame[8],frame[10],frame[11],frame[14],frame[15],frame[16][1],prop_time
            #time [0], success rate [8], framesize [10], RSSI [11], seq number [14], fragment no [15],retry frame [16][1],prop time 
            #print frame ,prop_time , frame[16][0]
            #print frame[0],frame[1],1,frame[8],frame[14],frame[15],frame[-1]

for j in Station_rx_series.keys():
    list_of_frames= Station_rx_series[j]
    for i in range(1,len(list_of_frames)):
        frame= list_of_frames[i]
        print frame

Overall_retx_delay=[]
Overall_cont_delay=[]
print "generating rx stats " 
for j in Station_rx_series.keys():
    #j is the station name 
    list_of_frames= Station_rx_series[j]
    for i in range(1,len(list_of_frames)):
        frame= list_of_frames[i]
        previous_frame= list_of_frames[i-1]
        current_frame_arrival=frame[0]
        previous_frame_arrival=previous_frame[0]            
        c_frame_seq_no = frame[] 
        p_frame_seq_no = previous_frame[]
        c_frame_prop_time = frame[-1]
        delay = -1 
        if frame[-2] == 1 : #means retransmitted 
            if ((c_frame_seq_no - p_frame_seq_no)<6) :
                if current_frame_arrival - previous_frame_arrival == 0 : 
                    delay = 0.0
                else :
                    delay=current_frame_departure-c_frame_prop_time - previous_frame_arrival
                    if delay <0 :
                        print "negatve delay for cont frames "
                        sys.exit(1)
                    Station_rx_overall_delay.append(delay)
        else :
            if current_frame_arrival - previous_frame_arrival == 0 :
                delay = 0.0
            else :
                delay=(current_frame_arrival-frame[-1])- previous_frame_arrival            
            Station_rx_cont_frames[j].append(delay)
            Overall_cont_delay.append(delay)
               
#print Station_rx_retx_frames
print "for Devices \nfor cont frames" 
for i in Station_tx_cont_frames.keys():
    print i 
    if len(Station_tx_cont_frames[i]) >1 :
        print avg(Station_tx_cont_frames[i]), variance(Station_tx_cont_frames[i]), percentile(Station_tx_cont_frames[i],90 )
    print 
print "for retx frames" 
for i in Station_tx_retx_frames.keys():
    print i
    if len(Station_tx_retx_frames[i]) >1 :
        print avg(Station_tx_retx_frames[i] ), variance(Station_tx_retx_frames[i]), percentile(Station_tx_retx_frames[i],90)
    else :
        print "no elem in tx_retx"
    print 

print "Overall delays" 
print "for retx overall delay " 
if len(Overall_retx_delay)>0:
    print avg(Overall_retx_delay), variance(Overall_retx_delay), percentile(Overall_retx_delay,90)
print "for continuous overall delays "
if len(Overall_cont_delay)>0:
    print avg(Overall_cont_delay), variance(Overall_cont_delay), percentile(Overall_cont_delay,90)
print 
print "Accumulating all delay " 
if len(Overall_delay)>0:
    print avg(Overall_delay), variance(Overall_delay), percentile(Overall_delay,90)


sys.exit(1)
f_n= output_station_filename
output_noise = open(f_n, 'wb')
pickle.dump( noise_map,output_noise )
output_noise.close()
print "done with print the keys "

for i in range(0,len(missing_files)):
	print missing_files[i]
print "number of files that can't be located ", len(missing_files)	
'''

