---
sidebar_position: 5
sidebar_label: "Week 6-7: Gazebo Simulation"
---

# Week 6-7: Gazebo Simulation

## 1. Introduction to Gazebo

Gazebo is an open-source 3D robot simulator widely used in robotics research and development. It allows users to accurately simulate populations of robots, environments, and sensors in a high-fidelity physics engine. Gazebo offers the ability to test algorithms, design robots, perform regression testing, and train AI systems in realistic scenarios without the need for physical hardware. It integrates seamlessly with the Robot Operating System (ROS), providing a powerful platform for simulating complex robotic systems.

Key features of Gazebo include:
*   **Physics Engine**: Supports various physics engines (ODE, Bullet, DART, Simbody) for realistic rigid-body dynamics.
*   **3D Graphics**: Utilizes OGRE for high-quality rendering of environments and robots.
*   **Sensor Simulation**: Simulates a wide range of sensors, including cameras, LiDAR, IMUs, force/torque sensors, and more, providing realistic data streams.
*   **Robot Models**: Supports URDF (Unified Robot Description Format) and SDF (Simulation Description Format) for defining robot kinematics, dynamics, and visual properties.
*   **Extensibility**: Plugin-based architecture allows users to extend Gazebo's functionality with custom sensors, actuators, and control algorithms.

## 2. Environment Setup

Setting up Gazebo typically involves installing it alongside ROS, which provides the necessary tools and libraries for robot control and perception.

### Ubuntu (Recommended for ROS/Gazebo)

For Ubuntu, the easiest way to install Gazebo is through the ROS installation. Assuming you have a ROS distribution (e.g., Noetic, Foxy, Humble) installed, Gazebo usually comes as a dependency.

**1. Install ROS (if not already installed):**

```bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
sudo apt update
sudo apt install ros-noetic-desktop-full  # For ROS Noetic; change 'noetic' for other distributions
```

**2. Install Gazebo (if not already part of desktop-full):**

```bash
sudo apt install gazebo11  # Gazebo 11 is standard for ROS Noetic
sudo apt install libgazebo11-dev  # For development files
```

**3. Set up environment variables:**

```bash
echo "source /usr/share/gazebo-11/setup.sh" >> ~/.bashrc
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

**4. Test Gazebo:**

```bash
gazebo
```
This should launch the Gazebo GUI with an empty world.

## 3. URDF/SDF Robot Descriptions for Humanoids

Robot descriptions are crucial for Gazebo to understand the physical and visual properties of a robot.

*   **URDF (Unified Robot Description Format)**: An XML format for describing robot kinematics and dynamics. It describes the robot's joints, links, sensors, and other features. URDF is primarily used in ROS for representing the robot model for manipulation and planning.
*   **SDF (Simulation Description Format)**: An XML format designed specifically for Gazebo. SDF can describe robots, environments, and even light sources. It is more comprehensive than URDF and allows for defining more advanced simulation properties directly within the file. Gazebo often converts URDF files to SDF internally for simulation.

### Key Elements in URDF/SDF

Both formats share common concepts:

*   **`<link>`**: Represents a rigid body of the robot (e.g., a limb, torso, head). It defines mass, inertia, visual properties (mesh, color), and collision properties.
*   **`<joint>`**: Defines the connection between two links. It specifies the type of joint (revolute, prismatic, fixed), its axis of rotation/translation, limits, and dynamics (friction, damping).
*   **`<collision>`**: Defines the geometry used for physics collision detection.
*   **`<visual>`**: Defines the geometry used for rendering the robot's appearance.
*   **`<inertial>`**: Defines the mass and inertia tensor of a link, critical for realistic physics simulation.

### URDF Example: Simple Humanoid Arm Segment

Let's consider a simple segment of a humanoid arm.

```xml
<?xml version="1.0"?>
<robot name="simple_arm">
  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.5"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Upper Arm Link -->
  <link name="upper_arm_link">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <origin xyz="0 0 0.15" rpy="0 0 0"/>
      <material name="red">
        <color rgba="0.8 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <origin xyz="0 0 0.15" rpy="0 0 0"/>
    </collision>
    <inertial>
      <origin xyz="0 0 0.15" rpy="0 0 0"/>
      <mass value="1.0"/>
      <inertia ixx="0.005" ixy="0" ixz="0" iyy="0.005" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Shoulder Joint (connects base_link to upper_arm_link) -->
  <joint name="shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="upper_arm_link"/>
    <origin xyz="0 0 0.05" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
    <dynamics damping="0.1" friction="0.1"/>
  </joint>

</robot>
```

This URDF defines two links (`base_link` and `upper_arm_link`) and a revolute joint (`shoulder_joint`) connecting them. The `origin` tag within `visual`, `collision`, and `inertial` refers to the offset of the geometry or inertial properties relative to the link's frame. The `origin` within the `joint` refers to the joint's position relative to the parent link.

### SDF Example: World with a Simple Robot (conceptual)

An SDF file can define a complete world, including static objects, lights, and multiple robots.

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="default">
    <!-- Ground Plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Sun Light -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- My Humanoid Robot -->
    <model name="my_humanoid">
      <pose>0 0 0.5 0 0 0</pose> <!-- Initial position and orientation -->
      <link name="torso">
        <inertial><mass>10</mass><inertia ixx="1" iyy="1" izz="1" ixy="0" ixz="0" iyz="0"/></inertial>
        <visual name="torso_visual">
          <geometry><box><size>0.2 0.3 0.5</size></box></geometry>
        </visual>
        <collision name="torso_collision">
          <geometry><box><size>0.2 0.3 0.5</size></box></geometry>
        </collision>
      </link>

      <link name="head">
        <inertial><mass>2</mass><inertia ixx="0.1" iyy="0.1" izz="0.1" ixy="0" ixz="0" iyz="0"/></inertial>
        <visual name="head_visual">
          <geometry><sphere><radius>0.1</radius></sphere></geometry>
        </visual>
        <collision name="head_collision">
          <geometry><sphere><radius>0.1</radius></sphere></geometry>
        </collision>
      </link>

      <joint name="torso_to_head_joint" type="revolute">
        <parent>torso</parent>
        <child>head</child>
        <pose>0 0 0.35 0 0 0</pose> <!-- Offset of head relative to torso -->
        <axis><xyz>0 1 0</xyz></axis>
        <limit lower="-0.5" upper="0.5"/>
      </joint>

      <!-- Can include more links and joints for arms, legs etc. -->
      <!-- Plugins for control or sensors can also be added here -->

    </model>
  </world>
</sdf>
```

This SDF defines a world with a ground plane, sun, and a `my_humanoid` model consisting of a `torso` and `head` link connected by a `torso_to_head_joint`.

## 4. Physics & Sensor Simulation

Gazebo's strength lies in its ability to simulate realistic physics and sensor data, crucial for developing robust AI systems.

### Physics Simulation

Gazebo leverages powerful physics engines to simulate:
*   **Gravity**: Objects fall and interact realistically.
*   **Collisions**: Accurate detection and response between complex geometries.
*   **Friction**: Affects sliding and rolling movements.
*   **Joint Dynamics**: Damping, friction, and motor control for robotic joints.
*   **Fluid Dynamics (with plugins)**: For simulating underwater or aerial robots.

The `<inertial>` tag in URDF/SDF is vital for correct physics simulation, defining mass, center of mass, and inertia tensor.

### Sensor Simulation

Gazebo provides plugins for various sensors. These plugins generate data streams that mimic real-world sensor outputs, complete with configurable noise, resolution, and update rates.

#### a) LiDAR (Light Detection and Ranging)

LiDAR sensors measure distances to objects by emitting pulsed laser light and measuring the reflected pulses. Gazebo simulates this by casting rays into the environment.

**SDF Snippet for a LiDAR Sensor:**

```xml
<link name="hokuyo_link">
  <inertial><mass>0.1</mass><inertia ixx="0.001" iyy="0.001" izz="0.001" ixy="0" ixz="0" iyz="0"/></inertial>
  <visual name="hokuyo_visual">
    <geometry><mesh><uri>model://hokuyo/meshes/hokuyo.dae</uri></mesh></geometry>
  </visual>
  <collision name="hokuyo_collision">
    <geometry><box><size>0.1 0.1 0.1</size></box></geometry>
  </collision>
  <sensor name="laser_sensor" type="ray">
    <pose>0 0 0 0 0 0</pose>
    <always_on>1</always_on>
    <visualize>true</visualize>
    <update_rate>30</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>180</samples>
          <resolution>1</resolution>
          <min_angle>-1.570796</min_angle> <!-- -90 degrees -->
          <max_angle>1.570796</max_angle>  <!-- +90 degrees -->
        </horizontal>
      </scan>
      <range>
        <min>0.1</min>
        <max>10.0</max>
        <resolution>0.01</resolution>
      </range>
      <noise type="gaussian">
        <mean>0.0</mean>
        <stddev>0.01</stddev>
      </noise>
    </ray>
    <plugin name="gazebo_ros_laser_controller" filename="libgazebo_ros_laser.so">
      <topicName>/laser/scan</topicName>
      <frameName>hokuyo_link</frameName>
    </plugin>
  </sensor>
</link>
<joint name="hokuyo_joint" type="fixed">
  <child>hokuyo_link</child>
  <parent>head</parent> <!-- Attach to the head link, for example -->
  <pose>0.05 0 0 0 0 0</pose>
</joint>
```

This snippet defines a `hokuyo_link` with a `ray` type sensor (LiDAR). It specifies the horizontal scan properties (samples, angles), range, and gaussian noise. The `libgazebo_ros_laser.so` plugin publishes the scan data to the `/laser/scan` ROS topic.

#### b) Cameras

Cameras provide visual information of the environment, simulating RGB, depth, and infrared data.

**SDF Snippet for a Camera Sensor:**

```xml
<link name="camera_link">
  <inertial><mass>0.01</mass><inertia ixx="0.0001" iyy="0.0001" izz="0.0001" ixy="0" ixz="0" iyz="0"/></inertial>
  <visual name="camera_visual">
    <geometry><box><size>0.02 0.02 0.02</size></box></geometry>
  </visual>
  <collision name="camera_collision">
    <geometry><box><size>0.02 0.02 0.02</size></box></geometry>
  </collision>
  <sensor name="camera" type="camera">
    <pose>0 0 0 0 0 0</pose>
    <always_on>1</always_on>
    <visualize>true</visualize>
    <update_rate>30</update_rate>
    <camera>
      <horizontal_fov>1.047</horizontal_fov> <!-- 60 degrees -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
      <noise type="gaussian">
        <mean>0.0</mean>
        <stddev>0.007</stddev>
      </noise>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <alwaysOn>true</alwaysOn>
      <updateRate>30.0</updateRate>
      <cameraName>robot_camera</cameraName>
      <imageTopicName>image_raw</imageTopicName>
      <cameraInfoTopicName>camer-info</cameraInfoTopicName>
      <frameName>camera_link</frameName>
      <hackBaseline>0.07</hackBaseline>
    </plugin>
  </sensor>
</link>
<joint name="camera_joint" type="fixed">
  <child>camera_link</child>
  <parent>head</parent>
  <pose>0.08 0 0 0 0 0</pose>
</joint>
```

This defines a `camera_link` with a `camera` type sensor. It configures the field of view (FOV), image resolution, format, and clipping planes. The `libgazebo_ros_camera.so` plugin publishes image data to `/robot_camera/image_raw` and camera info to `/robot_camera/camer-info` ROS topics.

#### c) IMUs (Inertial Measurement Units)

IMUs measure linear acceleration and angular velocity, providing information about a robot's orientation and movement.

**SDF Snippet for an IMU Sensor:**

```xml
<link name="imu_link">
  <inertial><mass>0.005</mass><inertia ixx="0.00001" iyy="0.00001" izz="0.00001" ixy="0" ixz="0" iyz="0"/></inertial>
  <visual name="imu_visual">
    <geometry><box><size>0.01 0.01 0.01</size></box></geometry>
  </visual>
  <collision name="imu_collision">
    <geometry><box><size>0.01 0.01 0.01</size></box></geometry>
  </collision>
  <sensor name="imu_sensor" type="imu">
    <always_on>1</always_on>
    <update_rate>100</update_rate>
    <imu>
      <noise type="gaussian">
        <rate>
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
          <bias_sd>0.0000076</bias_sd>
          <bias_walk>0.000004</bias_walk>
        </rate>
        <accel>
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
          <bias_sd>0.00002</bias_sd>
          <bias_walk>0.000006</bias_walk>
        </accel>
      </noise>
    </imu>
    <plugin name="imu_plugin" filename="libgazebo_ros_imu_sensor.so">
      <topicName>imu/data</topicName>
      <frameName>imu_link</frameName>
      <updateRate>100.0</updateRate>
      <rpyOffset>0 0 0</rpyOffset>
      <gaussianNoise>0.0001</gaussianNoise>
    </plugin>
  </sensor>
</link>
<joint name="imu_joint" type="fixed">
  <child>imu_link</child>
  <parent>torso</parent> <!-- Attach to the torso link -->
  <pose>0 0 0 0 0 0</pose>
</joint>
```

This defines an `imu_link` with an `imu` type sensor. It specifies update rate and detailed noise parameters for both angular velocity (`rate`) and linear acceleration (`accel`). The `libgazebo_ros_imu_sensor.so` plugin publishes IMU data to the `/imu/data` ROS topic.

## 5. Exercises

1.  **Modify a URDF:** Take the provided `simple_arm` URDF example. Add a new `forearm_link` and an `elbow_joint` to create a two-segment arm. Ensure proper joint limits and origins.
2.  **Launch a Robot in Gazebo:**
    *   Create a simple `my_robot.urdf` file for a wheeled robot (e.g., two wheels, a chassis, and an IMU).
    *   Create a Gazebo launch file (`launch/my_robot_world.launch`) that spawns your robot into an empty Gazebo world.
    *   Launch your robot: `roslaunch my_robot_pkg my_robot_world.launch`
3.  **Integrate a Sensor:** Add a camera sensor to the `head` link of the humanoid SDF example. Verify that the camera stream can be viewed (e.g., using `rqt_image_view` in ROS).
4.  **Explore Gazebo GUI:** Experiment with Gazebo's graphical interface:
    *   Change camera views.
    *   Add primitive shapes (boxes, spheres) to the world.
    *   Manipulate objects and apply forces.
    *   Inspect physics properties of links and joints.

## 6. Short Quiz

1.  What is the primary difference between URDF and SDF?
2.  Which XML tag in a robot description is crucial for realistic physics simulation, especially concerning mass distribution?
3.  If you want to simulate a laser range finder, which Gazebo sensor type would you use?
    a) `camera`
    b) `gpu_ray` (or `ray`)
    c) `imu`
    d) `contact`
4.  What ROS tool would you typically use to visualize the image stream from a simulated Gazebo camera?
5.  Why is environment setup for Gazebo often tied to ROS installation?
