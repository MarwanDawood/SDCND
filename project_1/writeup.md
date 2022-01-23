## Project overview
### Description:
Objective is to detect and classify vehicles, pedestrians and cyclist.
Using the open Waymo dataset, transfer learning from a pretrained model to Single-Shot Detection ResNet model shall be done to save effort in creating the new model.
The Waymo data tfrecords are large, hence a script will be used to extract the useful information into segments.

### Project steps are:
1. Data is already downloaded after being segmented, if not run
`python download_process.py --data_dirdata/waymo/training_and_validation`
2. Split the data into 'data' folder by running
`python create_splits.py --data_dir /home/workspace/data/`
3. Install Chrome browser by running
`sudo apt-get install chromium-browser`
4. Analyse exploratory data in 'analysis' folder by running
`./analysis/launch_jupyter.sh`
5. Configure the pipeline configuration file by running
`python edit_config.py --train_dir /home/workspace/data/train/ --eval_dir /home/workspace/data/val/ --batch_size 4 --checkpoint ./training/pretrained-models/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/checkpoint/ckpt-0 --label_map analysis/label_map.pbtxt`
6. Move the generated file 'pipeline_new.config' into 'training/reference/' and modify the segments paths inside it to the existing ones after the splitting.
7. Open tensorboard statistics by running the package
`python -m tensorboard.main --logdir experiments/reference/` then `tensorboard --logdir=training`
8. Train the model by running
`python training/model_main_tf2.py --model_dir=training/reference/ --pipeline_config_path=training/reference/pipeline_new.config`
9. Evaluate the model by running
`python training/model_main_tf2.py --model_dir=training/reference/ --pipeline_config_path=training/reference/pipeline_new.config --checkpoint_dir=training/reference/`
10. Improve the performance.
11. Create an animation.

### Importance of object detection in SDC:
Modern SDC use several sensors for object detection and classificaion, the latter one can be done only by cameras, their output is then fed to neural networks to achieve that.
This is crucial for sign recognition, differentiation between different objects here provides the ability to predict their behavior.

## Dataset
### Dataset analysis
This section should contain a quantitative and qualitative description of the dataset. It should include images, charts and other visualizations.
- There are 2 classes, cars, pedestrians.
- Trucks are classified as cars.
- Low camera resolution.
- Images are of low contrast (narrow pixel value distribution).
- There are no/few occlusion ojects.
- Most of the objects are far.
- Most of the car pictures are taken from front or rear side.
- No/few images with very bright/sunny light.

### Cross validation
This section should detail the cross validation strategy and justify your approach.
- Hold-out cross-validation is used.
- Since there are 100 data segments, training data is 75% used to train the model and validation data is 15% used to evaluate it.
- The testing dataset is 10% which is used once on the model to protect against data leakage between training and validation datasets.

### Training
Reference experiment
This section should detail the results of the reference experiment. It should includes training metrics and a detailed explanation of the algorithm's performances.

## Improve on the reference
This section should highlight the different strategies you adopted to improve your model. It should contain relevant figures and details of your findings.