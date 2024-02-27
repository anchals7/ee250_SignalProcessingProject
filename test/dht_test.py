import grovepi
import math
import time
dht = 7
if __name__ == '__main__':
    while True:
        [temp,humi] = grovepi.dht(dht,0)  
        if math.isnan(temp) == False and math.isnan(humi) == False:
            print("temp:" + str(temp) + ", humi:" + str(humi))
        time.sleep(1)
