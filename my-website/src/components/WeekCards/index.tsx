import React from 'react';
import styles from './styles.module.css';

const weekData = [
  {
    title: 'Week 1-2: Introduction',
    link: '/docs/week-1-2-introduction',
    description: 'Introduction to the course and fundamental concepts.',
  },
  {
    title: 'Week 3-5: ROS2 Fundamentals',
    link: '/docs/week-3-5-ros2-fundamentals',
    description: 'Diving deep into the Robot Operating System 2.',
  },
  {
    title: 'Week 6-7: Gazebo Simulation',
    link: '/docs/week-6-7-gazebo-simulation',
    description: 'Simulating robots in a virtual environment.',
  },
  {
    title: 'Week 8-10: NVIDIA Isaac Platform',
    link: '/docs/week-8-10-nvidia-isaac-platform',
    description: 'Exploring the NVIDIA Isaac platform for robotics.',
  },
];

function WeekCards() {
  return (
    <div className={styles.weekGrid}>
      {weekData.map((week, index) => (
        <a href={week.link} className={styles.weekCard} key={index}>
          <h3>{week.title}</h3>
          <p>{week.description}</p>
        </a>
      ))}
    </div>
  );
}

export default WeekCards;
