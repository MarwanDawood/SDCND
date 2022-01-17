# Writeup: Track 3D-Objects Over Time

Please use this starter template to answer the following questions:

### 1. Write a short recap of the four tracking steps and what you implemented there (filter, track management, association, camera fusion). Which results did you achieve? Which part of the project was most difficult for you to complete, and why?
#### filter:
Implemented Extended Kalman filter to predict and update tracked objects based on non-linear/linear measurements. RMSE shows high error in the start since the position is unknown in the begining, afterwards the RMSE goes lower as a result of track history.
![kalman-filter](img/30.png "kalman-filter]")

#### track management:
Implemented algorithm to manage tracked objects states as well creation and deletion based on score and covariance of tracked object. RMSE is high since the association between track and measurement is still not implemented.
![track-management](img/31.png "track-management]")

#### association:
Implemented association matrix that links the measurement to the related unassigned tracked object based on Mahalanobis distance, Simple Nearest Neighbor (SNN) and gating. RMSE is low but there are a lot of tentative tracks due to the FOV check is not yet implemented.
![association](img/32.png "association]")

#### camera fusion:
Implemented FOV check in addition to initializing camera measurements. RMSE is low and only confirmed tracks are concluded at the end of the simulation.
![camera-fusion](img/33.png "camera-fusion]")

### 2. Do you see any benefits in camera-lidar fusion compared to lidar-only tracking (in theory and in your concrete results)?
#### in theory:
The RMSE and the amout of detected ghosts shall decrease. The track states shall be decided faster since the covariance would be smaller as a result of using 2 snesors.
#### in practice:
Camera calibration affected the measurements that it could not support the LiDAR measurements, even it increased its covariance which lead to lower track score and eventually deleting the track.
No confirmed tracks were detected with the association of camera because of higher covariance, in contrast with the measurements with LiDAR only which gave results conforming to the ground truth.

![lidar-only-video](img/lidar_tracking_results.avi "lidar-only-video]")
![lidar-camera-video](img/lidar_camera_tracking_results.avi "lidar-camera-video]")

### 3. Which challenges will a sensor fusion system face in real-life scenarios? Did you see any of these challenges in the project?
Camera calibration is one of the challenges.

### 4. Can you think of ways to improve your tracking results in the future?
1. Use of more optimal distance calculation algorithm such as GNN or PDA.
2. Include z-axis in the calculations for better track estimation.
3. Fuse the data from multiple LiDAR sources.
