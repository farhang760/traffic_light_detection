# traffic_light_detection

This project is designed to test the traffic light detection for an autonomous vehicle

## schematic


![Alt text](docs/graph.png?raw=true "Overtake")


## Installation
## Dependencies
This software is built on the Robotic Operating System ([ROS]), which needs to be installed first. Additionally, YOLO for ROS depends on following software:

- [ROS(melodic)](http://wiki.ros.org/melodic/Installation/Ubuntu),
- [OpenCV](http://opencv.org/),
- [Darknet](https://pjreddie.com/darknet/)
 

### Building

In order to install traffic_light_detection, clone the latest version using SSH from this repository into your catkin workspace and compile the package using ROS.

    cd catkin_workspace/src
    git clone --recursive git@github.com:leggedrobotics/darknet_ros.git
    cd darknet 
    open Makefile and change OPENCV = 1 (for better performance if you have GPU support change CUDA = 1)
    make
    cd ../
    catkin_make
    
### Download weights

The yolov3-tiny.weights and tiny-yolo-voc.weights are downloaded automatically in the CMakeLists.txt file. If you need to download them again, go into the weights folder and download the two pre-trained weights from the COCO data set:

    cd catkin_workspace/src/traffic_light_detection/darknet/
    wget http://pjreddie.com/media/files/yolov3-tiny.weights



## Run
roslaunch traffic_light_detection detection.launch 

## Nodes

### Node: traffic_light_detector

This is the main Node.

### ROS related parameters

You can change the names and other parameters of the publishers, subscribers and actions inside `src/Traffic_light_detector.py`.

#### Subscribed Topics


#### Published Topics

* **`traffic_light_detected`** ([std_msgs/Bool])
     
     detected traffic light publish in boolean

* **`traffic_light_size`** ([geometry_msgs/Vector3 ])

    publishes the size of traffic light in vector

* **`zone_heigth`** ([std_msgs/Float32])

    Publishes the height of traffic light zones.


