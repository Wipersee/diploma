from os import listdir
from os.path import isdir
import random
from PIL import Image
import matplotlib.pyplot as plt
from numpy import savez_compressed
from numpy import asarray
from mtcnn.mtcnn import MTCNN
from numpy import load, array
from numpy import expand_dims
from numpy import asarray, arange
from numpy import savez_compressed
from tensorflow.keras.models import load_model
from scipy import spatial

# model = load_model('../facenet_keras.h5')

# extract a single face from a given photograph
def extract_face(filename, required_size=(160, 160)):
	# load image from file
	image = Image.open(filename)
	# convert to RGB, if needed
	image = image.convert('RGB')
	# convert to array
	pixels = asarray(image)
	# create the detector, using default weights
	detector = MTCNN()
	# detect faces in the image
	results = detector.detect_faces(pixels)
	# extract the bounding box from the first face
	x1, y1, width, height = results[0]['box']
	# bug fix
	x1, y1 = abs(x1), abs(y1)
	x2, y2 = x1 + width, y1 + height
	# extract the face
	face = pixels[y1:y2, x1:x2]
	# resize pixels to the model size
	image = Image.fromarray(face)
	image = image.resize(required_size)
	face_array = asarray(image)
	return face_array
 
# load images and extract faces for all images in a directory
def load_faces(directory):
	faces = list()
	# enumerate files
	for filename in listdir(directory):
		# path
		path = directory + filename
		# get face
		face = extract_face(path)
		# store
		faces.append(face)
	return faces

# get the face embedding for one face
def get_embedding(model, face_pixels):
	# scale pixel values
	face_pixels = face_pixels.astype('float32')
	# standardize pixel values across channels (global)
	mean, std = face_pixels.mean(), face_pixels.std()
	face_pixels = (face_pixels - mean) / std
	# transform face into one sample
	samples = expand_dims(face_pixels, axis=0)
	# make prediction to get embedding
	yhat = model.predict(samples)
	return yhat[0]

# load a dataset that contains one subdir for each class that in turn contains images
def load_dataset(directory, filename):
    X, y = list(), list()
	# enumerate folders, on per class
    for subdir in listdir(directory):
		# path
        path = directory + subdir + '/'
		# skip any files that might be in the dir
        if not isdir(path):
            continue
		# load all faces in the subdirectory
        faces = load_faces(path)
		# create labels
        labels = [subdir for _ in range(len(faces))]
		# summarize progress
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        X.extend(faces)
        y.extend(labels)
        newTrainX = list()
        for face_pixels in faces:
            embedding = get_embedding(model, face_pixels)
            newTrainX.append(embedding)
        newTrainX = asarray(newTrainX)
        savez_compressed(f'npzs/{filename}/{subdir}-embeddings.npz', newTrainX, y)
    return asarray(X), asarray(y)

def load_npzs():
    # load train dataset
    trainX, trainy = load_dataset('dataset/train/', 'train')
    # load test dataset
    testX, testy = load_dataset('dataset/test/', 'test')

def verify(input_image, embeddings, detection_threshold, verification_threshold):
    # Build results array
    results = []
    for validation_image in embeddings:
        # Make Predictions
        result = spatial.distance.cosine(input_image, validation_image)
        results.append(result)

    # Detection Threshold: Metric above which a prediciton is considered positive
    detection = sum(array(results) < detection_threshold)
    # Verification Threshold: Proportion of positive predictions / total positive samples
    verification = detection / len(embeddings)
    verified = verification > verification_threshold

    return results, verified

DETECTION_THRESHOLD = 0.3
VERIFICATION_THRESHOLD = 0.6

def evaluate():
    counts_positive = {}
    counts_negtive = {}
    folders = listdir('npzs/test')
    for filename in folders:
        data_train = load(f"npzs/train/{filename}")["arr_0"]
        data_test = load(f"npzs/test/{filename}")['arr_0']
        count_per_person = 0
        for embedding in data_test:
            results, verified = verify(
                input_image=embedding,
                embeddings=data_train,
                detection_threshold=DETECTION_THRESHOLD,
                verification_threshold=VERIFICATION_THRESHOLD,
            )
            if verified:
                count_per_person+=1
        counts_positive[filename.split('-')[0]] = (count_per_person, len(data_test))


    for filename in folders:
        negative = random.choice(list(filter(lambda x: x!= filename, folders)))
        data_train = load(f"npzs/train/{filename}")["arr_0"]
        data_test = load(f"npzs/test/{negative}")['arr_0']
        count_per_person = 0
        for embedding in data_test:
            results, verified = verify(
                input_image=embedding,
                embeddings=data_train,
                detection_threshold=DETECTION_THRESHOLD,
                verification_threshold=VERIFICATION_THRESHOLD,
            )
            if not verified:
                count_per_person+=1
        counts_negtive[filename.split('-')[0]] = (count_per_person, len(data_test))
    print(counts_negtive)
    print(counts_positive)

    tp = sum([counts_positive.get(name)[0] for name in counts_positive.keys()])
    fn = sum([counts_positive.get(name)[1] for name in counts_positive.keys()]) - tp
    tn = sum([counts_negtive.get(name)[0] for name in counts_negtive.keys()])
    fp = sum([counts_negtive.get(name)[1] for name in counts_negtive.keys()]) - tn

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    fallout = tn / (tn + fp)
    f_measure = (2 * tp) / (2*tp + fp + fn)
    accurancy = (tp + tn) / (tp + tn + fp + fn)
    error_rate = (fp + fn) / (tp + tn + fp + fn)
    sensitivity = tp / (tp + fn)

    print(f"""
    Report:
    Precision = {precision};
    Recall = {recall};
    Fallout = {fallout};
    F-measure = {f_measure};
    Accuranct = {accurancy};
    Error rate = {error_rate};
    Sensitivity = {sensitivity};
    """)

    font = {'family' : 'Times New Roman',
            'size'   : 10}

    plt.rc('font', **font)

    plt.subplot(1, 2, 1)
    plt.bar(counts_positive.keys(), [x[0] / x[1] *100 for x in counts_positive.values()], color='green')
    plt.xlabel('Person name')
    plt.ylabel('Percent of true positive varification')


    plt.subplot(1, 2, 2)
    plt.bar(counts_negtive.keys(), [x[0] / x[1] *100 for x in counts_negtive.values()], color='navy')
    plt.xlabel('Person name')
    plt.ylabel('Percent of true negative varification')

    plt.show()

evaluate()