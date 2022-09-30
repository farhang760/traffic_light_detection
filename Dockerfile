FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
SHELL ["/bin/bash", "-c"]
MAINTAINER abhishek bose 
ENV DEBIAN_FRONTEND noninteractive
ARG ROS_PKG=ros_base
ENV ROS_DISTRO=melodic
ENV ROS_ROOT=/opt/ros/${ROS_DISTRO}
RUN apt update && apt install -y tcl
RUN apt-get update -y && apt-get install -y python-pip python-dev libsm6 libxext6 libxrender-dev


RUN \
	apt-get install -y \
	wget \
	unzip \
	ffmpeg \ 
	git

RUN pip install numpy
RUN apt-get install -y --no-install-recommends libopencv-dev 

# add the ROS deb repo to the apt sources list
#
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
          git \
		cmake \
		build-essential \
		curl \
		wget \
		gnupg2 \
		lsb-release \
		ca-certificates

RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -


# 
# install ROS packages
#
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
		ros-melodic-`echo "${ROS_PKG}" | tr '_' '-'` \
		ros-melodic-image-transport \
		ros-melodic-vision-msgs \
          python-rosdep \
          python-rosinstall \
          python-rosinstall-generator \
          python-wstool 
    


#
# init/update rosdep
#
RUN apt-get update && \
    cd ${ROS_ROOT} && \
    rosdep init && \
    rosdep update 



WORKDIR /root
ENV PLANNER_WS=catkin_ws

RUN apt update
RUN apt-get install -y python-catkin-pkg python-rosdep ros-melodic-catkin
RUN apt-get install -y  python-pip python3-pip python3-colcon-common-extensions python3-setuptools python3-vcstool
RUN apt-get install -y python3 python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip
RUN pip3 install -U setuptools
RUN apt-get install -y ros-melodic-catkin python-catkin-tools
RUN rosdep update
RUN pip install --upgrade pip
RUN apt-get -y install cmake wget
RUN apt-get install -y gcc g++
RUN apt-get install -y python-dev python-numpy
RUN apt-get install -y libavcodec-dev libavformat-dev libswscale-dev
RUN apt-get install -y libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
RUN apt-get install -y libgtk2.0-dev
RUN apt-get install -y libgtk-3-dev
RUN apt-get install -qqy x11-apps
RUN apt-get update -y || true && \
DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata libx11-dev && \
apt-get install -y --no-install-recommends libopencv-dev 
RUN mkdir $PLANNER_WS
WORKDIR /root
WORKDIR $PLANNER_WS
RUN mkdir src
WORKDIR src
RUN git clone https://github.com/farhang760/traffic_light_detection
WORKDIR /root
RUN git clone https://github.com/farhang760/darknet 
WORKDIR /root/darknet
RUN git checkout python_support
RUN sed -i 's/GPU=.*/GPU=0/' Makefile 
RUN sed -i 's/OPENCV=.*/OPENCV=1/' Makefile && \
	make


RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN wget https://github.com/smarthomefans/darknet-test/raw/master/yolov3-tiny.weights
WORKDIR /root
WORKDIR $PLANNER_WS
COPY ./ros_entrypoint.sh /
COPY ./ros_launchscript.sh /

RUN ["chmod", "+x", "/ros_entrypoint.sh"]
RUN ["chmod", "+x", "/ros_launchscript.sh"]
RUN source "/opt/ros/$ROS_DISTRO/setup.bash" && catkin_make
# Expose ports
EXPOSE 90

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["/ros_launchscript.sh"]




RUN pip install -U rospkg
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade Pillow
RUN pip3 install commonroad-io
RUN pip3 install rospkg numpy matplotlib
RUN apt-get install -y libproj-dev
RUN apt-get install -y libprotobuf-dev protobuf-compiler
RUN apt-get install -y ros-melodic-cmake-modules
RUN apt-get install -y ros-melodic-rosbash
RUN apt-get install -y ros-melodic-cv-bridge




RUN wget https://pjreddie.com/media/files/yolov3.weights -P weights/

WORKDIR /home
