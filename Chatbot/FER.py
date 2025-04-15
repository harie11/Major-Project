from deepface import DeepFace # type: ignore
import cv2 # type: ignore
import time

emolist = []

def emodetect(image_path, max_retries=1):
    while max_retries:
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Image not found or path is incorrect.")

            # Perform emotion analysis
            prediction = DeepFace.analyze(img, actions=['emotion'])
            dominant_emotion = prediction[0]['dominant_emotion']
            print(f" Dominant Emotion in FER: {dominant_emotion}")

            # Maintain a rolling list of emotions
            if len(emolist) > 5:
                emolist.pop(0)
            emolist.append(dominant_emotion)

            return dominant_emotion

        except Exception as e:
            #print(f" Error occurred: {e}")
            return None

def capture_and_detect_emotion():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print(" Error: Could not access the webcam.")
        return

    #print(" Capturing image...")
    ret, frame = camera.read()

    if not ret:
        print(" Error: Failed to capture image.")
        camera.release()
        return

    # Define image save path
    save_path = f"C:/Users/nandh/Downloads/tensor/sentiment/images/captured_images.jpg"
    #test_path = f"C:/Users/nandh/Downloads/tensor/sentiment/images/sad.jpg"
    cv2.imwrite(save_path, frame)
    #print(" Image saved successfully.")

    # Perform emotion detection
    detected_emotion = emodetect(save_path)
    

    camera.release()
    cv2.destroyAllWindows()
    return detected_emotion

def run_every_5_seconds():
    while True:
        capture_and_detect_emotion()
        time.sleep(5)

# Run the function

# Example call
'''
if __name__ == "__main__":
    run_every_5_seconds()
'''