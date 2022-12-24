from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import start_server
from datetime import datetime

# passes = {
#             "CBJ-couple": 120,
#             "CBJ-single": 120,
#             "GGS-couple": 60,
#             "GGS-single": 60,
#             "MLK-couple": 60,
#             "MLK-single": 60
#         }
passes1 = {
    "CBJ-couple": {
        'time': 120
    },
    "CBJ-single": {
        'time': 120
    },
    "GGS-couple": {
        'time': 60
    },
    "GGS-single": {
        'time': 60
    },
    "MLK-couple": {
        'time': 60
    },
    "MLK-single": {
        'time': 60
    }
}        

def time():
    while True:
       # Taking input from the user
        data = input_group("Trip Calculator", [
            input('Start Time', name='start', type=TIME,
                required=True, PlaceHolder=""),
            
            input('End Time', name='end', type=TIME,
                required=True, PlaceHolder=""),
                
            input('Type', name='type', type= TEXT, required=True, 
                PlaceHolder="Scooter/ Bike ",
                datalist=['scooter', 'bike']),

            input('Penalty RM (Optional)', name='penalty', value=0 ,min=0, type=NUMBER),

            input('Pass (Optional)', name='pass', type= TEXT, 
                PlaceHolder="Pass ",
                datalist=["CBJ-couple","CBJ-Single","GGS-couple","GGS-single","MLK-couple","MLK-single"]),
        ])


        #Bike pricing
        first_min = 15
        price = 0.40
        first_min_price = 2
        
        # Scooter pricing
        if data['type'] == 'scooter':
            first_min = 0
            price = 0.50
            first_min_price = 0

        start_time = datetime.strptime(data['start'], "%H:%M")
        end_time = datetime.strptime(data['end'], "%H:%M")
        # get difference
        delta = end_time - start_time
        
        # Convert the difference to sec
        sec = delta.total_seconds()
        # Convert the difference to M-sec
        mSec = sec/1000
        
        
        # passes check 
        if data['pass'] in passes1:
            
            pass_time= passes1[data['pass']]['time']
            print(type(data['pass']))
            min = (sec/60) - pass_time
            pass_text = 'Pass type: ' + data['pass'] +' '+str(pass_time)+' min'
        else:
            # sec to min
            min = sec / 60
            pass_text=''


        if min <=15 and str(data['type']) == "bike" :
            # First 15 min for RM2
            trip_fare =2
        else:
            trip_fare = (min - first_min)* price + first_min_price 
        
        if min <60:
            full_time=''
        elif min == 60:
            full_time = 'One Hour ||'   
        else:
            #full difference time format
            full_time=str(delta) +' ||' 

        if data['penalty'] >0:
            #calculat penalty
            fine= (data['penalty'] / price) + min

            fare_total= trip_fare + data['penalty']

            fine_text= 'Total min with penalty: ' + str(fine) + '\nTrip fare with penalty: RM' +str(round(fare_total,4))

        else:  
            fine_text= ''

        v_type=["scooter","bike"]
        #result
        if str(data['type']) in v_type and min>0 : 
                popup("Trip Details",
                    f"Start time: {data['start']}\nEnd time: {data['end']}\
                    \nType: {str(data['type'])}\nDuration: {full_time} {min} min || {format(mSec, '.6f')} M-sec\nTrip Fare: RM{round(trip_fare,4)}\n{pass_text}\n{fine_text}",
                    closable=True )
        
        else:   
            #Validation for negative Time         
            if min <=0:
                 toast('Negative Time is not allowed', position='center', color='red', duration=2)
            else:
                #Validation for check the type 
                toast('Wrong Type please choose Scooter or Bike', position='center', color='red', duration=2)
                
    # put_button("Reload",onclick=lambda: run_js('window.location.reload()'))

if __name__ == '__main__':
    
    start_server(time, port=80)
    
    


    