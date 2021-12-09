SAVE CODE 09/12/2021 À 12H00

AWSTemplateFormatVersion: '2010-09-09' 
Transform: 'AWS::Serverless-2016-10-31' 

Parameters: 
  AppName: 
    Type: String 
    Default: campus-app 
  Stage: 
    Type: String 
    Default: dev 
  DevicesTableName:
    Type: String 
    Default: campus-l3-dev-app-fanny-table-devices-dev

Resources: 
  Api: 
    Type: AWS::Serverless::Api 
    Properties: 
      Cors: 
        AllowMethods: "'POST, GET, OPTIONS, PUT'" 
        AllowHeaders: "'Accept, Content-Type, Content-Length, Authorization, X-Api-Key'" 
        AllowOrigin: "'*'" 
        MaxAge: "'600'" 
      Name: 
        Fn::Sub: ${AppName}-api-${Stage} 
      StageName: !Ref Stage
      DefinitionBody: 
        Fn::Transform: 
          Name: AWS::Include 
          Parameters: 
            Location: specification/openapi.yml

  ApiRole: 
    Type: AWS::IAM::Role 
    Properties: 
      Path: 
        Fn::Sub: /${Stage}/${AppName}/serviceRoles/ 
      RoleName: 
        Fn::Sub: ${AppName}-api-execution-role-${Stage} 
      AssumeRolePolicyDocument: 
        Version: '2012-10-17' 
        Statement: 
          - Effect: Allow 
            Principal: 
              Service: 
                - apigateway.amazonaws.com 
            Action: sts:AssumeRole 
      Policies: 
        - PolicyName: 
            Fn::Sub: ${AppName}-api-execution-role-policy-${Stage} 
          PolicyDocument: 
            Version: '2012-10-17' 
            Statement: 
              - Effect: Allow 
                Action: 
                  - lambda:InvokeFunction 
                Resource: 
                  Fn::Sub: ${GetDevices.Arn}

  GetDevicesRole: 
    Type: AWS::IAM::Role 
    Properties: 
      Path: 
        Fn::Sub: /${Stage}/${AppName}/serviceRoles/ 
      RoleName: 
        Fn::Sub: ${AppName}-get-devices-role-${Stage} 
      AssumeRolePolicyDocument: 
        Version: '2012-10-17' 
        Statement: 
          - Effect: Allow 
            Principal: 
              Service: 
                - lambda.amazonaws.com 
            Action: sts:AssumeRole 
      Policies: 
        - PolicyName:
            Fn::Sub: ${AppName}-get-devices-role-policy-dynamodb-${Stage}
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:Query
                  - dynamodb:Scan
                Resource: 
                  Fn::Sub: ${devicesTable.Arn}

  # GetDevicesLogGroup:
  #   Type: AWS::Logs::LogGroup
  #   DependsOn: [ GetDevices ]
  #   Properties:
  #     LogGroupName: !Sub /aws/lambda/${GetDevices}
  #     RetentionInDays: 7

  devicesTable: 
    Type: AWS::DynamoDB::Table
    Properties: 
      AttributeDefinitions: 
        - 
          AttributeName: "deviceId"
          AttributeType: "S"
        - 
          AttributeName: "deviceName"
          AttributeType: "S"
        - 
          AttributeName: "deviceType"
          AttributeType: "S"
      KeySchema: 
        - 
          AttributeName: "deviceId"
          KeyType: "HASH"

      GlobalSecondaryIndexes:
        -
          IndexName: "deviceProperties"
          KeySchema:
            -
              AttributeName: "deviceName"
              KeyType: "HASH"
            -
              AttributeName: "deviceType"
              KeyType: "RANGE"
          Projection:
            ProjectionType: ALL 
          ProvisionedThroughput: 
            ReadCapacityUnits: "5"
            WriteCapacityUnits: "5"

      ProvisionedThroughput: 
        ReadCapacityUnits: "5"
        WriteCapacityUnits: "5"
      TableName: !Ref DevicesTableName
        # Fn::Sub: ${AppName}-table-devices-${Stage}

  GetDevices: 
      Type: AWS::Serverless::Function 
      Properties: 
        Tracing: Active 
        Runtime: python3.8 
        PackageType: Zip 
        FunctionName: 
          Fn::Sub: ${AppName}-get-devices-${Stage} 
        Description: Get the list of devices 
        CodeUri: ./src/get
        Handler: devices.get_devices
        Role:
          Fn::Sub: ${GetDevicesRole.Arn}
        Environment:
          Variables:
            # DEVICES_TABLE: !Ref devicesTable
            DEVICES_TABLE: !Ref DevicesTableName

    # GetDevice: 
    #   Type: AWS::Serverless::Function 
    #   Properties: 
    #     Tracing: Active 
    #     Runtime: python3.8 
    #     PackageType: Zip 
    #     FunctionName: 
    #       Fn::Sub: ${AppName}-get-device-${Stage} 
    #     Description: Get a single device by id
    #     CodeUri: ./src/get
    #     Handler: device.get_device
