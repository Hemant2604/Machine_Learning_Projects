import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import json
import pickle
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Dropout, Input
from keras.optimizers import SGD

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents data
with open('data.json', 'r') as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignore_words = ['?', '!']

# Process intents
for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize, lowercase, and remove duplicates
words = sorted(set(lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words))
classes = sorted(classes)

print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique lemmatized words", words)

# Save words and classes
pickle.dump(words, open('texts.pkl', 'wb'))
pickle.dump(classes, open('labels.pkl', 'wb'))

# Create training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in doc[0]]
    
    for w in words:
        bag.append(1 if w in pattern_words else 0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# Debugging print to check input and output lengths
for t in training:
    print(f'Input vector length: {len(t[0])}, Output vector length: {len(t[1])}')

# Shuffle and split data
random.shuffle(training)
train_x = np.array([t[0] for t in training], dtype=np.float32)
train_y = np.array([t[1] for t in training], dtype=np.float32)

print("Training data created")
print(f'train_x shape: {train_x.shape}')
print(f'train_y shape: {train_y.shape}')

# Create the model
model = Sequential([
    Input(shape=(len(train_x[0]),)),  # Explicit input layer
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(len(train_y[0]), activation='softmax')
])

# Use the correct optimizer for Keras 3
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save the model
model.save('model.h5')
print("Model created successfully!")
