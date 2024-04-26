import os
from xml.etree import ElementTree as ET

def convert_coco_to_yolo(coco_xml_dir, yolo_txt_dir, class_mapping):
    """Converts COCO-formatted XML annotations to YOLO text format.

    Args:
        coco_xml_dir (str): Path to the directory containing COCO XML files.
        yolo_txt_dir (str): Path to the output directory for YOLO text files.
        class_mapping (dict): Dictionary mapping COCO class names to YOLO class IDs.
    """

    for filename in os.listdir(coco_xml_dir):
        if filename.endswith(".xml"):
            xml_path = os.path.join(coco_xml_dir, filename)
            yolo_txt_path = os.path.join(yolo_txt_dir, filename.replace(".xml", ".txt"))

            # Parse COCO XML using ElementTree
            with open(xml_path, 'r') as file:
                xml_data = ET.fromstring(file.read())

            img_width = int(xml_data.find('size').find('width').text)
            img_height = int(xml_data.find('size').find('height').text)

            with open(yolo_txt_path, 'w') as file:
                for obj in xml_data.findall('object'):
                    class_name = obj.find('name').text
                    class_id = class_mapping.get(class_name)

                    if class_id is not None:
                        bndbox = obj.find('bndbox')
                        x_min = int(bndbox.find('xmin').text)
                        y_min = int(bndbox.find('ymin').text)
                        x_max = int(bndbox.find('xmax').text)
                        y_max = int(bndbox.find('ymax').text)

                        # Calculate normalized bounding box coordinates for YOLO
                        x_center = (x_min + x_max) / 2 / img_width
                        y_center = (y_min + y_max) / 2 / img_height
                        width = (x_max - x_min) / img_width
                        height = (y_max - y_min) / img_height

                        # Write YOLO annotation line with proper formatting
                        file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

# Example usage
class_mapping = {
    'car': 0,
    'human':1
   
}

coco_xml_dir = 'xml/annotation/dir'
yolo_txt_dir = 'txt/annotationsave/dir'

convert_coco_to_yolo(coco_xml_dir, yolo_txt_dir, class_mapping)