import numpy as np
import torch
from .food_info import get_food_info

from ultralytics.utils.plotting import Annotator, colors

from models.common import DetectMultiBackend
from utils.general import (
    Profile,
    check_img_size,
    cv2,
    non_max_suppression,
    scale_boxes,
)
from utils.augmentations import (
    letterbox,
)
from utils.torch_utils import smart_inference_mode


@smart_inference_mode()
def food_detection(
    im0s
):
    food_info = get_food_info()
    device = torch.device('cpu')
    model = DetectMultiBackend('ckpt/best.pt', device=device, dnn=False, data="ckpt/food.yaml", fp16=False)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size((640, 640), s=stride)

    bs = 1  

    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    dt = (Profile(device=device), Profile(device=device), Profile(device=device))

    
    im = letterbox(im0s, imgsz, stride=stride, auto=pt)[0] 
    im = im.transpose((2, 0, 1))[::-1] 
    im = np.ascontiguousarray(im)  

    with dt[0]:
        im = torch.from_numpy(im).to(model.device)
        im = im.half() if model.fp16 else im.float() 
        im /= 255  
        if len(im.shape) == 3:
            im = im[None]  
        if model.xml and im.shape[0] > 1:
            ims = torch.chunk(im, im.shape[0], 0)

    with dt[1]:
        if model.xml and im.shape[0] > 1:
            pred = None
            for image in ims:
                if pred is None:
                    pred = model(image, augment=False, visualize=False).unsqueeze(0)
                else:
                    pred = torch.cat((pred, model(image, augment=False, visualize=False).unsqueeze(0)), dim=0)
            pred = [pred, None]
        else:
            pred = model(im, augment=False, visualize=False)

    with dt[2]:
        pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)

    total_calorie = 0
    labels = []
    for i, det in enumerate(pred): 
        im0 = im0s.copy()

        annotator = Annotator(im0, line_width=3, example=str(names))
        if len(det):
            det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
            for *xyxy, conf, cls in reversed(det):
                c = int(cls)  # integer class
                label =food_info[c][0]# names[c] if False else f"{names[c]}"
                labels.append(label)
                total_calorie+=food_info[c][1]
                c = int(cls)  # integer class
                # label = None if False else (names[c] if False else f"{names[c]} {conf:.2f}")
                annotator.box_label(xyxy, label, color=colors(c, True))
        im0 = annotator.result()
    return im0, labels, total_calorie