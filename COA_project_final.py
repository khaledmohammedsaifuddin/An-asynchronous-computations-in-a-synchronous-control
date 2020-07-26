#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 13:52:28 2020

@author: illusionist
"""

from random import seed
from random import randint
import math
import matplotlib.pyplot as plt

def Problem_1():
    total_time=-1
    n=-1
    
    while total_time < 0:
        total_time=int(input('Please provide the time for which you want to run the system.  '))
        if total_time<=0:
            print('Please provide a positive time.')
        else: 
            break
        
    while n < 0:
        n=int(input('Please provide the capacity of main block(n)  '))
        if n<=0:
            print('Please provide a positive block size')
        else:
            break
    interval=n
    seed(10)
    sum_of_arrived_slots=0
    no_of_slots_in_secondary_block=0
    sum_of_probability=0
    minimum=0
    medium=0
    maximum=0
    m=0
    system_time=0
    queuing_time_from_secondary_block=0
    arrival_time=0
    service_event=0
    service_time=0
    m_activated=False
    arrival={}
    service ={}
    secondary={}
    slots_queued_from_secondary_block={}
    slots_arrived_naturally={}
    probability_i={}
    arrival_event_prob={}
    service_event_prob={}
    queuing_event_prob={}
    count_of_slots_being_serviced={}
    float_m=0
    first_fraction=0
    second_fraction=0

    for z in range(0,n+1):
    # all these dictionaries are used for probability calculation
    # arrival, service, queueing event probability dictionaries store probabilities of
    # i-th slot in main block in case of each event
    # probability dictionary sums up each i-th slot's cummulative probability for all events
    # slots_queued_from_secondary_block keeps track of number of times i-th slot has been
    # queued from secondary block to main block
    # slots_arrived_naturally array keeps track of number of times i-th slot has been queued
    # into main block through natural arrival
        probability_i[z]=0
        arrival_event_prob[z]=0
        service_event_prob[z]=0
        queuing_event_prob[z]=0
        slots_queued_from_secondary_block[z]=0
        slots_arrived_naturally[z]=0

    for i in range(1,1001):
        # service and secondary dictionaries are used when the system is running
        # service dictionary stores the number of slots in main block at a given time
        # secondary dictionary stores the number of slots in secondary block at a given time
        service[i]=0
        secondary[i]=0
        arrival[i]=0
        #arrival.append(randint(1,10))
        
    
    for i in range(1,total_time+1):
        # arrival dictionary is used to store arrived slots to the system in each second
        # slots queued from secondary block dictionary is used to keep track of the number of times
        # i(1,2,3...n) number of slots have been queued from secondary block to first block
        # slots arrived naturally dictionary is used to keep track of the number of time i-th slot
        # have been queued into main block nautrally, not from secondary block
        arrival[i]=randint(1,n)
        

    for i in range(1,total_time+1):
        #sum of arrived_slots dictionary calculates total arrived slots
        sum_of_arrived_slots=sum_of_arrived_slots+arrival[i]

    # arrival rate and service rate specifies arrival rate of slots and service rate at which slots are processed
    pending_slots=sum_of_arrived_slots
    arrivalrate=sum_of_arrived_slots/total_time
    servicerate=int(arrivalrate)+1
    
    for i in range(1,total_time+1):
        
        if m> total_time and no_of_slots_in_secondary_block<n:
            break

        lstinterval=interval

        # m_activated boolean variable is used to check whether slots have started coming from secondary block
        # if the value is set false, slots are coming naturally
        # if the value is set true, slots have started coming from secondary block
        # interval variable keeps track of how many slots can be further queued into main block
        # suppose, main block has n capacity and already has i slots.
        # so, value of interval will be n-i
        # if interval's value is less than 0, it means slots will be queued into secondary block
        if no_of_slots_in_secondary_block==0:
            if m_activated==False:
                interval=interval-arrival[i]
            elif m_activated==True and m<=total_time:
                interval=interval-arrival[m]
        else:
            interval=interval-no_of_slots_in_secondary_block

        # keeping track of slot no. of blocks which have been filled up
        if interval>=0:
            for x in range(interval, lstinterval):
                slots_arrived_naturally[n-x]+=1
        
        if interval>0:
            #service.append(arrival[i])
            service[i]=arrival[i]
        elif interval<=0:

            if lstinterval !=0:
                #service.append(lstinterval)
                #arrival[i]=arrival[i]-lstinterval

                # if interval's value is less than or equal to 0, then main block has
                # n slots. main block will start processing batch of n slots.
                # this block calculates how many slots can be queued into secondary block
                # no_of_slots_in_secondary_block calculates the number of slots in secondary block
                if m_activated==False:
                    no_of_slots_in_secondary_block=arrival[i]-lstinterval
                elif m_activated==True and m<=total_time:
                    no_of_slots_in_secondary_block=arrival[m]-lstinterval

                # keeping track of slot no. of blocks which have been filled up
                if interval<0:
                    for x in range(1, lstinterval+1):
                        slots_arrived_naturally[n-x+1]+=1
                interval=0


            #main block has n slots. this block calculates the timeframe within which
            #service will be provided to batch of n slots.
            if m_activated==False:
                starting_index=i
                #if i+math.ceil(n/servicerate)>=total_time:
                #    m=total_time
                #else:
                float_m = i+(n/servicerate)
                m=math.ceil(float_m)
            elif m_activated==True:
                starting_index=m
                if m+math.ceil(n/servicerate)>=total_time:
                    m=total_time
                else:
                    float_m = m+(n/servicerate)
                    m=math.ceil(float_m)
            
            ending_index=m
            
            # sometimes servicing of slots take fraction of seconds, i.e. 5.2/2.3 secs to complete. 
            # so, we have to keep track of exactly how much time it takes for main block to process
            # slots. For example, if servicing of slots take 5.2 secs, we should queue slots arrived
            # in 0.2 sec of 6th sec in secondary block. slots arrived in remaining 0.8 second should
            # be queued into main block.
            
            if (float_m%1)!=0:
                if m+1<= total_time:

                    # we consider the case for arrival of slots is going on and still hasn't reached 
                    # the end of slot arrival. we modify the arrived slots' array considering the fact
                    # that servicing of slots requires a float value of time. before last seconds, all
                    # arrived slots will be queued into secondary block. during the last sec, we take
                    # fraction value. if servicing time is 5.2 sec, we take 0.2 sec which is fraction
                    # value. let's assume that this second is i. we obtain arrived slots in i-th sec from
                    # arrived slots' array. we calculate how many slots may arrive in 0.2/20% of i-th sec.
                    # the reason for doing this is only this amount of slots will be slots will be queued
                    # into secondary value during this float value of time. this will allow us to manage 
                    # arrival of slots more efficiently. the remainder of arrived slots' array will be
                    # modified as follows- according to the example, remaining time of i-th second is 0.8s.
                    # we calculate arrived slots from 0.8/80% of i-th second and 0.2/20% of (i+1)-th second
                    # we add these 2 values and consider this to be number of arrived slots at (i+1)-th second 
                    first_fraction = float_m%1
                    second_fraction = 1-first_fraction

                    temp = arrival[m]
                    arrival[m] = math.floor(first_fraction* arrival[m])
                    for x in range(m+1, total_time+1):
                        temp2=arrival[x]
                        value = math.ceil(second_fraction*temp) + math.floor(first_fraction*temp2)
                        temp=arrival[x]
                        arrival[x]=value

                    arrival[total_time+1]=math.ceil(second_fraction*temp)
                    total_time+=1

                elif arrival[m]>0:
                    # we consider the case when arrival of slots has almost reached the end of slot arrival. 
                    # after a service of slots' event, only the last second of arrived slots is pending. 
                    # in this case, we modify the last elemnt of arrived slots' array we consider the fact 
                    # that servicing of slots requires a float value of time. if servicing time is 5.2 sec, 
                    # we take 0.2 sec which is fraction value. let's assume that this second is i, which is 
                    # last second for slot arrival. we obtain arrived slots in i-th sec from arrived slots' 
                    # array. we calculate how many slots may arrive in 0.2/20% of i-th sec. this value is 
                    # the number of slots arrived at i-th second. remaining time of i-th second is 0.8s. 
                    # we calculate arrived slots from 0.8/80% of i-th second and and consider this to be 
                    # number of arrived slots at (i+1)-th second.
                    total_time+=1
                    first_fraction = float_m%1
                    second_fraction = 1-first_fraction

                    temp = arrival[m]
                    arrival[m] = math.floor(first_fraction* arrival[m])
                    arrival[total_time]=math.ceil(second_fraction*temp)


            while True:
                # for loop shows the code of main block processing n slots.
                # in the meantime, secondary block stores arrived slots while
                # main block is busy processing n slots
                for j in range(starting_index+1,ending_index+1):
                    #secondary.append(arrival[j])
                    service[j]=0
                    if j<=total_time:
                        no_of_slots_in_secondary_block+=arrival[j]
                    #secondary[i]=arrival[j]
                service_event+=1
                m=m+1

                # processing is over. if secondary block has less than or equal to n slots, all
                # slots will be queued into main block. it will assumed that this transfer takes 1 sec
                if no_of_slots_in_secondary_block<n:
                    service[m]=no_of_slots_in_secondary_block
                    interval=n-service[m]
                    slots_queued_from_secondary_block[no_of_slots_in_secondary_block]+=1
                    no_of_slots_in_secondary_block=0

                    if interval==0:
                        m+=1
                        service[m]=n
                        no_of_slots_in_secondary_block -= n
                        slots_queued_from_secondary_block[n]+=1
                        starting_index=m
                        float_m = m+(n/servicerate)
                        m=math.ceil(float_m)
                        ending_index=m
                        
                        # we consider the case for arrival of slots is going on and still hasn't reached 
                        # the end of slot arrival. we modify the arrived slots' array considering the fact
                        # that servicing of slots requires a float value of time. before last seconds, all
                        # arrived slots will be queued into secondary block. during the last sec, we take
                        # fraction value. if servicing time is 5.2 sec, we take 0.2 sec which is fraction
                        # value. let's assume that this second is i. we obtain arrived slots in i-th sec from
                        # arrived slots' array. we calculate how many slots may arrive in 0.2/20% of i-th sec.
                        # the reason for doing this is only this amount of slots will be slots will be queued
                        # into secondary value during this float value of time. this will allow us to manage 
                        # arrival of slots more efficiently. the remainder of arrived slots' array will be
                        # modified as follows- according to the example, remaining time of i-th second is 0.8s.
                        # we calculate arrived slots from 0.8/80% of i-th second and 0.2/20% of (i+1)-th second
                        # we add these 2 values and consider this to be number of arrived slots at (i+1)-th second
                        
                        if (float_m%1)!=0:
                            if m+1<=total_time:
                                # we consider the case for arrival of slots is going on and still hasn't 
                                # reached the end of slot arrival. we modify the arrived slots' array 
                                # considering the fact that servicing of slots requires a float value of time.
                                # before last seconds, all arrived slots will be queued into secondary block. 
                                # during the last sec, we take fraction value. if servicing time is 5.2 sec, 
                                # we take 0.2 sec which is fraction value. let's assume that this second is i.
                                # we obtain arrived slots in i-th sec from arrived slots' array. we calculate 
                                # how many slots may arrive in 0.2/20% of i-th sec. the reason for doing this
                                # is only this amount of slots will be slots will be queued into secondary 
                                # value during this float value of time. this will allow us to manage 
                                # arrival of slots more efficiently. the remainder of arrived slots' array 
                                # will be modified as follows- according to the example, remaining time of 
                                # i-th second is 0.8s. we calculate arrived slots from 0.8/80% of i-th second 
                                # and 0.2/20% of (i+1)-th second we add these 2 values and consider this to be
                                # number of arrived slots at (i+1)-th second
                                first_fraction = float_m%1
                                second_fraction = 1-first_fraction

                                temp = arrival[m]
                                arrival[m] = math.floor(first_fraction* arrival[m+1])
                                for x in range(m+1, total_time+1):
                                    temp2=arrival[x]
                                    value = math.ceil(second_fraction*temp) + math.floor(first_fraction*temp2)
                                    temp=arrival[x]
                                    arrival[x]=value

                                arrival[total_time+1]=math.ceil(second_fraction*temp)
                                total_time+=1
                            elif arrival[m]>0:
                                # we consider the case when arrival of slots has almost reached the end of slot
                                # arrival. after a service of slots' event, only the last second of arrived 
                                # slots is pending. in this case, we modify the last elemnt of arrived slots' 
                                # array we consider the fact that servicing of slots requires a float value of
                                # time. if servicing time is 5.2 sec, we take 0.2 sec which is fraction value.
                                # let's assume that this second is i, which is last second for slot arrival. 
                                # we obtain arrived slots in i-th sec from arrived slots' array. we calculate 
                                # how many slots may arrive in 0.2/20% of i-th sec. this value is the number 
                                # of slots arrived at i-th second. remaining time of i-th second is 0.8s. 
                                # we calculate arrived slots from 0.8/80% of i-th second and and consider this
                                # to be number of arrived slots at (i+1)-th second.
                                total_time+=1
                                first_fraction = float_m%1
                                second_fraction = 1-first_fraction

                                temp = arrival[m]
                                arrival[m] = math.floor(first_fraction* arrival[m])
                                arrival[total_time]=math.ceil(second_fraction*temp)
                elif no_of_slots_in_secondary_block>=n:
                    # if secondary block has more than n slots, only n slots will be queued into main
                    # block. since main block's capacity is n slots. during this slot transfer period,
                    # secondary slot will store arrived slots. since main block has n slots, it will process
                    # a batch of n slots again
                    service[m]=n
                    interval=0
                    no_of_slots_in_secondary_block -= n
                    slots_queued_from_secondary_block[n]+=1
                    if m<=total_time:
                        no_of_slots_in_secondary_block+=arrival[m]
                    starting_index=m
                    float_m = m+(n/servicerate)
                    m=math.ceil(float_m)
                    ending_index=m
                    
                    if (float_m%1)!=0: 
                        if m+1<=total_time:
                            first_fraction = float_m%1
                            second_fraction = 1-first_fraction

                            temp = arrival[m]
                            arrival[m] = math.floor(first_fraction* arrival[m+1])
                            for x in range(m+1, total_time+1):
                                temp2=arrival[x]
                                value = math.ceil(second_fraction*temp) + math.floor(first_fraction*temp2)
                                temp=arrival[x]
                                arrival[x]=value

                            arrival[total_time+1]=math.ceil(second_fraction*temp)
                            total_time+=1
                        elif arrival[m]>0:
                            total_time+=1
                            first_fraction = float_m%1
                            second_fraction = 1-first_fraction

                            temp = arrival[m]
                            arrival[m] = math.floor(first_fraction* arrival[m])
                            arrival[total_time]=math.ceil(second_fraction*temp)

                m_activated=True
                if interval>0 or m>total_time:
                    break


    for i in range(0,n+1):
        #this block calculates the number of time slots have been queued into
        #main block naturally or secondary block
        queuing_time_from_secondary_block+=slots_queued_from_secondary_block[i]
        arrival_time+=slots_arrived_naturally[i]

    #using arrival rate and service rate, the time required for arrival and service events
    #main block processes all n slots at an equal service rate unlike arrival. so, number
    #of service events is taken into consideration for calculating n slots.
    arrival_time=arrival_time/arrivalrate
    service_time=(n+1)/servicerate
    service_time*=service_event
    system_time=arrival_time+service_time+queuing_time_from_secondary_block

    print('\ni slots probability values:')
    for p in range(0,n+1):
        #main block processes all n slots at an equal service rate unlike arrival. so, number
        #of service events is taken into consideration for calculating n slots. for service
        #events, all i slots are equiprobable. for all i slots, main block has same similarity
        #to have i slots during a service event

        #for arrival events, we have kept track of how many times each i-slot have been queued
        #into main block(natually/from secondary block) using 2 dictionaries. these are taken
        #into account while calculating probability of i-th slot in case of arrival events
        if arrival_time>0 and system_time>0:
            arrival_event_prob[p] = (arrival_time/system_time) * (slots_arrived_naturally[p]/(arrivalrate*arrival_time))
        if service_time>0 and system_time>0:
            service_event_prob[p] = (service_time/system_time) * (service_event/(servicerate*service_time))
        if queuing_time_from_secondary_block>0 and system_time>0:
            queuing_event_prob[p] = (queuing_time_from_secondary_block/system_time) * (slots_queued_from_secondary_block[p]/queuing_time_from_secondary_block)
        probability_i[p] = arrival_event_prob[p]+ service_event_prob[p] + queuing_event_prob[p]
        sum_of_probability+=probability_i[p]
        print('i=',p,'   P[i]=',probability_i[p])

    print('\nSum of n slots probability', sum_of_probability)

    #probability values are plotted in graph
    plt.plot(list(probability_i.values()))
    plt.show()



def Problem_2():
    total_time=-1
    n=-1
    while total_time<0:
        total_time=int(input('Please provide the time for which you want to run the system.  '))
        if total_time<=0:
            print('Please provide a positive time')
        else:
            break
    while n<0:
        n=int(input('Please provide the capacity of main block(n)  '))
        if n<=0:
            print('Please provide a positive block size')
        else:
            break
    interval=n
    sum_of_arrived_slots=0
    no_of_slots_in_secondary_block=0
    sum_of_probability=0
    minimum=0
    medium=0
    maximum=0
    m=0
    system_time=0
    queuing_time_from_secondary_block=0
    arrival_time=0
    service_event=0
    service_time=0
    n_count=1
    m_activated=False
    arrival={}
    service ={}
    secondary={}
    slots_queued_from_secondary_block={}
    slots_arrived_naturally={}
    probability_i={}
    final_probability_i={}
    arrival_event_prob={}
    service_event_prob={}
    queuing_event_prob={}
    count_of_slots_being_serviced={}
    values_of_n={}
    values_of_n[n_count]=n
    n_count+=1
    float_m=0
    first_fraction=0
    second_fraction=0
    max_value=n

    for z in range(0,1001):
    # all these dictionaries are used for probability calculation
    # arrival, service, queueing event probability dictionaries store probabilities of
    # i-th slot in main block in case of each event
    # probability dictionary sums up each i-th slot's cummulative probability for all events
    # service and secondary dictionaries are used when the system is running
    # service dictionary stores the number of slots in main block at a given time
    # secondary dictionary stores the number of slots in secondary block at a given time
    # slots_queued_from_secondary_block keeps track of number of times i-th slot has been
    # queued from secondary block to main block
    # slots_arrived_naturally array keeps track of number of times i-th slot has been queued
    # into main block through natural arrival
    # count_of_slots_being_serviced array keeps track of number of times i-th slots has been serviced
    # in the main block
        probability_i[z]=0
        arrival_event_prob[z]=0
        service_event_prob[z]=0
        queuing_event_prob[z]=0
        service[z]=0
        secondary[z]=0
        arrival[z]=0
        slots_queued_from_secondary_block[z]=0
        slots_arrived_naturally[z]=0
        count_of_slots_being_serviced[z]=0


    for i in range(1,total_time+1):
        # arrival dictionary is used to store arrived slots to the system in each second
        # slots queued from secondary block dictionary is used to keep track of the number of times
        # i(1,2,3...n) number of slots have been queued from secondary block to first block
        # slots arrived naturally dictionary is used to keep track of the number of time i-th slot
        # have been queued into main block nautrally, not from secondary block
        arrival[i]=randint(1,n)


    for i in range(1,total_time+1):
        # sum of arrived_slots dictionary calculates total arrived slots
        sum_of_arrived_slots=sum_of_arrived_slots+arrival[i]

    # arrival rate and service rate specifies arrival rate of slots and service rate at which slots are processed
    pending_slots=sum_of_arrived_slots
    arrivalrate=sum_of_arrived_slots/total_time
    servicerate=int(arrivalrate)+1

    for i in range(1,total_time+1):

        if m> total_time and no_of_slots_in_secondary_block<n:
            break
            
        lstinterval=interval

        # m_activated boolean variable is used to check whether slots have started coming from secondary block
        # if the value is set false, slots are coming naturally
        # if the value is set true, slots have started coming from secondary block
        # interval variable keeps track of how many slots can be further queued into main block
        # suppose, main block has n capacity and already has i slots.
        # so, value of interval will be n-i
        # if interval's value is less than 0, it means slots will be queued into secondary block
        if no_of_slots_in_secondary_block==0:
            if m_activated==False:
                interval=interval-arrival[i]
            elif m_activated==True and m<=total_time:
                interval=interval-arrival[m]
        else:
            interval=interval-no_of_slots_in_secondary_block

        # keeping track of slot no. of blocks which have been filled up
        if interval>=0:
            for x in range(interval, lstinterval):
                slots_arrived_naturally[n-x]+=1
                service[i]=arrival[i]
        if interval>0:
            #service.append(arrival[i])
            service[i]=arrival[i]
        elif interval<=0:

            if lstinterval !=0:
                #service.append(lstinterval)
                #arrival[i]=arrival[i]-lstinterval

                # if interval's value is less than or equal to 0, then main block has
                # n slots. main block will start processing batch of n slots.
                # this block calculates how many slots can be queued into secondary block
                # no_of_slots_in_secondary_block calculates the number of slots in secondary block
                if m_activated==False:
                    no_of_slots_in_secondary_block=arrival[i]-lstinterval
                elif m_activated==True and m<=total_time:
                    no_of_slots_in_secondary_block=arrival[m]-lstinterval

                # keeping track of slot no. of blocks which have been filled up
                if interval<0:
                    for x in range(1, lstinterval+1):
                        slots_arrived_naturally[n-x+1]+=1
                interval=0


            #main block has n slots. this block calculates the timeframe within which
            #service will be provided to batch of n slots.
            if m_activated==False:
                starting_index=i
                #if i+math.ceil(n/servicerate)>=total_time:
                #    m=total_time
                #else:
                float_m = i+(n/servicerate)
                m=math.ceil(float_m)
            elif m_activated==True:
                starting_index=m
                if m+math.ceil(n/servicerate)>=total_time:
                    m=total_time
                else:
                    float_m = m+(n/servicerate)
                    m=math.ceil(float_m)

            ending_index=m
            
            if m>total_time:
                # m variable keeps track of total time. if time to service slots exceed m, m is set 
                # to total_time. this is unlike the other 2 problems where servicing of slot starts
                # when main block has n slots. In this problem, main block has no fixed capacity size
                # servicing will only stop when all arrived slots has been serviced. this is why m is
                # set to total time whenever m exceeds total time
                total_time=m
            
            m_activated=True
            
            # sometimes servicing of slots take fraction of seconds, i.e. 5.2/2.3 secs to complete. 
            # so, we have to keep track of exactly how much time it takes for main block to process
            # slots. For example, if servicing of slots take 5.2 secs, we should queue slots arrived
            # in 0.2 sec of 6th sec in secondary block. slots arrived in remaining 0.8 second should
            # be queued into main block.
            
            if (float_m%1)!=0:
                if m+1<= total_time:

                    # we consider the case for arrival of slots is going on and still hasn't reached 
                    # the end of slot arrival. we modify the arrived slots' array considering the fact
                    # that servicing of slots requires a float value of time. before last seconds, all
                    # arrived slots will be queued into secondary block. during the last sec, we take
                    # fraction value. if servicing time is 5.2 sec, we take 0.2 sec which is fraction
                    # value. let's assume that this second is i. we obtain arrived slots in i-th sec from
                    # arrived slots' array. we calculate how many slots may arrive in 0.2/20% of i-th sec.
                    # the reason for doing this is only this amount of slots will be slots will be queued
                    # into secondary value during this float value of time. this will allow us to manage 
                    # arrival of slots more efficiently. the remainder of arrived slots' array will be
                    # modified as follows- according to the example, remaining time of i-th second is 0.8s.
                    # we calculate arrived slots from 0.8/80% of i-th second and 0.2/20% of (i+1)-th second
                    # we add these 2 values and consider this to be number of arrived slots at (i+1)-th second 
                    first_fraction = float_m%1
                    second_fraction = 1-first_fraction

                    temp = arrival[m]
                    arrival[m] = math.floor(first_fraction* arrival[m])
                    for x in range(m+1, total_time+1):
                        temp2=arrival[x]
                        value = math.ceil(second_fraction*temp) + math.floor(first_fraction*temp2)
                        temp=arrival[x]
                        arrival[x]=value

                    arrival[total_time+1]=math.ceil(second_fraction*temp)
                    total_time+=1

                elif arrival[m]>0:
                    # we consider the case when arrival of slots has almost reached the end of slot arrival. 
                    # after a service of slots' event, only the last second of arrived slots is pending. 
                    # in this case, we modify the last elemnt of arrived slots' array we consider the fact 
                    # that servicing of slots requires a float value of time. if servicing time is 5.2 sec, 
                    # we take 0.2 sec which is fraction value. let's assume that this second is i, which is 
                    # last second for slot arrival. we obtain arrived slots in i-th sec from arrived slots' 
                    # array. we calculate how many slots may arrive in 0.2/20% of i-th sec. this value is 
                    # the number of slots arrived at i-th second. remaining time of i-th second is 0.8s. 
                    # we calculate arrived slots from 0.8/80% of i-th second and and consider this to be 
                    # number of arrived slots at (i+1)-th second.
                    total_time+=1
                    first_fraction = float_m%1
                    second_fraction = 1-first_fraction

                    temp = arrival[m]
                    arrival[m] = math.floor(first_fraction* arrival[m])
                    arrival[total_time]=math.ceil(second_fraction*temp)
                    
                
                
            while True:
                #for loop shows the code of main block processing n slots.
                #in the meantime, secondary block stores arrived slots while
                #main block is busy processing n slots
                for j in range(starting_index+1,ending_index+1):
                    #secondary.append(arrival[j])
                    service[j]=0
                    if j<=total_time:
                        no_of_slots_in_secondary_block+=arrival[j]
                
                for x in range(n+1):
                    count_of_slots_being_serviced[x]+=1

                # keeping track of the number of slots that have been processed
                # increasing service event by 1
                pending_slots-=n
                service_event+=1
                if pending_slots==0:
                    break
                m=m+1

                # changing value of n. this way, block size, n is adaptive
                # the number of slots in secondary block will be the new value of n
                # all slots will be queued from secondary block to main block
                service[m]=no_of_slots_in_secondary_block
                slots_queued_from_secondary_block[no_of_slots_in_secondary_block]+=1
                if no_of_slots_in_secondary_block>0:
                    n= no_of_slots_in_secondary_block
                elif no_of_slots_in_secondary_block==0:
                    m+=1
                    if m<=total_time:
                        n=arrival[m]
                values_of_n[n_count]=n
                n_count+=1
                
                if n>max_value:
                    max_value=n
                
                if m<=total_time:
                    no_of_slots_in_secondary_block=arrival[m]
                starting_index=m
                float_m = m+(n/servicerate)
                m=math.ceil(float_m)
                ending_index=m
                if m>total_time:
                    total_time=m
                # sometimes servicing of slots take fraction of seconds, i.e. 5.2/2.3 secs to complete. 
                # so, we have to keep track of exactly how much time it takes for main block to process
                # slots. For example, if servicing of slots take 5.2 secs, we should queue slots arrived
                # in 0.2 sec of 6th sec in secondary block. slots arrived in remaining 0.8 second should
                # be queued into main block.
                
                if (float_m%1)!=0:
                    if m+1<= total_time:

                    # we consider the case for arrival of slots is going on and still hasn't reached 
                    # the end of slot arrival. we modify the arrived slots' array considering the fact
                    # that servicing of slots requires a float value of time. before last seconds, all
                    # arrived slots will be queued into secondary block. during the last sec, we take
                    # fraction value. if servicing time is 5.2 sec, we take 0.2 sec which is fraction
                    # value. let's assume that this second is i. we obtain arrived slots in i-th sec from
                    # arrived slots' array. we calculate how many slots may arrive in 0.2/20% of i-th sec.
                    # the reason for doing this is only this amount of slots will be slots will be queued
                    # into secondary value during this float value of time. this will allow us to manage 
                    # arrival of slots more efficiently. the remainder of arrived slots' array will be
                    # modified as follows- according to the example, remaining time of i-th second is 0.8s.
                    # we calculate arrived slots from 0.8/80% of i-th second and 0.2/20% of (i+1)-th second
                    # we add these 2 values and consider this to be number of arrived slots at (i+1)-th second 
                        first_fraction = float_m%1
                        second_fraction = 1-first_fraction

                        temp = arrival[m]
                        arrival[m] = math.floor(first_fraction* arrival[m])
                        for x in range(m+1, total_time+1):
                            temp2=arrival[x]
                            value = math.ceil(second_fraction*temp) + math.floor(first_fraction*temp2)
                            temp=arrival[x]
                            arrival[x]=value

                        arrival[total_time+1]=math.ceil(second_fraction*temp)
                        total_time+=1
                        
                    elif arrival[m]>0:
                    # we consider the case when arrival of slots has almost reached the end of slot arrival. 
                    # after a service of slots' event, only the last second of arrived slots is pending. 
                    # in this case, we modify the last elemnt of arrived slots' array we consider the fact 
                    # that servicing of slots requires a float value of time. if servicing time is 5.2 sec, 
                    # we take 0.2 sec which is fraction value. let's assume that this second is i, which is 
                    # last second for slot arrival. we obtain arrived slots in i-th sec from arrived slots' 
                    # array. we calculate how many slots may arrive in 0.2/20% of i-th sec. this value is 
                    # the number of slots arrived at i-th second. remaining time of i-th second is 0.8s. 
                    # we calculate arrived slots from 0.8/80% of i-th second and and consider this to be 
                    # number of arrived slots at (i+1)-th second.
                        total_time+=1
                        first_fraction = float_m%1
                        second_fraction = 1-first_fraction

                        temp = arrival[m]
                        arrival[m] = math.floor(first_fraction* arrival[m])
                        arrival[total_time]=math.ceil(second_fraction*temp)
                    
                    

                

        if pending_slots==0:
            break

    for i in range(0,max_value+1):
        #this block calculates the number of time slots have been queued into
        #main block naturally or secondary block
        queuing_time_from_secondary_block+=slots_queued_from_secondary_block[i]
        arrival_time+=slots_arrived_naturally[i]
        service_time+=count_of_slots_being_serviced[i]
        
    print('\nAdaptive values of n(changing values of n is completely dependent on arrival of slots) :')
    for i in range(1,n_count):
        print(values_of_n[i])

    # using arrival rate and service rate, the time required for arrival and service events
    # main block processes all n slots at an equal service rate unlike arrival. so, number
    # of service events is taken into consideration for calculating n slots.
    arrival_time=arrival_time/arrivalrate
    service_time/=servicerate
    system_time=arrival_time+service_time+queuing_time_from_secondary_block

    print('\ni slots probability values:')
    for p in range(0,max_value+1):
        # main block processes all n slots at an equal service rate unlike arrival. so, number
        # of service events is taken into consideration for calculating n slots. for service
        # events, all i slots are equiprobable. for all i slots, main block has same similarity
        # to have i slots during a service event

        # for arrival events, we have kept track of how many times each i-slot have been queued
        # into main block(natually/from secondary block) using 2 dictionaries. these are taken
        # into account while calculating probability of i-th slot in case of arrival events
        if arrival_time>0 and system_time>0:
            arrival_event_prob[p] = (arrival_time/system_time) * (slots_arrived_naturally[p]/(arrivalrate*arrival_time))
        if service_time>0 and system_time>0:
            service_event_prob[p] = (service_time/system_time) * (count_of_slots_being_serviced[p]/(servicerate*service_time))
        if queuing_time_from_secondary_block>0 and system_time>0:
            queuing_event_prob[p] = (queuing_time_from_secondary_block/system_time) * (slots_queued_from_secondary_block[p]/queuing_time_from_secondary_block)

        probability_i[p] = arrival_event_prob[p]+ service_event_prob[p] + queuing_event_prob[p]
        sum_of_probability+=probability_i[p]
        print('i=',p,'   P[i]=',probability_i[p])
        
    for y in range(1, max_value+1):
        final_probability_i[y]=probability_i[y]

    print('\nSum of n slots probability', sum_of_probability)

    #probability values are plotted in graph
    plt.plot(list(final_probability_i.values()))
    plt.show()


def Problem_3():
    total_time=-1
    n=-1
    while total_time<0:
        total_time=int(input('Please provide the time for which you want to run the system.  '))
        if total_time<=0:
            print('Please provide a positive time')
        else:
            break
    while n<0:
        n=int(input('Please provide the capacity of main block(n)  '))
        if n<=0:
            print('Please provide a positive block size')
        else:
            break
    seed(10)
    sum_of_arrived_slots=0
    no_of_slots_in_secondary_block=0
    sum_of_probability=0
    minimum=0
    medium=0
    maximum=0
    m=0
    system_time=0
    queuing_time_from_secondary_block=0
    arrival_time=0
    service_event=0
    service_time=0
    m_activated=False
    arrival={}
    service ={}
    secondary={}
    slots_queued_from_secondary_block={}
    slots_arrived_naturally={}
    probability_i={}
    arrival_event_prob={}
    service_event_prob={}
    queuing_event_prob={}
    count_of_slots_being_serviced={}
    system_time_estimation={}
    secondary_block_size_estimation={}
    options_for_n={}
    float_m=0
    first_fraction=0
    second_fraction=0
    events=0
    

    for i in range(1,1001):
        # service and secondary dictionaries are used when the system is running
        # service dictionary stores the number of slots in main block at a given time
        # secondary dictionary stores the number of slots in secondary block at a given time
        service[i]=0
        secondary[i]=0
        arrival[i]=0
        #arrival.append(randint(1,10))
        

    for i in range(1,total_time+1):
        # arrival dictionary is used to store arrived slots to the system in each second
        # slots queued from secondary block dictionary is used to keep track of the number of times
        # i(1,2,3...n) number of slots have been queued from secondary block to first block
        # slots arrived naturally dictionary is used to keep track of the number of time i-th slot
        # have been queued into main block nautrally, not from secondary block
        arrival[i]=randint(1,n)

    

    for i in range(1,total_time+1):
        #sum of arrived_slots dictionary calculates total arrived slots
        sum_of_arrived_slots=sum_of_arrived_slots+arrival[i]

    # arrival rate and service rate specifies arrival rate of slots and service rate at which slots are processed
    pending_slots=sum_of_arrived_slots
    arrivalrate=sum_of_arrived_slots/total_time
    servicerate=arrivalrate*2
    
    # we will consider few options for choosing n. the options are arrival rate, maximum limit of
    # arrived slots per second, service rate,  average of arrival rate and maximum limit of arrived slots
    # and average of arrival rate and maximum limit of arrived slots.
    # we calculate approximate system time and approximate slots in secondary block for each of these options
    options_for_n[0]=int(arrivalrate)
    options_for_n[1]=n
    options_for_n[2]=int((arrivalrate+n)/2)
    options_for_n[3]=int(servicerate)
    options_for_n[4]=int((servicerate+n)/2)
    
    for q in range(5):
        events=(int)(sum_of_arrived_slots/options_for_n[q])
        system_time_estimation[q]=(events*(options_for_n[q]/arrivalrate))
        system_time_estimation[q]+=(events*(options_for_n[q]/servicerate))
        system_time_estimation[q]+=((sum_of_arrived_slots-(events*options_for_n[q]))/arrivalrate)
        secondary_block_size_estimation[q]=(events*(options_for_n[q]/servicerate)*arrivalrate)
    
    print('\nWe have considered several options for block capacity-\n1. Arrival rate\n2. Maximum limit of slots\n3. Average of arrival rate and maximum limit of slots\n4. Service rate\n3. Average of service rate and maximum limit of slots')
    print('\nAfter comparing each of these options\' approximate system time and secondary block size,\n')
    
    # we compare approximate system time and approximate secondary block size for each of these options.
    # whichever option has approximate lowest system time and secondary block size, block size is set to
    # the option value. we give priority to lowest secondary block size between system time and secondary
    # block size. if we can't find a clear winner consider system time and secondary block size, we will
    # choose whichever option has lowest secondary block size. The objective of the problem is slots should
    # be processed as soon as they arrive. In order to do that, secondary slots should have fewer slots.
    if system_time_estimation[0]<system_time_estimation[1] and system_time_estimation[0]<system_time_estimation[2] and system_time_estimation[0]<system_time_estimation[3] and system_time_estimation[0]<system_time_estimation[4] and secondary_block_size_estimation[0]<secondary_block_size_estimation[1] and secondary_block_size_estimation[0]<secondary_block_size_estimation[2] and secondary_block_size_estimation[0]<secondary_block_size_estimation[3] and secondary_block_size_estimation[0]<secondary_block_size_estimation[4]:
        print('Block capacity of main block is set to arrival rate. The value is ',int(arrivalrate))
        n=int(arrivalrate)
    elif secondary_block_size_estimation[0]<secondary_block_size_estimation[1] and secondary_block_size_estimation[0]<secondary_block_size_estimation[2] and secondary_block_size_estimation[0]<secondary_block_size_estimation[3] and secondary_block_size_estimation[0]<secondary_block_size_estimation[4]:
        print('Block capacity of main block is set to arrival rate. The value is ',int(arrivalrate))
        n=int(arrivalrate)
    elif system_time_estimation[1]<system_time_estimation[0] and system_time_estimation[1]<system_time_estimation[2] and system_time_estimation[1]<system_time_estimation[3] and system_time_estimation[1]<system_time_estimation[4] and secondary_block_size_estimation[1]<secondary_block_size_estimation[0] and secondary_block_size_estimation[1]<secondary_block_size_estimation[2] and secondary_block_size_estimation[1]<secondary_block_size_estimation[3] and secondary_block_size_estimation[1]<secondary_block_size_estimation[4]:
        print('Block capacity of main block is set to maximum limit on slots per second. The value is ',n)
    elif secondary_block_size_estimation[1]<secondary_block_size_estimation[0] and secondary_block_size_estimation[1]<secondary_block_size_estimation[2] and secondary_block_size_estimation[1]<secondary_block_size_estimation[3] and secondary_block_size_estimation[1]<secondary_block_size_estimation[4]:
        print('Block capacity of main block is set to maximum limit on slots per second. The value is ',n)
    elif system_time_estimation[2]<system_time_estimation[0] and system_time_estimation[2]<system_time_estimation[1] and system_time_estimation[2]<system_time_estimation[3] and system_time_estimation[2]<system_time_estimation[4] and secondary_block_size_estimation[2]<secondary_block_size_estimation[0] and secondary_block_size_estimation[2]<secondary_block_size_estimation[1] and secondary_block_size_estimation[2]<secondary_block_size_estimation[3] and secondary_block_size_estimation[2]<secondary_block_size_estimation[4]:
        print('Block capacity of main block is set to average of arrival rate and maximum limit on slots per second. The value is ',int((arrivalrate+n)/2))
        n=int((arrivalrate+n)/2)
    elif secondary_block_size_estimation[2]<secondary_block_size_estimation[0] and secondary_block_size_estimation[2]<secondary_block_size_estimation[1] and secondary_block_size_estimation[2]<secondary_block_size_estimation[3] and secondary_block_size_estimation[2]<secondary_block_size_estimation[4]:
        print('Block capacity of main block is set to average of arrival rate and maximum limit on slots per second. The value is ',int((arrivalrate+n)/2))
        n=int((arrivalrate+n)/2)
    elif system_time_estimation[3]<system_time_estimation[1] and system_time_estimation[3]<system_time_estimation[2] and system_time_estimation[0]>system_time_estimation[3] and system_time_estimation[3]<system_time_estimation[4] and secondary_block_size_estimation[3]<secondary_block_size_estimation[1] and secondary_block_size_estimation[3]<secondary_block_size_estimation[2] and secondary_block_size_estimation[0]>secondary_block_size_estimation[3] and secondary_block_size_estimation[3]<secondary_block_size_estimation[4]:
        print('Block capacity of main block is set to service rate. The value is ',int(servicerate))
        n=int(servicerate)
    elif secondary_block_size_estimation[3]<secondary_block_size_estimation[1] and secondary_block_size_estimation[3]<secondary_block_size_estimation[2] and secondary_block_size_estimation[0]>secondary_block_size_estimation[3] and secondary_block_size_estimation[3]<secondary_block_size_estimation[4]:
        print('Block capacity of main block is set to service rate. The value is ',int(servicerate))
        n=int(servicerate)
    elif system_time_estimation[4]<system_time_estimation[0] and system_time_estimation[4]<system_time_estimation[1] and system_time_estimation[4]<system_time_estimation[3] and system_time_estimation[2]>system_time_estimation[4] and secondary_block_size_estimation[4]<secondary_block_size_estimation[0] and secondary_block_size_estimation[4]<secondary_block_size_estimation[1] and secondary_block_size_estimation[4]<secondary_block_size_estimation[3] and secondary_block_size_estimation[2]>secondary_block_size_estimation[4]:
        print('Block capacity of main block is set to average of service rate and maximum limit on slots per second. The value is ',int((servicerate+n)/2))
        n=int((arrivalrate+n)/2)
    elif secondary_block_size_estimation[4]<secondary_block_size_estimation[0] and secondary_block_size_estimation[4]<secondary_block_size_estimation[1] and secondary_block_size_estimation[4]<secondary_block_size_estimation[3] and secondary_block_size_estimation[2]>secondary_block_size_estimation[4]:
        print('Block capacity of main block is set to average of service rate and maximum limit on slots per second. The value is ',int((servicerate+n)/2))
        n=int((arrivalrate+n)/2)

    interval=n
    
    
    for z in range(0,n+1):
    # all these dictionaries are used for probability calculation
    # arrival, service, queueing event probability dictionaries store probabilities of
    # i-th slot in main block in case of each event
    # probability dictionary sums up each i-th slot's cummulative probability for all events
        probability_i[z]=0
        arrival_event_prob[z]=0
        service_event_prob[z]=0
        queuing_event_prob[z]=0
        slots_queued_from_secondary_block[z]=0
        slots_arrived_naturally[z]=0

    for i in range(1,total_time+1):

        if m> total_time and no_of_slots_in_secondary_block<n:
            break

        lstinterval=interval

        # m_activated boolean variable is used to check whether slots have started coming from secondary block
        # if the value is set false, slots are coming naturally
        # if the value is set true, slots have started coming from secondary block
        # interval variable keeps track of how many slots can be further queued into main block
        # suppose, main block has n capacity and already has i slots.
        # so, value of interval will be n-i
        # if interval's value is less than 0, it means slots will be queued into secondary block
        if no_of_slots_in_secondary_block==0:
            if m_activated==False:
                interval=interval-arrival[i]
            elif m_activated==True and m<=total_time:
                interval=interval-arrival[m]
        else:
            interval=interval-no_of_slots_in_secondary_block

        # keeping track of slot no. of blocks which have been filled up
        if interval>=0:
            for x in range(interval, lstinterval):
                slots_arrived_naturally[n-x]+=1
                service[i]=arrival[i]
        if interval>0:
            #service.append(arrival[i])
            service[i]=arrival[i]
        elif interval<=0:

            if lstinterval !=0:
                #service.append(lstinterval)
                #arrival[i]=arrival[i]-lstinterval

                # if interval's value is less than or equal to 0, then main block has
                # n slots. main block will start processing batch of n slots.
                # this block calculates how many slots can be queued into secondary block
                # no_of_slots_in_secondary_block calculates the number of slots in secondary block
                if m_activated==False:
                    no_of_slots_in_secondary_block=arrival[i]-lstinterval
                elif m_activated==True and m<=total_time:
                    no_of_slots_in_secondary_block=arrival[m]-lstinterval

                # keeping track of slot no. of blocks which have been filled up
                if interval<0:
                    for x in range(1, lstinterval+1):
                        slots_arrived_naturally[n-x+1]+=1
                interval=0


            #main block has n slots. this block calculates the timeframe within which
            #service will be provided to batch of n slots.
            if m_activated==False:
                starting_index=i
                #if i+math.ceil(n/servicerate)>=total_time:
                #    m=total_time
                #else:
                m=i+math.ceil(n/servicerate)
            elif m_activated==True:
                starting_index=m
                if m+math.ceil(n/servicerate)>=total_time:
                    m=total_time
                else:
                    m=m+math.ceil(n/servicerate)

            ending_index=m
            
            
            # sometimes servicing of slots take fraction of seconds, i.e. 5.2/2.3 secs to complete. 
            # so, we have to keep track of exactly how much time it takes for main block to process
            # slots. For example, if servicing of slots take 5.2 secs, we should queue slots arrived
            # in 0.2 sec of 6th sec in secondary block. slots arrived in remaining 0.8 second should
            # be queued into main block.
            
            if (float_m%1)!=0:
                if m+1<= total_time:

                    # we consider the case for arrival of slots is going on and still hasn't reached 
                    # the end of slot arrival. we modify the arrived slots' array considering the fact
                    # that servicing of slots requires a float value of time. before last seconds, all
                    # arrived slots will be queued into secondary block. during the last sec, we take
                    # fraction value. if servicing time is 5.2 sec, we take 0.2 sec which is fraction
                    # value. let's assume that this second is i. we obtain arrived slots in i-th sec from
                    # arrived slots' array. we calculate how many slots may arrive in 0.2/20% of i-th sec.
                    # the reason for doing this is only this amount of slots will be slots will be queued
                    # into secondary value during this float value of time. this will allow us to manage 
                    # arrival of slots more efficiently. the remainder of arrived slots' array will be
                    # modified as follows- according to the example, remaining time of i-th second is 0.8s.
                    # we calculate arrived slots from 0.8/80% of i-th second and 0.2/20% of (i+1)-th second
                    # we add these 2 values and consider this to be number of arrived slots at (i+1)-th second 
                    first_fraction = float_m%1
                    second_fraction = 1-first_fraction

                    temp = arrival[m]
                    arrival[m] = math.floor(first_fraction* arrival[m])
                    for x in range(m+1, total_time+1):
                        temp2=arrival[x]
                        value = math.ceil(second_fraction*temp) + math.floor(first_fraction*temp2)
                        temp=arrival[x]
                        arrival[x]=value

                    arrival[total_time+1]=math.ceil(second_fraction*temp)
                    total_time+=1

                elif arrival[m]>0:
                    # we consider the case when arrival of slots has almost reached the end of slot arrival. 
                    # after a service of slots' event, only the last second of arrived slots is pending. 
                    # in this case, we modify the last elemnt of arrived slots' array we consider the fact 
                    # that servicing of slots requires a float value of time. if servicing time is 5.2 sec, 
                    # we take 0.2 sec which is fraction value. let's assume that this second is i, which is 
                    # last second for slot arrival. we obtain arrived slots in i-th sec from arrived slots' 
                    # array. we calculate how many slots may arrive in 0.2/20% of i-th sec. this value is 
                    # the number of slots arrived at i-th second. remaining time of i-th second is 0.8s. 
                    # we calculate arrived slots from 0.8/80% of i-th second and and consider this to be 
                    # number of arrived slots at (i+1)-th second.
                    total_time+=1
                    first_fraction = float_m%1
                    second_fraction = 1-first_fraction

                    temp = arrival[m]
                    arrival[m] = math.floor(first_fraction* arrival[m])
                    arrival[total_time]=math.ceil(second_fraction*temp)
                                   

            while True:
                #for loop shows the code of main block processing n slots.
                #in the meantime, secondary block stores arrived slots while
                #main block is busy processing n slots
                for j in range(starting_index+1,ending_index+1):
                    #secondary.append(arrival[j])
                    service[j]=0
                    if j<=total_time:
                        no_of_slots_in_secondary_block+=arrival[j]
                    #secondary[i]=arrival[j]

                service_event+=1
                m=m+1

                #processing is over. if secondary block has less than or equal to n slots, all
                #slots will be queued into main block. it will assumed that this transfer takes 1 sec
                if no_of_slots_in_secondary_block<n:
                    service[m]=no_of_slots_in_secondary_block
                    interval=n-service[m]
                    slots_queued_from_secondary_block[no_of_slots_in_secondary_block]+=1
                    no_of_slots_in_secondary_block=0

                    if interval==0:
                        m+=1
                        service[m]=n
                        no_of_slots_in_secondary_block -= n
                        slots_queued_from_secondary_block[n]+=1
                        starting_index=m
                        m+=math.ceil(n/servicerate)
                        ending_index=m
                        
                        # we consider the case for arrival of slots is going on and still hasn't reached 
                        # the end of slot arrival. we modify the arrived slots' array considering the fact
                        # that servicing of slots requires a float value of time. before last seconds, all
                        # arrived slots will be queued into secondary block. during the last sec, we take
                        # fraction value. if servicing time is 5.2 sec, we take 0.2 sec which is fraction
                        # value. let's assume that this second is i. we obtain arrived slots in i-th sec from
                        # arrived slots' array. we calculate how many slots may arrive in 0.2/20% of i-th sec.
                        # the reason for doing this is only this amount of slots will be slots will be queued
                        # into secondary value during this float value of time. this will allow us to manage 
                        # arrival of slots more efficiently. the remainder of arrived slots' array will be
                        # modified as follows- according to the example, remaining time of i-th second is 0.8s.
                        # we calculate arrived slots from 0.8/80% of i-th second and 0.2/20% of (i+1)-th second
                        # we add these 2 values and consider this to be number of arrived slots at (i+1)-th second
                        
                        if (float_m%1)!=0:
                            if m+1<=total_time:
                                # we consider the case for arrival of slots is going on and still hasn't 
                                # reached the end of slot arrival. we modify the arrived slots' array 
                                # considering the fact that servicing of slots requires a float value of time.
                                # before last seconds, all arrived slots will be queued into secondary block. 
                                # during the last sec, we take fraction value. if servicing time is 5.2 sec, 
                                # we take 0.2 sec which is fraction value. let's assume that this second is i.
                                # we obtain arrived slots in i-th sec from arrived slots' array. we calculate 
                                # how many slots may arrive in 0.2/20% of i-th sec. the reason for doing this
                                # is only this amount of slots will be slots will be queued into secondary 
                                # value during this float value of time. this will allow us to manage 
                                # arrival of slots more efficiently. the remainder of arrived slots' array 
                                # will be modified as follows- according to the example, remaining time of 
                                # i-th second is 0.8s. we calculate arrived slots from 0.8/80% of i-th second 
                                # and 0.2/20% of (i+1)-th second we add these 2 values and consider this to be
                                # number of arrived slots at (i+1)-th second
                                first_fraction = float_m%1
                                second_fraction = 1-first_fraction

                                temp = arrival[m]
                                arrival[m] = math.floor(first_fraction* arrival[m+1])
                                for x in range(m+1, total_time+1):
                                    temp2=arrival[x]
                                    value = math.ceil(second_fraction*temp) + math.floor(first_fraction*temp2)
                                    temp=arrival[x]
                                    arrival[x]=value

                                arrival[total_time+1]=math.ceil(second_fraction*temp)
                                total_time+=1
                            elif arrival[m]>0:
                                # we consider the case when arrival of slots has almost reached the end of slot
                                # arrival. after a service of slots' event, only the last second of arrived 
                                # slots is pending. in this case, we modify the last elemnt of arrived slots' 
                                # array we consider the fact that servicing of slots requires a float value of
                                # time. if servicing time is 5.2 sec, we take 0.2 sec which is fraction value.
                                # let's assume that this second is i, which is last second for slot arrival. 
                                # we obtain arrived slots in i-th sec from arrived slots' array. we calculate 
                                # how many slots may arrive in 0.2/20% of i-th sec. this value is the number 
                                # of slots arrived at i-th second. remaining time of i-th second is 0.8s. 
                                # we calculate arrived slots from 0.8/80% of i-th second and and consider this
                                # to be number of arrived slots at (i+1)-th second.
                                total_time+=1
                                first_fraction = float_m%1
                                second_fraction = 1-first_fraction

                                temp = arrival[m]
                                arrival[m] = math.floor(first_fraction* arrival[m])
                                arrival[total_time]=math.ceil(second_fraction*temp)
                elif no_of_slots_in_secondary_block>=n:
                    #if secondary block has more than n slots, only n slots will be queued into main
                    #block. since main block's capacity is n slots. during this slot transfer period,
                    #secondary slot will store arrived slots. since main block has n slots, it will process
                    #a batch of n slots again
                    service[m]=n
                    interval=0
                    no_of_slots_in_secondary_block -= n
                    slots_queued_from_secondary_block[n]+=1
                    if m<=total_time:
                        no_of_slots_in_secondary_block+=arrival[m]
                    starting_index=m
                    m=m+math.ceil(n/servicerate)
                    ending_index=m
                    
                    if (float_m%1)!=0: 
                        if m+1<=total_time:
                            first_fraction = float_m%1
                            second_fraction = 1-first_fraction

                            temp = arrival[m]
                            arrival[m] = math.floor(first_fraction* arrival[m+1])
                            for x in range(m+1, total_time+1):
                                temp2=arrival[x]
                                value = math.ceil(second_fraction*temp) + math.floor(first_fraction*temp2)
                                temp=arrival[x]
                                arrival[x]=value

                            arrival[total_time+1]=math.ceil(second_fraction*temp)
                            total_time+=1
                        elif arrival[m]>0:
                            total_time+=1
                            first_fraction = float_m%1
                            second_fraction = 1-first_fraction

                            temp = arrival[m]
                            arrival[m] = math.floor(first_fraction* arrival[m])
                            arrival[total_time]=math.ceil(second_fraction*temp)

                m_activated=True
                if interval>0 or m>total_time:
                    break

    for i in range(0,n+1):
        #this block calculates the number of time slots have been queued into
        #main block naturally or secondary block
        queuing_time_from_secondary_block+=slots_queued_from_secondary_block[i]
        arrival_time+=slots_arrived_naturally[i]

    #using arrival rate and service rate, the time required for arrival and service events
    #main block processes all n slots at an equal service rate unlike arrival. so, number
    #of service events is taken into consideration for calculating n slots.
    arrival_time=arrival_time/arrivalrate
    service_time=(n+1)/servicerate
    service_time*=service_event
    system_time=arrival_time+service_time+queuing_time_from_secondary_block

    print('\ni slots probability values:')
    for p in range(0,n+1):
        #main block processes all n slots at an equal service rate unlike arrival. so, number
        #of service events is taken into consideration for calculating n slots. for service
        #events, all i slots are equiprobable. for all i slots, main block has same similarity
        #to have i slots during a service event

        #for arrival events, we have kept track of how many times each i-slot have been queued
        #into main block(natually/from secondary block) using 2 dictionaries. these are taken
        #into account while calculating probability of i-th slot in case of arrival events
        if arrival_time>0 and system_time>0:
            arrival_event_prob[p] = (arrival_time/system_time) * (slots_arrived_naturally[p]/(arrivalrate*arrival_time))
        if service_time>0 and system_time>0:
            service_event_prob[p] = (service_time/system_time) * (service_event/(servicerate*service_time))
        if queuing_time_from_secondary_block>0 and system_time>0:
            queuing_event_prob[p] = (queuing_time_from_secondary_block/system_time) * (slots_queued_from_secondary_block[p]/queuing_time_from_secondary_block)
        probability_i[p] = arrival_event_prob[p]+ service_event_prob[p] + queuing_event_prob[p]
        sum_of_probability+=probability_i[p]
        print('i=',p,'   P[i]=',probability_i[p])

    print('\nSum of n slots probability', sum_of_probability)

    #probability values are plotted in graph
    plt.plot(list(probability_i.values()))
    plt.show()





print('~~~~~~~~~~ Welcome to Synchronous Control System ~~~~~~~~~~')
print('           Developed by:')
print('           Khaled Mohammed Saifuddin')
print('           Muhammad Ifte Khairul Islam')
print('           Farhan Tanvir\n')



while True:
    p1=int(input("Press 1 to run problem_1: \nPress 2 to run Problem_2: \nPress 3 to run Problem_3: \n        OR          \nPress any digit to exit: \n"))

# map the inputs to the function blocks
    options = {1 : Problem_1,
           2 : Problem_2,
           3 : Problem_3,

                }
    if (p1==1 or p1==2 or p1==3):
        options[p1]()
    else:
        print ("Exit")
        break