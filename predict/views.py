import base64

from rest_framework.views import APIView
from rest_framework.response import Response

from ultralytics import YOLO

model = YOLO("predict/ml/YOLOv8n-pose/best.pt")
upload_path = "predict/upload/"
predicted_path = "media/"


def predict(filename):
    results = model(f"{upload_path}{filename}")

    # Process results list
    for result in results:
        # boxes = result.boxes  # Boxes object for bounding box outputs
        # masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        print(keypoints)
        # probs = result.probs  # Probs object for classification outputs
        # obb = result.obb  # Oriented boxes object for OBB outputs
        # result.show()  # display to screen
        result.save(filename=f"{predicted_path}{filename}")  # save to disk
    return results


# Create your views here.


class PredictView(APIView):

    @staticmethod
    def post(request):
        image_base64 = base64.b64decode(request.data['image_base64'])
        filepath = f"{upload_path}{request.data['filename']}"
        with open(filepath, 'wb') as f:
            f.write(image_base64)
            f.close()
        predict(request.data['filename'])
        image_base64_predicted = base64.b64encode(open(f"{predicted_path}{request.data['filename']}", "rb").read())
        return Response({'image_base64_predicted': image_base64_predicted})
