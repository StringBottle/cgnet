
import os
import cv2 

import os.path as osp 
import numpy as np 
import cityscapesscripts.helpers.labels as CSLabels

from glob import glob 


class CityscapesDatset: 
    
    """
    Cityscapes dataset.
    The ``img_suffix`` is fixed to '_leftImg8bit.png' and ``seg_map_suffix`` is
    fixed to '_gtFine_labelTrainIds.png' for Cityscapes dataset.

    Code Reference : 
        [1] https://github.com/open-mmlab/mmsegmentation
    """

    CLASSES = ('road', 'sidewalk', 'building', 'wall', 'fence', 'pole',
               'traffic light', 'traffic sign', 'vegetation', 'terrain', 'sky',
               'person', 'rider', 'car', 'truck', 'bus', 'train', 'motorcycle',
               'bicycle')

    PALETTE = [[128, 64, 128], [244, 35, 232], [70, 70, 70], [102, 102, 156],
               [190, 153, 153], [153, 153, 153], [250, 170, 30], [220, 220, 0],
               [107, 142, 35], [152, 251, 152], [70, 130, 180], [220, 20, 60],
               [255, 0, 0], [0, 0, 142], [0, 0, 70], [0, 60, 100],
               [0, 80, 100], [0, 0, 230], [119, 11, 32]]

    def __init__(self, data_dir, data_type = 'train'):

        self.data_dir = data_dir
        self.img_dir = osp.join(data_dir, 'leftImg8bit_trainvaltest/leftImg8bit', data_type)
        self.ann_dir = osp.join(data_dir, 'gtFine_trainvaltest/gtFine', data_type)
        self.img_suffix = '_leftImg8bit.png'
        self.seg_map_suffix = '_gtFine_labelIds.png'

        # load annotations
        self.img_infos = self.load_img_infos()

        
    def load_img_infos(self): 

        """Load annotation from directory.
        Args:
            img_dir (str): Path to image directory
            img_suffix (str): Suffix of images.
            ann_dir (str|None): Path to annotation directory.
            seg_map_suffix (str|None): Suffix of segmentation maps.
            
        Returns:
            list[dict]: All image info of dataset.

        Code Reference : 
            [1] https://github.com/open-mmlab/mmsegmentation
        """
        img_infos = []
        img_list = []

        for _, _, files in os.walk(self.img_dir):
            for file in files:
                if file.endswith(self.img_suffix):
                    img_list.append(file)


        for img in img_list:
            img_info = dict(filename=img)
            seg_map = img.replace(self.img_suffix, self.seg_map_suffix)
            img_info['ann'] = dict(seg_map=seg_map)
            img_infos.append(img_info)

        return img_infos

    def prepare_img(self, idx): 

        """ Read image from the dataset directory
        Args:
                        
        Returns:
            
        """

        img_filename = self.img_infos[idx]['filename']
        img_prefix = img_filename.split('_')[0]

        img_path = osp.join(self.img_dir, img_prefix, img_filename)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return img

    def prepare_seg_mask(self, idx): 

        """ Read segmentation mask from the annotation directory
        Args:
                        
        Returns:
            
        """

        seg_filename = self.img_infos[idx]['ann']['seg_map']
        seg_prefix = seg_filename.split('_')[0]

        seg_path = osp.join(self.ann_dir, seg_prefix, seg_filename)
        seg = cv2.imread(seg_path, cv2.IMREAD_UNCHANGED)

        return CityscapesDatset._convert_to_label_id(seg)

    @staticmethod
    def _convert_to_label_id(seg):
        """Convert trainId to id for cityscapes."""
        seg_copy = seg.copy()
        for label in CSLabels.labels:
            # print(label.name)
            seg_copy[seg == label.id] = label.trainId
        return seg_copy
            
    

    def __len__ (self) : 

        return len(self.img_infos)

    
    def __getitem__(self, idx):
        
        """Get training/test data after pipeline.

        Args:
            idx (int): Index of data.
        Returns:
            dict: Training/test data (with annotation if `test_mode` is set
                False).
        """
        data = {}
        data['image'] = self.prepare_img(idx)
        data['segmentation_mask'] = self.prepare_seg_mask(idx)

        return data


def test(): 
    data_dir = '/home/sss/UOS-SSaS Dropbox/05. Data/00. Benchmarks/01. cityscapes'
    cityscapes_dataset = CityscapesDatset(data_dir)
    img_infos = cityscapes_dataset.img_infos
    for data in cityscapes_dataset: 
        print(np.unique(data['segmentation_mask'])[-2])
    
    return None 

if __name__ == "__main__" : 
    test()