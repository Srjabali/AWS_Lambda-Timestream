import boto3
import time

def lambda_handler(event, context):
    iCurrentValue = 0
    
    for reported in event:
        items = event[reported]
        for item in items:
            try:
                if item == "AM..4:1-1":
                    iCurrentValue = int(items[item], 16)
            except Exception:
                iCurrentValue = 0

    current_time = str(round(time.time() * 1000))

    response = 'value: ' + str(iCurrentValue) + ' time_ms: ' + current_time
    
    dimensions = [
        {'Name': 'region', 'Value': 'your_region'},
    ]
    
    temperature_value = {
        'Dimensions': dimensions,
        'MeasureName': 'temperature',
        'MeasureValue': str(iCurrentValue),
        'MeasureValueType': 'BIGINT',
        'Time': current_time
    }
    
    #Contenido de la tabla
    records = [temperature_value]
    
    client = boto3.client('timestream-write')

    try:
        result = client.write_records(DatabaseName='testTimestreamDB', TableName='datosPLC',
                                      Records=records, CommonAttributes={})
        print("WriteRecords Status: [%s]" % result['ResponseMetada']['HTTPStatusCode'])
    except Exception as err:
        print("Error awb logo:", err)
        
    return response