import json

with open('./daikibo-telemetry-data.json', 'r') as fileReader:
   telemetries_n = json.load(fileReader)

listOfUnhealthyTelemetries = []

listOfFactories = [
                     'daikibo-berlin', 
                     'daikibo-factory-meiyo', 
                     'daikibo-factory-seiko', 
                     'daikibo-shenzhen' 
                  ];

listOfDeviceTypes = [
                        'AirWrench', 
                        'CNC', 
                        'ConveyorBelt', 
                        'Furnace', 
                        'HeavyDutyDrill', 
                        'LaserCutter', 
                        'LaserWelder', 
                        'MetalPress', 
                        'SpotWelder' 
                    ];

for factory in listOfFactories:
   for deviceType in listOfDeviceTypes:
      listOfUnhealthyTelemetries.append(
                                          {
                                             'factory'    : factory, 
                                             'deviceType' : deviceType, 
                                             'unhealthy'  : 0 
                                          }
                                       )

for telemetry_i in telemetries_n:
   if telemetry_i['data']['status'] == 'unhealthy':
      for unhealthyTelemetry in listOfUnhealthyTelemetries:
         if  telemetry_i['location']['factory'] == unhealthyTelemetry['factory'] \
         and telemetry_i['deviceType']          == unhealthyTelemetry['deviceType']:
            unhealthyTelemetry['unhealthy'] += 10

fileWriter = open('unhealthyTelemetries.csv', 'w')

fileWriter.write('Factory,Device Type,Unhealthy\n')

for unhealthyTelemetry in listOfUnhealthyTelemetries:
   fileWriter.write( unhealthyTelemetry['factory']    + ',' + 
                     unhealthyTelemetry['deviceType'] + ',' + 
                 str(unhealthyTelemetry['unhealthy']) + '\n')

fileWriter.close()

