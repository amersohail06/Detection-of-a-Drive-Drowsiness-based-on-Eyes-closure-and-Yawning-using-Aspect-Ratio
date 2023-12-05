from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import sys
import playsound as play
from dbconfig import DBConnection
class VisualBehaviour(object):

	def __init__(self):
		self.EYE_AR_THRESH = 0.28
		self.EYE_AR_CONSEC_FRAMES = 48
		self.MOUTH_THER = 0.48
		self.NOSE_LENGTH_UP = 1.1
		self.NOSE_LENGTH_DOWN = 0.7
		self.NOSE_AVERAGE = 0
		self.COUNT_FRAMES = 20

	def eye_aspect_ratio(self,eye):
		A = dist.euclidean(eye[1], eye[5])
		B = dist.euclidean(eye[2], eye[4])
		C = dist.euclidean(eye[0], eye[3])
		ear = (A + B) / (2.0 * C)
		return ear

	def mou_aspect_ratio(self,mou):
		A = dist.euclidean(mou[2], mou[10])
		B = dist.euclidean(mou[3], mou[9])
		C = dist.euclidean(mou[4], mou[8])
		D = dist.euclidean(mou[6], mou[0])
		mou_np = (A + B + C) / (3.0 * D)
		return mou_np

	def nos_aspect_ratio(self,nos):
		A = dist.euclidean(nos[3], nos[0])
		nos_np = A / self.NOSE_AVERAGE
		return nos_np / 75

	def start(self,dr_uid):
		try:
			database = DBConnection.getConnection()
			cursor = database.cursor()
			state = "Normal"
			ap = argparse.ArgumentParser()
			ap.add_argument("-w", "--webcam", type=int, default=0,
							help="index of webcam on system")
			args = vars(ap.parse_args())

			COUNTER = 0
			ALARM_ON = False

			print("[INFO] loading facial landmark predictor...")
			detector = dlib.get_frontal_face_detector()
			predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

			(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
			(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
			(sMou, eMou) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
			(sNos, eNos) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]

			print("[INFO] starting video stream...")

			vs = VideoStream(src=args["webcam"]).start()

			print("[INFO] SetUp loading...")
			print("[INFO} Please keep ur HEAD STRAIGHT toward's camera")
			time.sleep(5)
			print("[INFO] Taking values please wait...")

			# Calculate Nose Length
			for i in range(75):
				frame = vs.read()
				frame = imutils.resize(frame, width=450)
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				rects = detector(gray, 0)
				for rect in rects:
					B = 0.0
					shape = predictor(gray, rect)
					shape = face_utils.shape_to_np(shape)
					nose = shape[sNos:eNos]
					A = dist.euclidean(nose[3], nose[0])
					B += A
					self.NOSE_AVERAGE = B
			# print("Avrg: ", NOSE_AVERAGE)
			self.NOSE_AVERAGE = self.NOSE_AVERAGE / 75
			print("NOSE_AVERAGE: ", self.NOSE_AVERAGE)

			count = 0
			count1 = 0
			while True:
				frame = vs.read()
				frame = imutils.resize(frame, width=450)
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				rects = detector(gray, 0)

				for rect in rects:
					shape = predictor(gray, rect)
					shape = face_utils.shape_to_np(shape)

					leftEye = shape[lStart:lEnd]
					rightEye = shape[rStart:rEnd]
					leftEAR = self.eye_aspect_ratio(leftEye)
					rightEAR = self.eye_aspect_ratio(rightEye)
					mouth = shape[sMou:eMou]
					Mouth = self.mou_aspect_ratio(mouth)
					nose = shape[sNos:eNos]
					Nose = self.nos_aspect_ratio(nose)
					print('Nose0oo', Nose)

					ear = (leftEAR + rightEAR) / 2.0
					leftEyeHull = cv2.convexHull(leftEye)
					rightEyeHull = cv2.convexHull(rightEye)
					mouthHull = cv2.convexHull(mouth)
					noseHull = cv2.convexHull(nose)
					cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
					cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
					cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
					cv2.drawContours(frame, [noseHull], -1, (0, 255, 0), 1)

					if Nose > self.NOSE_LENGTH_UP or Nose < self.NOSE_LENGTH_DOWN:
						# print("Head Bending")
						count += 1
					else:
						count = 0
					if Mouth >= self.MOUTH_THER:
						count1 += 1
					else:
						count1 = 0
					if count > self.COUNT_FRAMES:
						# print("NLR: ", Nose)
						cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
									cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
						cv2.putText(frame, "Head Bending!", (140, 300),
									cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
						state = "Head Bending"
						play.playsound("MP3.wav")
					if count1 > self.COUNT_FRAMES:
						# print("ALERT Yawning")
						# print("MOR: ", Mouth)
						cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
									cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
						cv2.putText(frame, "Yawning!", (290, 300),
									cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
						state = "Yawning"
						play.playsound("MP3.wav")

					if ear < self.EYE_AR_THRESH:
						COUNTER += 1
						if COUNTER >= self.EYE_AR_CONSEC_FRAMES:
							# print("EAR: ", ear)
							cv2.putText(frame, "Eye Closed!", (10, 300),
										cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
							cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
										cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
							state = "Eye Closed"
							play.playsound("MP3.wav")
					else:
						COUNTER = 0

					query = "insert into driver_history values(%s,%s,%s,%s,%s,now())"
					values = (dr_uid, str(ear), str(Mouth), str(Nose), str(state))
					cursor.execute(query, values)
					database.commit()

				cv2.imshow("Frame", frame)
				key = cv2.waitKey(10) & 0xFF
				if key == 27:
					break

			cv2.destroyAllWindows()
			vs.stop()
		except Exception as e:
			print("Error=", e.args[0])
			tb = sys.exc_info()[2]
			print(tb.tb_lineno)

	#exit(0)

if __name__=="__main__":
	d=VisualBehaviour()
	d.start()


