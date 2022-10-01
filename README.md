# Traffic_light_detection

This project is designed to test the traffic light detection for an autonomous vehicle

## schematic


![Alt text](docs/graph.png?raw=true "Overtake")


## Installation


## Dependencies
This software is built on the Robotic Operating System ([ROS]), which needs to be installed first. Additionally, YOLO for ROS depends on following software:

- [ROS(melodic)](http://wiki.ros.org/melodic/Installation/Ubuntu),
- [OpenCV](http://opencv.org/),
- [Darknet](https://pjreddie.com/darknet/)
 


## Install docker
Follow this instruction for installing docker:
https://docs.docker.com/engine/install/ubuntu/

## Commands for execution

Get the repository:
```bash
cd catkin_workspace/src/traffic_light_detection
Build the Docker Container:

docker build -t traffic_light_detection --progress=plain .
```
> **Note:** Ensure you can run docker without sudo. Building the conainer takes between 10 minutes and 30 minutes depending on your systems performance. 

Run the Container:
```bash
xhost +

docker run --rm -ti --net=host --ipc=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --env="QT_X11_NO_MITSHM=1" traffic_light_detection
```


## Viewing the report
open another terminal :
```bash
rostopic echo /traffic_light_size
rostopic echo /traffic_light_detected
rostopic echo /zone_height


```

### Building

In order to install traffic_light_detection, clone the latest version using SSH from this repository into your catkin workspace and compile the package using ROS.

    cd catkin_workspace/src
    git clone --recursive git@github.com:farhang760/traffic_light_detection.git
    cd darknet 
    open Makefile and change OPENCV = 1 (for better performance if you have GPU support change CUDA = 1)
    make
    cd ../
    catkin_make
    
### Download weights

Download the pre-trained weight from the COCO data set:

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


