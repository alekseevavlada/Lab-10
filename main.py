import json
import pyaudio
import requests
import vosk
import cv2


model = vosk.Model('vosk-model-small-ru-0.22')
response = requests.get('https://dog.ceo/api/breeds/image/random')
data = json.loads(response.content)

record = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=16000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


# Сохранение картинки
def save_image():
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    image_url = response.json()['message']
    p = requests.get(image_url)
    out = open('img.jpg', 'wb')
    out.write(p.content)
    out.close()
    print('Ваше собачка теперь сохранена у Вас')


def get_dog_image():
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    image_url = response.json()['message']
    # Отображаем изображение
    print(image_url)
    p = requests.get(image_url)
    out = open('img.jpg', 'wb')
    out.write(p.content)
    out.close()
    print('Ваш милашик готов')
    img = cv2.imread('img.jpg')
    cv2.imshow('Doggy', img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()


def name():
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    data = response.json()
    breeds = data['message']
    breeds = breeds.split('/')
    print('Порода Вашей собачки:', breeds[-2])


# Получение разрешения картинки
def get_image_resolution():
    img = cv2.imread('img.jpg')
    width, height, _ = img.shape
    resolution = str(width) + " x " + str(height)
    print(resolution)


for text in listen():
    if 'показать' in text:
        get_dog_image()
    elif 'сохранить' in text:
        save_image()
    elif 'описание' in text:
        get_breed_description()
    elif 'назвать породу' in text:
        name()
    elif 'разрешения' in text:
        get_image_resolution()
    elif 'выход' in text:
        break
    else:
        print('Не удалось распознать команду')
