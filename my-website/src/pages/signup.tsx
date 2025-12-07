import React, { useState } from "react";
import Layout from "@theme/Layout";
import Heading from "@theme/Heading";
import styles from "./signup.module.css";
import Link from "@docusaurus/Link";

const programmingLevels = ["Beginner", "Intermediate", "Advanced", "Expert"];
const aiKnowledgeLevels = ["None", "Beginner", "Intermediate", "Advanced"];
const languages = ["Python", "C++", "JavaScript", "Rust", "Java", "Go", "Other"];

interface FormData {
  email: string;
  password: string;
  confirmPassword: string;
  experienceYears: string;
  languagesKnown: string[];
  comfortLevel: string;
  arduinoExperience: boolean;
  raspberryPiExperience: boolean;
  previousRoboticsProjects: string;
  mlExperienceLevel: string;
  coursesCompleted: string;
  familiarConcepts: string[];
  rosExperience: boolean;
  rosVersion: string;
  learningGoals: string;
  timeCommitment: string;
}

const initialFormData: FormData = {
  email: "",
  password: "",
  confirmPassword: "",
  experienceYears: "",
  languagesKnown: [],
  comfortLevel: "",
  arduinoExperience: false,
  raspberryPiExperience: false,
  previousRoboticsProjects: "",
  mlExperienceLevel: "",
  coursesCompleted: "",
  familiarConcepts: [],
  rosExperience: false,
  rosVersion: "",
  learningGoals: "",
  timeCommitment: "",
};

const SignUpPage: React.FC = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value, type } = e.target;

    if (type === "checkbox") {
      setFormData({
        ...formData,
        [name]: (e.target as HTMLInputElement).checked,
      });
    } else if (name === "languagesKnown" || name === "familiarConcepts") {
      const selectedOptions = Array.from(
        (e.target as HTMLSelectElement).options
      )
        .filter((option) => option.selected)
        .map((option) => option.value);

      setFormData({
        ...formData,
        [name]: selectedOptions,
      });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const handleNext = () => {
    setError(null);

    switch (step) {
      case 1:
        if (!formData.email || !formData.password || !formData.confirmPassword) {
          setError("Please fill in all required fields.");
          return;
        }
        if (formData.password !== formData.confirmPassword) {
          setError("Passwords do not match.");
          return;
        }
        if (formData.password.length < 8) {
          setError("Password must be at least 8 characters long.");
          return;
        }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
          setError("Please enter a valid email address.");
          return;
        }
        break;

      case 2:
        if (
          !formData.experienceYears ||
          !formData.comfortLevel ||
          formData.languagesKnown.length === 0
        ) {
          setError("Please fill in all required fields.");
          return;
        }
        break;

      case 4:
        if (!formData.mlExperienceLevel) {
          setError("Please select your ML experience level.");
          return;
        }
        break;

      case 5:
        if (formData.rosExperience && formData.rosVersion === "") {
          setError("Please select ROS version.");
          return;
        }
        break;
    }

    setStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setError(null);
    setStep((prev) => prev - 1);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setError(null);
    setSuccess(null);

    if (formData.rosExperience && formData.rosVersion === "") {
      setError("Please select your ROS version.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/auth/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });

      if (response.ok) {
        setSuccess("Registration successful! You can now log in.");
        setFormData(initialFormData);
        setStep(1);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || "Registration failed. Please try again.");
      }
    } catch (err) {
      console.error("Network error:", err);
      setError("Network error. Please try again.");
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div>
            <Heading as="h2">Step 1: Account Information</Heading>
            <p>Create your email and password.</p>

            <div className={styles.formGroup}>
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className={styles.formGroup}>
              <label>Password (min 8 chars):</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>

            <div className={styles.formGroup}>
              <label>Confirm Password:</label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>

            <button onClick={handleNext}>Next</button>
          </div>
        );

      case 2:
        return (
          <div>
            <Heading as="h2">Step 2: Programming Background</Heading>

            <div className={styles.formGroup}>
              <label>Years of Experience:</label>
              <input
                type="number"
                name="experienceYears"
                value={formData.experienceYears}
                onChange={handleChange}
                min="0"
                max="20"
              />
            </div>

            <div className={styles.formGroup}>
              <label>Languages Known:</label>
              <select
                name="languagesKnown"
                multiple
                value={formData.languagesKnown}
                onChange={handleChange}
              >
                {languages.map((lang) => (
                  <option key={lang} value={lang}>
                    {lang}
                  </option>
                ))}
              </select>
            </div>

            <div className={styles.formGroup}>
              <label>Comfort Level:</label>
              <select
                name="comfortLevel"
                value={formData.comfortLevel}
                onChange={handleChange}
              >
                <option value="">-- Select --</option>
                {programmingLevels.map((lvl) => (
                  <option key={lvl} value={lvl}>
                    {lvl}
                  </option>
                ))}
              </select>
            </div>

            <button onClick={handleBack}>Back</button>
            <button onClick={handleNext}>Next</button>
          </div>
        );

      case 3:
        return (
          <div>
            <Heading as="h2">Step 3: Hardware Background</Heading>

            <div className={styles.formGroup}>
              <label>
                <input
                  type="checkbox"
                  name="arduinoExperience"
                  checked={formData.arduinoExperience}
                  onChange={handleChange}
                />
                Arduino Experience
              </label>
            </div>

            <div className={styles.formGroup}>
              <label>
                <input
                  type="checkbox"
                  name="raspberryPiExperience"
                  checked={formData.raspberryPiExperience}
                  onChange={handleChange}
                />
                Raspberry Pi Experience
              </label>
            </div>

            <div className={styles.formGroup}>
              <label>Previous Robotics Projects:</label>
              <textarea
                name="previousRoboticsProjects"
                value={formData.previousRoboticsProjects}
                onChange={handleChange}
              />
            </div>

            <button onClick={handleBack}>Back</button>
            <button onClick={handleNext}>Next</button>
          </div>
        );

      case 4:
        return (
          <div>
            <Heading as="h2">Step 4: AI/ML Knowledge</Heading>

            <div className={styles.formGroup}>
              <label>ML Experience Level:</label>
              <select
                name="mlExperienceLevel"
                value={formData.mlExperienceLevel}
                onChange={handleChange}
              >
                <option value="">-- Select --</option>
                {aiKnowledgeLevels.map((lvl) => (
                  <option key={lvl} value={lvl}>
                    {lvl}
                  </option>
                ))}
              </select>
            </div>

            <button onClick={handleBack}>Back</button>
            <button onClick={handleNext}>Next</button>
          </div>
        );

      case 5:
        return (
          <div>
            <Heading as="h2">Step 5: ROS & Goals</Heading>

            <div className={styles.formGroup}>
              <label>
                <input
                  type="radio"
                  name="rosExperience"
                  checked={formData.rosExperience === true}
                  onChange={() =>
                    setFormData({
                      ...formData,
                      rosExperience: true,
                      rosVersion: formData.rosVersion || "ROS2",
                    })
                  }
                />
                Yes, I have ROS experience
              </label>

              <label>
                <input
                  type="radio"
                  name="rosExperience"
                  checked={formData.rosExperience === false}
                  onChange={() =>
                    setFormData({
                      ...formData,
                      rosExperience: false,
                      rosVersion: "None",
                    })
                  }
                />
                No, I don't have ROS experience
              </label>
            </div>

            {formData.rosExperience && (
              <div className={styles.formGroup}>
                <label>ROS Version:</label>
                <select
                  name="rosVersion"
                  value={formData.rosVersion}
                  onChange={handleChange}
                >
                  <option value="">-- Select --</option>
                  <option value="ROS1">ROS1</option>
                  <option value="ROS2">ROS2</option>
                  <option value="Both">Both</option>
                </select>
              </div>
            )}

            <button onClick={handleBack}>Back</button>
            <button onClick={handleSubmit}>Register</button>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <Layout title="Sign Up" description="Sign up for Physical AI Book">
      <div className={styles.signupContainer}>
        <div className={styles.signupBox}>
          <Heading as="h1">Sign Up</Heading>

          {error && <div className={styles.errorMessage}>{error}</div>}
          {success && <div className={styles.successMessage}>{success}</div>}

          <form onSubmit={handleSubmit}>{renderStep()}</form>

          <p className={styles.loginLink}>
            Already have an account? <Link to="/signin">Sign In</Link>
          </p>
        </div>
      </div>
    </Layout>
  );
};

export default SignUpPage;
