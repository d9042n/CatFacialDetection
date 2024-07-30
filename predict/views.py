import base64

from rest_framework.response import Response
from rest_framework.views import APIView
from ultralytics import YOLO

model = YOLO("predict/ml/YOLOv8n-pose/best.pt")
upload_path = "predict/upload/"
predicted_path = "media/"
classes = ['Left_Eye', 'Right_Eye', 'Mouth', 'Left_Ear_1', 'Left_Ear_2', 'Left_Ear_3', 'Right_Ear_1', 'Right_Ear_2',
           'Right_Ear_3']


def predict(filename):
    keypoints_return = []
    results = model(f"{upload_path}{filename}")

    # Process results list
    for result in results:
        # boxes = result.boxes  # Boxes object for bounding box outputs
        # masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        # probs = result.probs  # Probs object for classification outputs
        # obb = result.obb  # Oriented boxes object for OBB outputs
        # result.show()  # display to screen
        result.save(filename=f"{predicted_path}{filename}")  # save to disk
        keypoints_return.append(keypoints.xy.tolist()[0])
    return results, keypoints_return


# Create your views here.


class PredictView(APIView):

    @staticmethod
    def post(request):
        image_base64 = base64.b64decode(request.data['image_base64'])
        filepath = f"{upload_path}{request.data['filename']}"

        with open(filepath, 'wb') as f:
            f.write(image_base64)
            f.close()

        _result, keypoints = predict(request.data['filename'])
        image_base64_predicted = base64.b64encode(open(f"{predicted_path}{request.data['filename']}", "rb").read())

        return Response(
            {'keypoints': dict(zip(classes, keypoints[0])), 'image_base64_predicted': image_base64_predicted})
