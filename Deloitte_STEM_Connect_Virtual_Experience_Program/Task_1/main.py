import json, unittest, datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)

# Create the expected JSON format from a tuple of ordered string values.
def createExpectedFormat (*tupleOfValues):
  return {
            'deviceID'    : tupleOfValues[0], 
            'deviceType'  : tupleOfValues[1], 
            'timestamp'   : tupleOfValues[2], 
            'location'    : 
              {
                'country' : tupleOfValues[3],
                'city'    : tupleOfValues[4],
                'area'    : tupleOfValues[5],
                'factory' : tupleOfValues[6],
                'section' : tupleOfValues[7]                
              }, 
            'data' : 
              {
                'status'      : tupleOfValues[8],
                'temperature' : tupleOfValues[9]
              }
          }

def convertFromFormat1 ():
  return createExpectedFormat (
    jsonData1['deviceID'], 
    jsonData1['deviceType'], 
    jsonData1['timestamp'], 
    jsonData1['location'].split('/')[0], 
    jsonData1['location'].split('/')[1], 
    jsonData1['location'].split('/')[2], 
    jsonData1['location'].split('/')[3], 
    jsonData1['location'].split('/')[4], 
    jsonData1['operationStatus'], 
    jsonData1['temp'] 
  )

def convertFromFormat2 ():
  return createExpectedFormat (
    jsonData2['device']['id'], 
    jsonData2['device']['type'], 
    int(
          (
              datetime.datetime.strptime(
                                          jsonData2['timestamp'], 
                                          '%Y-%m-%dT%H:%M:%S.%fZ'
                                        ) 
            - datetime.datetime(1970, 1, 1)
          ).total_seconds()*1000
        ), 
    jsonData2['country'], 
    jsonData2['city'], 
    jsonData2['area'], 
    jsonData2['factory'], 
    jsonData2['section'], 
    jsonData2['data']['status'], 
    jsonData2['data']['temperature'] 
  )


def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1()
    else:
        result = convertFromFormat2()

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
