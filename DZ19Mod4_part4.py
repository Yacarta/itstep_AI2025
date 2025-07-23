import onnxruntime
import torch
from torchvision import transforms
from PIL import Image

# dummy_input = torch.rand(1,3,64,64)
# path = 'model1.onnx'
# torch.onnx.export(
#     model,
#     dummy_input,
#     path,
#     inputs=['image'],
#     output=['result'],
#     dynamic_axes={"image": {0: "batch_size"}, "result": {0: "batch_size"}},
# )

classes = ['Apple Braeburn',
 'Apple Granny Smith',
 'Apricot',
 'Avocado',
 'Banana',
 'Blueberry',
 'Cactus fruit',
 'Cantaloupe',
 'Cherry',
 'Clementine',
 'Corn',
 'Cucumber Ripe',
 'Grape Blue',
 'Kiwi',
 'Lemon',
 'Limes',
 'Mango',
 'Onion White',
 'Orange',
 'Papaya',
 'Passion Fruit',
 'Peach',
 'Pear',
 'Pepper Green',
 'Pepper Red',
 'Pineapple',
 'Plum',
 'Pomegranate',
 'Potato Red',
 'Raspberry',
 'Strawberry',
 'Tomato',
 'Watermelon']

path = 'data/model1.onnx'

session = onnxruntime.InferenceSession(path)

# завантаження зображення
image = Image.open('data/lesson_many/lesson_many/fruits/9.jpg')
image.show()

# обробка зображення

# Визначити конвеєр перетворень
transformer = transforms.Compose([
    transforms.Resize((64, 64)),   # зміна розміру зображення на 64х64 пікселя
    transforms.ToTensor(),  # перевести в тензор
])

image = transformer(image)

# добавити 1 до розміру тензора
image = image.unsqueeze(0)  # 1 має бути під індексом 0

# перевести у масив numpy
image = image.numpy()

# print(image.shape)
# print(image)


results = session.run(
    ['result'],   # назви результатів які треба отримати, або None щоб отримати все
    {'image': image}
)

# отримати результат для першого зображення
result = results[0]

# перевести результат в ймовірності
result = torch.tensor(result)  # переводимо назад у тензор
result = torch.nn.functional.softmax(result, dim=1)
result = result.numpy()

print(result.shape)
print(result)

# отримати максимальну ймовірність та її індекс
result = result[0]  # дістаємо дані для першого(єдиного зображення)

max_proba = result.max()
max_idx = result.argmax()  # індекс максимального елемента
image_class = classes[max_idx]  # назва класу для зображення

print(f'Максимальна ймовірність: {max_proba}')
print(f'Індекс: {max_idx}')
print(f'Назва перелому: {image_class}')