Project is based on this [Github repository](https://github.com/udacity/nd013-c2-fusion-starter).
# SDCND : Sensor Fusion and Tracking
This is the project for the second course in the  [Udacity Self-Driving Car Engineer Nanodegree Program](https://www.udacity.com/course/c-plus-plus-nanodegree--nd213) : Sensor Fusion and Tracking.

In this project, you'll fuse measurements from LiDAR and camera and track vehicles over time. You will be using real-world data from the Waymo Open Dataset, detect objects in 3D point clouds and apply an extended Kalman filter for sensor fusion and tracking.

<img src="img/img_title_1.jpeg"/>

The project consists of two major parts:
1. **Object detection**: In this part, a deep-learning approach is used to detect vehicles in LiDAR data based on a birds-eye view perspective of the 3D point-cloud. Also, a series of performance measures is used to evaluate the performance of the detection approach.
2. **Object tracking** : In this part, an extended Kalman filter is used to track vehicles over time, based on the lidar detections fused with camera detections. Data association and track management are implemented as well.

The following diagram contains an outline of the data flow and of the individual steps that make up the algorithm.

<img src="img/img_title_2_new.png"/>

Also, the project code contains various tasks, which are detailed step-by-step in the code. More information on the algorithm and on the tasks can be found in the Udacity classroom.

## Project File Structure

📦project<br>
 ┣ 📂dataset --> contains the Waymo Open Dataset sequences <br>
 ┃<br>
 ┣ 📂misc<br>
 ┃ ┣ evaluation.py --> plot functions for tracking visualization and RMSE calculation<br>
 ┃ ┣ helpers.py --> misc. helper functions, e.g. for loading / saving binary files<br>
 ┃ ┗ objdet_tools.py --> object detection functions without student tasks<br>
 ┃ ┗ params.py --> parameter file for the tracking part<br>
 ┃ <br>
 ┣ 📂results --> binary files with pre-computed intermediate results<br>
 ┃ <br>
 ┣ 📂student <br>
 ┃ ┣ association.py --> data association logic for assigning measurements to tracks incl. student tasks <br>
 ┃ ┣ filter.py --> extended Kalman filter implementation incl. student tasks <br>
 ┃ ┣ measurements.py --> sensor and measurement classes for camera and lidar incl. student tasks <br>
 ┃ ┣ objdet_detect.py --> model-based object detection incl. student tasks <br>
 ┃ ┣ objdet_eval.py --> performance assessment for object detection incl. student tasks <br>
 ┃ ┣ objdet_pcl.py --> point-cloud functions, e.g. for birds-eye view incl. student tasks <br>
 ┃ ┗ trackmanagement.py --> track and track management classes incl. student tasks  <br>
 ┃ <br>
 ┣ 📂tools --> external tools<br>
 ┃ ┣ 📂objdet_models --> models for object detection<br>
 ┃ ┃ ┃<br>
 ┃ ┃ ┣ 📂darknet<br>
 ┃ ┃ ┃ ┣ 📂config<br>
 ┃ ┃ ┃ ┣ 📂models --> darknet / yolo model class and tools<br>
 ┃ ┃ ┃ ┣ 📂pretrained --> copy pre-trained model file here<br>
 ┃ ┃ ┃ ┃ ┗ complex_yolov4_mse_loss.pth<br>
 ┃ ┃ ┃ ┣ 📂utils --> various helper functions<br>
 ┃ ┃ ┃<br>
 ┃ ┃ ┗ 📂resnet<br>
 ┃ ┃ ┃ ┣ 📂models --> fpn_resnet model class and tools<br>
 ┃ ┃ ┃ ┣ 📂pretrained --> copy pre-trained model file here <br>
 ┃ ┃ ┃ ┃ ┗ fpn_resnet_18_epoch_300.pth <br>
 ┃ ┃ ┃ ┣ 📂utils --> various helper functions<br>
 ┃ ┃ ┃<br>
 ┃ ┗ 📂waymo_reader --> functions for light-weight loading of Waymo sequences<br>
 ┃<br>
 ┣ basic_loop.py<br>
 ┣ loop_over_dataset.py<br>



## Installation Instructions for Running Locally
### Cloning the Project
In order to create a local copy of the project, please click on "Code" and then "Download ZIP". Alternatively, you may of-course use GitHub Desktop or Git Bash for this purpose.

### Python
The project has been written using Python 3.7. Please make sure that your local installation is equal or above this version.

### Package Requirements
All dependencies required for the project have been listed in the file `requirements.txt`. You may either install them one-by-one using pip or you can use the following command to install them all at once:
`pip3 install -r requirements.txt`

### Waymo Open Dataset Reader
The Waymo Open Dataset Reader is a very convenient toolbox that allows you to access sequences from the Waymo Open Dataset without the need of installing all of the heavy-weight dependencies that come along with the official toolbox. The installation instructions can be found in `tools/waymo_reader/README.md`.

### Waymo Open Dataset Files
This project makes use of three different sequences to illustrate the concepts of object detection and tracking. These are:
- Sequence 1 : `training_segment-1005081002024129653_5313_150_5333_150_with_camera_labels.tfrecord`
- Sequence 2 : `training_segment-10072231702153043603_5725_000_5745_000_with_camera_labels.tfrecord`
- Sequence 3 : `training_segment-10963653239323173269_1924_000_1944_000_with_camera_labels.tfrecord`

To download these files, you will have to register with Waymo Open Dataset first: [Open Dataset – Waymo](https://waymo.com/open/terms), if you have not already, making sure to note "Udacity" as your institution.

Once you have done so, please [click here](https://console.cloud.google.com/storage/browser/waymo_open_dataset_v_1_2_0_individual_files) to access the Google Cloud Container that holds all the sequences. Once you have been cleared for access by Waymo (which might take up to 48 hours), you can download the individual sequences.

The sequences listed above can be found in the folder "training". Please download them and put the `tfrecord`-files into the `dataset` folder of this project.


### Pre-Trained Models
The object detection methods used in this project use pre-trained models which have been provided by the original authors. They can be downloaded [here](https://drive.google.com/file/d/1Pqx7sShlqKSGmvshTYbNDcUEYyZwfn3A/view?usp=sharing) (darknet) and [here](https://drive.google.com/file/d/1RcEfUIF1pzDZco8PJkZ10OL-wLL2usEj/view?usp=sharing) (fpn_resnet). Once downloaded, please copy the model files into the paths `/tools/objdet_models/darknet/pretrained` and `/tools/objdet_models/fpn_resnet/pretrained` respectively.

### Using Pre-Computed Results

In the main file `loop_over_dataset.py`, you can choose which steps of the algorithm should be executed. If you want to call a specific function, you simply need to add the corresponding string literal to one of the following lists:

- `exec_data` : controls the execution of steps related to sensor data.
  - `pcl_from_rangeimage` transforms the Waymo Open Data range image into a 3D point-cloud
  - `load_image` returns the image of the front camera

- `exec_detection` : controls which steps of model-based 3D object detection are performed
  - `bev_from_pcl` transforms the point-cloud into a fixed-size birds-eye view perspective
  - `detect_objects` executes the actual detection and returns a set of objects (only vehicles)
  - `validate_object_labels` decides which ground-truth labels should be considered (e.g. based on difficulty or visibility)
  - `measure_detection_performance` contains methods to evaluate detection performance for a single frame

In case you do not include a specific step into the list, pre-computed binary files will be loaded instead. This enables you to run the algorithm and look at the results even without having implemented anything yet. The pre-computed results for the mid-term project need to be loaded using [this](https://drive.google.com/drive/folders/1-s46dKSrtx8rrNwnObGbly2nO3i4D7r7?usp=sharing) link. Please use the folder `darknet` first. Unzip the file within and put its content into the folder `results`.

- `exec_tracking` : controls the execution of the object tracking algorithm

- `exec_visualization` : controls the visualization of results
  - `show_range_image` displays two LiDAR range image channels (range and intensity)
  - `show_labels_in_image` projects ground-truth boxes into the front camera image
  - `show_objects_and_labels_in_bev` projects detected objects and label boxes into the birds-eye view
  - `show_objects_in_bev_labels_in_camera` displays a stacked view with labels inside the camera image on top and the birds-eye view with detected objects on the bottom
  - `show_tracks` displays the tracking results
  - `show_detection_performance` displays the performance evaluation based on all detected
  - `make_tracking_movie` renders an output movie of the object tracking results

Even without solving any of the tasks, the project code can be executed.

The final project uses pre-computed lidar detections in order for all students to have the same input data. If you use the workspace, the data is prepared there already. Otherwise, [download the pre-computed lidar detections](https://drive.google.com/drive/folders/1IkqFGYTF6Fh_d8J3UjQOSNJ2V42UDZpO?usp=sharing) (~1 GB), unzip them and put them in the folder `results`.

## External Dependencies
Parts of this project are based on the following repositories:
- [Simple Waymo Open Dataset Reader](https://github.com/gdlg/simple-waymo-open-dataset-reader)
- [Super Fast and Accurate 3D Object Detection based on 3D LiDAR Point Clouds](https://github.com/maudzung/SFA3D)
- [Complex-YOLO: Real-time 3D Object Detection on Point Clouds](https://github.com/maudzung/Complex-YOLOv4-Pytorch)


## License
[License](LICENSE.md)


# Midterm writeup: Track 3D-Objects Over Time

## Short recap
### Step 1:
  The target was to extract the range image from the top-mounted LiDAR sensor, then extract the intensity and the range channels afterwards stack them in order to be viewed as a 2D image using OpenCV. The point-cloud frames of this range image is then converted into 3D image using Open3d.

  In sequence 3, starting from frame 13, the frames can be interpretted as a two-way road, in the opposite direction of the road, on the right-hand lane, a van and some sedans can be identified, on the left-hand side lane, a traffic jam queue can be identified which consists of hatch-backs and sedans. The direction of Waymo car contains a truck that pulls a trailer plus other cars.

  The car trailer has some persistent features such as:
  1. the truck towing rod.
  2. the trailer back barrier.
  3. the truck side mirrors.
  4. the tyres.

![truck-trailer](img/trailer.gif "truck-trailer]")


  The car queue have some persistent features such as:
  1. the empty spaces inside the cars.
  2. the license plates place shows no pcl, maybe the reflective material is diffusive.
  3. the side mirrors.
  4. the tyres.

![car-queue](img/queue.png "car-queue]")


### Step 2:
  Convert the point-cloud x-y coordinates into Birds-Eye View (BEV). The intensity channel shall be plotted as well using OpenCV in 2D image showing reflection intensity based on type of material. The height channel shall be plotted as well using OpenCV based on z-axis value of a point.

### Step 3:
  A pre-trianed Feature Pyramid Network Residual Neural Network (FPN ResNet) is used to detect vehicles in the given image frames.
  The NN configuration is as following:
    number of layers = 18
    number of classes = 3
    minimum IoU threshold = 0.6
    image size = 608 x 608

  The detected objects in BEV coordinate space must be converted into metric coordinates in vehicle space (3D bounding boxes).

### Step 4:
  Calculate precision and recall to understand system performance.

## Benefits in camera-lidar fusion compared to lidar-only tracking
Using camera-LiDAR helps eleminating ghost objects, detects traffic signs besides objects color.

## Challenges that a sensor fusion system face in real-life scenarios
Real-time processing is a challenge which I noticed during the project development.

# Final writeup: Track 3D-Objects Over Time

Lidar sensor fusion
![lidar-only-video](img/lidar_tracking_results.gif "lidar-only-video]")

Lidar and camera sensor fusion
![lidar-camera-video](img/lidar_camera_tracking_results.gif "lidar-camera-video]")

## Short recap
### Filter:
Implemented Extended Kalman filter to predict and update tracked objects based on non-linear/linear measurements. RMSE shows high error in the start since the position is unknown in the begining, afterwards the RMSE goes lower as a result of track history.
![kalman-filter](img/30.png "kalman-filter]")

### Track management:
Implemented algorithm to manage tracked objects states as well creation and deletion based on score and covariance of tracked object. RMSE is high since the association between track and measurement is still not implemented.
![track-management](img/31.png "track-management]")

### Association:
Implemented association matrix that links the measurement to the related unassigned tracked object based on Mahalanobis distance, Simple Nearest Neighbor (SNN) and gating. RMSE is low but there are a lot of tentative tracks due to the FOV check is not yet implemented.
![association](img/32.png "association]")

### Camera fusion:
Implemented FOV check in addition to initializing camera measurements. RMSE is low and only confirmed tracks are concluded at the end of the simulation.
![camera-fusion](img/33.png "camera-fusion]")

## Benefits in camera-lidar fusion compared to lidar-only tracking (in theory and in your concrete results)
### In theory:
The RMSE and the amout of detected ghosts shall decrease. The track states shall be decided faster since the covariance would be smaller as a result of using 2 snesors.
### In practice:
Camera calibration affected the measurements that it could not support the LiDAR measurements, even it increased its covariance which lead to lower track score and eventually deleting the track.
No confirmed tracks were detected with the association of camera because of higher covariance, in contrast with the measurements with LiDAR only which gave results conforming to the ground truth.

To convert png images into video, use this command

`ffmpeg -framerate 5 -pattern_type glob -i '*.png' -c:v ffv1 lidar_tracking_results.avi`

## Challenges will a sensor fusion system face in real-life scenarios
Camera calibration is one of the challenges.

## Improving tracking results in the future
1. Use of more optimal distance calculation algorithm such as GNN or PDA.
2. Include z-axis in the calculations for better track estimation.
3. Fuse the data from multiple LiDAR sources.

## Interesting links for further study:
- If you want to deepen your knowledge in sensor fusion, you can take the Sensor Fusion nanodegree:\
  https://www.udacity.com/course/sensor-fusion-engineer-nanodegree--nd313

- Here is the PyTorch documentation, which is extensive, in case you want to learn more about PyTorch:\
  https://pytorch.org/docs/stable/index.html

- The Wikipedia article about Extended Kalman Filters is very informative, in case you want to deepen your knowledge of EKF:\
  https://en.wikipedia.org/wiki/Extended_Kalman_filter

- A reference link for understanding Sensor Fusion and Object Tracking:\
  https://www.mathworks.com/videos/series/understanding-sensor-fusion-and-tracking.html

- [Waymo dataset structure](Waymo_dataset_structure.txt)
