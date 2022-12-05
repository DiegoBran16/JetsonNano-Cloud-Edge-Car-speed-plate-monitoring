import json 
import boto3 
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
import smtplib
 
 
def lambda_handler(event, context):
    image_name=event['IDaws'] 
    speed = event['dataspeedaws']  
    multa = Sistema_multa(speed)
    bucket='carimages-traffic-jetson-nano-4gb'
    plateimage=image_name+'.jpg'
    plate=call_rekognition(plateimage,bucket)
    plate = normalize(plate)
    Dynamo_write(image_name,speed,plate,multa)
    time_aux = get_timestamp(image_name)
    if multa == 'Si':
        send_mail(plate, time_aux, speed) 
    

 
    #return plate 
    
    return {
        'statusCode': 200
        
    }
    
def call_rekognition(plateimage, bucket):
    plate = 'AAAA'
    
    client_rekognition = boto3.client('rekognition', region_name='us-east-2')

    response=client_rekognition.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':plateimage}})
    
    allTextDetections =response['TextDetections']
     
    for i in range(len(allTextDetections)):
        TextObject = allTextDetections[i]
        print(TextObject)
        
        if TextObject['Type']=="LINE" and len(TextObject['DetectedText']) >= 6 :
            plate = TextObject['DetectedText'] 
            plate = plate.replace(" ", "-") 
           #identificar en donde esta el espacio o el guion, y luego de ahi tomar donde vamos a tomar los caracteres
            character = '-'
            index = plate.find(character)
            plate = plate[(index-1):(index+6)] 
                    
    return plate

    

def get_timestamp(image_name):
    aux_name = 0
    for i in range(len(image_name)):
        if image_name[i]=="_":
            aux_name = (i+1)
    return image_name[aux_name:]
        
    
    
def Dynamo_write(image_name,speed,plate,multa):
#     
    dynamoDB = boto3.resource('dynamodb')
    dynamoTable = dynamoDB.Table('Detected-Cars-DB')
    dynamoTable.put_item(
        Item={
            'ID':image_name,
            'timestamp': get_timestamp(image_name),
            'Plate':plate,
            'Speed':str(speed),
            'ImageName':image_name+'.jpg',
            'Multa': multa
        }
    )

def normalize(plate):
    replacements = (
        ("á", "a"),
        ("é", "e"), 
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("Á", "a"),
        ("É", "e"),
        ("Í", "i"),
        ("Ó", "o"),
        ("Ú", "u"),
    )
    for a, b in replacements:
        plate = plate.replace(a, b)
        upper_P = plate.upper()
    return upper_P

def Sistema_multa(speed):
    rapidez = float(speed)
    rapidez_aceptada = 35
    multa = ""
    if rapidez > rapidez_aceptada:
        multa = "Si"
    else:
        multa = "No"
        
    return multa

def send_mail(plate, timestamp, speed):
    msg = MIMEMultipart() 
    dynamodb2 = boto3.resource('dynamodb')
    tablaDuenos = dynamodb2.Table('CarOwners')
    getEmail = tablaDuenos.get_item(Key = {'Matricula': plate},AttributesToGet = ['Email'])
    EmailItem = getEmail['Item']
    email = EmailItem['Email']
    #email = getEmail
    getFirstName = tablaDuenos.get_item(Key = {'Matricula': plate},AttributesToGet = ['FirstName'] )
    FirstNameItem = getFirstName['Item']
    firstname = FirstNameItem['FirstName']
    #firstname = getFirstName
    getSurname = tablaDuenos.get_item(Key = {'Matricula': plate},AttributesToGet = ['FirstSurname'] )
    SurnameItem = getSurname['Item']
    surname = SurnameItem['FirstSurname'] 
    #surname = getSurname
    time_usuario = timestamp
    rapidez_usuario = speed
     
    message = 'CIUDADANO ' + str(firstname) + ' ' + str(surname) + ' USTED INCLUMPLIO CON EL LÍMITE DE RAPIDEZ ESTABLECIDO AL MANEJAR A ' + str(speed) + ' KM/H'
    password = 'c'
    msg['From']='secastroa@correo.url.edu.gt'
    msg['To']=email
    msg['Subject']='Aviso de Multa'
    #secastroa@correo.url.edu.gt
    msg.attach(MIMEText(message)) 
    server=smtplib.SMTP(host='smtp.office365.com', port =587)
    #smtp.office365.com    - 587
    server.starttls()
    server.login(msg['From'],password)
    server.sendmail(msg['From'],msg['To'],msg.as_string())  
    server.quit()  
    print("Correo Enviado")
      
     
     