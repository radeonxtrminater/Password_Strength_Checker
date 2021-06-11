from flask import Flask, render_template, flash, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/result/', methods = ["GET", "POST"])
def mainPage():
	if request.method == "POST":
		enteredPassword = request.form['password']


		from sklearn import svm
		import re


		with open('test.txt','w') as test:
			testData = str(enteredPassword) + '|' + str(2)
			test.write(testData)

		
		def parseData(data):
			features = list()
			labels = list()
			passwords = list()

			with open(data) as f:
				for line in f:
					if line != "":

						both = line.replace('\n', '').split("|")
						password = both[0]
						label = both[1]

						feature = [0,0,0,0,0]

						
						lenMin = False; 
						specChar = False 
						ucChar = False 
						numChar = False 

						
						if len(password) > 8:
							lenMin = True

						
						specialMatch = re.search(r'([^a-zA-Z0-9]+)', password, re.M)
						if specialMatch:
							specChar = True

						
						ucMatch = re.search(r'([A-Z])', password, re.M)
						if ucMatch:
							ucChar = True

						
						numMatch = re.search(r'([0-9])', password, re.M)
						if numMatch:
							numChar = True

						
						if lenMin:
							feature[0] = 1

						if specChar and ucChar and numChar:
							feature[1] = 3

						if ucChar and numChar:
							feature[2] = 1

						if specChar and numChar:
							feature[3] = 2

						if specChar and ucChar:
							feature[4] = 2

						features.append(feature)
						labels.append(int(label))
						passwords.append(password)

			return [features,  labels, passwords]


		
		trainingData = parseData( 'training.txt' )
		testingData = parseData( 'test.txt' )

		
		clf = svm.SVC(kernel='linear', C = 1.0)

		
		clf = clf.fit(trainingData[0], trainingData[1])

		
		prediction = clf.predict(testingData[0])

		target = len(testingData[1])
		current = 0
		incorrect = 0
		for index in range(target):
				if(prediction[index] == 0):
					predicted = "Very Weak Password"
				elif(prediction[index] == 1):
					predicted = "Weak Password"
				elif(prediction[index] == 2):
					predicted = "Strong Password"
				elif(prediction[index] == 3):
					predicted = "Very Strong Password"
	return render_template("result.html", predicted = predicted, target = len(trainingData[1]))


if __name__ == "__main__":
    app.run(host= '127.0.0.1')


