---
sidebar_position: 4
sidebar_label: "Week 3-5: ROS 2 Fundamentals"
---

# Week 3-5: ROS 2 Fundamentals

## 1. Introduction to ROS 2 Architecture

The Robot Operating System (ROS) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms. ROS 2 is the successor to ROS 1, designed with improvements in areas like real-time capabilities, multi-robot systems, and embedded platforms.

At its core, ROS 2 facilitates communication between different parts of a robotic system. These parts, often referred to as *nodes*, can be individual programs responsible for specific functionalities, such as controlling a motor, reading sensor data, or performing navigation algorithms.

Key architectural concepts in ROS 2 include:

*   **Nodes**: Independent executable processes that perform computations.
*   **Topics**: A publish/subscribe mechanism for real-time data streaming.
*   **Services**: A request/reply mechanism for remote procedure calls.
*   **Actions**: A long-running goal-oriented communication mechanism, built on topics and services.
*   **Parameters**: Dynamic configuration values for nodes.
*   **Launch Files**: XML or Python files to start and configure multiple ROS 2 nodes and their parameters.
*   **ROS 2 Graph**: The network of ROS 2 nodes processing data.

Unlike ROS 1, ROS 2 uses a Data Distribution Service (DDS) as its middleware, providing better reliability, scalability, and quality-of-service (QoS) settings.

## 2. Nodes, Topics, and Services

### Nodes

A ROS 2 node is an executable that performs a specific task. For example, a robot might have one node for reading laser scan data, another for controlling the robot's wheels, and a third for path planning. Nodes are designed to be modular and reusable.

### Topics

Topics are the most common way for nodes to exchange data in ROS 2. They implement a publish/subscribe model:
*   **Publishers**: Nodes that send data to a topic.
*   **Subscribers**: Nodes that receive data from a topic.

When a publisher publishes data to a topic, all nodes subscribed to that topic will receive the data. Data is sent as *messages*, which are structured data types defined by ROS 2.

**Example Scenario**: A robot's camera node (publisher) publishes image data to the `/camera/image` topic. An image processing node (subscriber) receives these images from the topic to detect objects.

### Services

Services provide a request/reply mechanism, allowing nodes to offer specific functionalities that other nodes can call. This is useful for operations that require a response, unlike the continuous data stream of topics.

*   **Service Server**: The node that offers the service and responds to requests.
*   **Service Client**: The node that requests the service and receives a response.

**Example Scenario**: A navigation node (service client) might call a mapping node's `/map_service` (service server) to get a map of the environment.

## 3. Python Integration with rclpy

`rclpy` is the Python client library for ROS 2. It provides an interface to interact with the ROS 2 graph using Python.

### Setting up a ROS 2 Python Package

Before writing code, you typically create a ROS 2 package.

```bash
# Create a new ROS 2 workspace (if you don't have one)
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Create a new Python package named 'my_robot_pkg'
ros2 pkg create --build-type ament_python my_robot_pkg
```

Now, navigate into `~/ros2_ws/src/my_robot_pkg`. Your Python scripts will go into the `my_robot_pkg/my_robot_pkg` directory. Remember to add `install` target to `setup.py`

```python
from setuptools import setup

package_name = 'my_robot_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = my_robot_pkg.publisher_member_function:main',
            'listener = my_robot_pkg.subscriber_member_function:main',
            'add_two_ints_server = my_robot_pkg.service_member_function:main',
            'add_two_ints_client = my_robot_pkg.client_member_function:main',
        ],
    },
)

```

### Publishers (Talker)

Let's create a simple publisher node that sends "Hello ROS 2!" messages.

**File**: `~/ros2_ws/src/my_robot_pkg/my_robot_pkg/publisher_member_function.py`

```python
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS 2: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Subscribers (Listener)

Now, a subscriber node to receive these messages.

**File**: `~/ros2_ws/src/my_robot_pkg/my_robot_pkg/subscriber_member_function.py`

```python
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

To run these:
1.  **Build your package**: `cd ~/ros2_ws && colcon build --packages-select my_robot_pkg`
2.  **Source your workspace**: `source install/setup.bash` (or `setup.zsh`, `setup.ps1` for PowerShell)
3.  **Run publisher**: `ros2 run my_robot_pkg talker`
4.  **Run subscriber in another terminal**: `ros2 run my_robot_pkg listener`

You should see the subscriber printing the messages from the publisher.

### Services

Let's implement a simple service that adds two integers.

First, you need to define the service interface. ROS 2 services are defined in `.srv` files.

**File**: `~/ros2_ws/src/my_robot_pkg/srv/AddTwoInts.srv`

```
int64 a
int64 b
---
int64 sum
```

You need to modify `package.xml` and `CMakeLists.txt` to properly build this service message.

**`package.xml` additions:**

```xml
  <depend>rclpy</depend>
  <depend>std_msgs</depend>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <build_depend>rosidl_default_generators</build_depend>
  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>
```

**`CMakeLists.txt` additions:**

```cmake
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/AddTwoInts.srv"
)

ament_python_install_package(${PROJECT_NAME})
```

Now, the service server and client.

**Service Server**: `~/ros2_ws/src/my_robot_pkg/my_robot_pkg/service_member_function.py`

```python
from my_robot_pkg.srv import AddTwoInts

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request
a: %d b: %d' % (request.a, request.b))
        return response


def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

**Service Client**: `~/ros2_ws/src/my_robot_pkg/my_robot_pkg/client_member_function.py`

```python
import sys

from my_robot_pkg.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    minimal_client.get_logger().info(
        'Result of add_two_ints: for %d + %d = %d' %
        (response.a, response.b, response.sum))

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

To run these:
1.  **Build your package again**: `cd ~/ros2_ws && colcon build --packages-select my_robot_pkg`
2.  **Source your workspace**: `source install/setup.bash`
3.  **Run service server**: `ros2 run my_robot_pkg add_two_ints_server`
4.  **Run service client in another terminal**: `ros2 run my_robot_pkg add_two_ints_client 5 7`

You should see the client receiving the sum from the server.

## 4. Launch Files and Parameters

### Launch Files

Launch files are a powerful way to start and configure multiple ROS 2 nodes simultaneously. They replace the functionality of `ros2 run` for multiple nodes and offer greater flexibility in configuration. Launch files are typically written in Python or XML. Python launch files are generally preferred for their flexibility.

**Example Python Launch File**: `~/ros2_ws/src/my_robot_pkg/launch/my_robot_launch.py`

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_robot_pkg',
            executable='talker',
            name='my_publisher',
            parameters=[{'timer_period': 1.0}] # Example parameter
        ),
        Node(
            package='my_robot_pkg',
            executable='listener',
            name='my_subscriber'
        ),
    ])
```

To use this launch file, you also need to ensure it's installed. Add this to your `setup.py`'s `data_files` list:

```python
        ('share/' + package_name + '/launch', ['launch/my_robot_launch.py']),
```

And then rebuild your package: `cd ~/ros2_ws && colcon build --packages-select my_robot_pkg`
Source again: `source install/setup.bash`

**Running the Launch File**: `ros2 launch my_robot_pkg my_robot_launch.py`

This will start both the `talker` and `listener` nodes with the configurations defined in the launch file.

### Parameters

Parameters are dynamic values that can be configured for a node. They are analogous to global variables for a node, allowing you to change a node's behavior without recompiling the code. Parameters can be set in launch files, from the command line, or programmatically.

In the publisher example above, we could modify `timer_period` as a parameter.

**Modifying `publisher_member_function.py` for parameters:**

```python
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.declare_parameter('timer_period', 0.5) # Declare parameter with default value
        timer_period = self.get_parameter('timer_period').get_parameter_value().double_value

        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info(f'Publisher started with timer_period: {timer_period}')
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS 2: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Now, when launching the publisher, you can set `timer_period`:

*   **From command line**: `ros2 run my_robot_pkg talker --ros-args -p timer_period:=1.0`
*   **From launch file (as shown in the example above)**:
    ```python
            parameters=[{'timer_period': 1.0}]
    ```

## 5. Exercises and Quiz

### Exercises

1.  **Modify the Talker-Listener Example**:
    *   Change the message type from `std_msgs.msg.String` to `std_msgs.msg.Int32` and have the publisher send an incrementing integer.
    *   Update the subscriber to correctly receive and print the `Int32` messages.
    *   Rebuild and run to verify.
2.  **Create a Custom Message Type**:
    *   Define a custom ROS 2 message (e.g., `Person.msg` with `string name` and `int32 age`).
    *   Create a new publisher node that publishes instances of this custom message.
    *   Create a new subscriber node that subscribes to and prints the custom messages.
    *   Remember to update `package.xml` and `CMakeLists.txt` for your new message type.
3.  **Implement a Calculator Service**:
    *   Extend the `AddTwoInts` service to include subtraction, multiplication, and division operations.
    *   Create a new service server that handles these operations based on a request field (e.g., `string operation`, `int64 num1`, `int64 num2`).
    *   Create a new service client that can call this service for different operations.
4.  **Launch File with Multiple Publishers**:
    *   Create a launch file that starts two `talker` nodes, each publishing to a *different* topic (e.g., `/topic_a` and `/topic_b`) with different `timer_period` parameters.
    *   Start two `listener` nodes, each subscribing to one of the new topics.
    *   Verify that both publisher-subscriber pairs are working correctly.

### Short Quiz

1.  What is the primary communication mechanism for real-time data streaming in ROS 2?
    a) Services
    b) Parameters
    c) Topics
    d) Actions
2.  Which ROS 2 client library is used for Python?
    a) rospy
    b) rclcpp
    c) rclpy
    d) ros_python
3.  How do nodes request a response from another node for a specific functionality?
    a) By publishing to a topic
    b) By calling a service
    c) By setting a parameter
    d) By using a launch file
4.  What is the main purpose of a ROS 2 launch file?
    a) To define custom message types
    b) To compile ROS 2 packages
    c) To start and configure multiple ROS 2 nodes
    d) To visualize robot data
5.  Which of the following is NOT a core architectural concept in ROS 2?
    a) Nodes
    b) Topics
    c) Services
    d) GUI tools

---

**Quiz Answers**: 1. c, 2. c, 3. b, 4. c, 5. d