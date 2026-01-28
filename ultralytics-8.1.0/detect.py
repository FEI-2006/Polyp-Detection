from ultralytics import YOLO

if __name__ == '__main__':
    # 加载模型
    model = YOLO(r'/root/autodl-tmp/polyp_YOLO/ultralytics-8.1.0/runs/detect/BEST_KVASIR/weights/best.pt')
    model.predict(
        source=r'/root/autodl-tmp/polyp_YOLO/ultralytics-8.1.0/datasets/kvasir-seg/images/train/72.jpg',
        save=True,  
        imgsz=640,  
        conf=0.25,  
        iou=0.1,    
        device="0",
        show=False, 
        project='/root/autodl-tmp/polyp_YOLO/ultralytics-8.1.0/runs/picture',  # 项目名称（可选）
        name='exp', 
        save_txt=False,  
        save_conf=False, 
        save_crop=False, 
        show_labels=True,  
        show_conf=True,  
        vid_stride=1,  
        line_width=3, 
        visualize=False,  
        augment=False,  
        agnostic_nms=False, 
        retina_masks=False,  
        boxes=True,  
    )
