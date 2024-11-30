import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import styles from "../styles/LessonPage.module.css";

function fixImagePaths(content) {
  const mediaUrl = "http://localhost:8000/media/";
  const updatedContent = content.replace(
    /src="\/media\/([^"]+)"/g,
    (match, p1) => {
      const updatedPath = `${mediaUrl}${p1}`;
      console.log(`Updated image path: ${updatedPath}`); // Log for verification
      return `src="${updatedPath}"`;
    }
  );
  return updatedContent;
}

function LessonPage() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [completedLessons, setCompletedLessons] = useState([]);
  const [selectedLesson, setSelectedLesson] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");
  const [courseCompleted, setCourseCompleted] = useState(false);

  useEffect(() => {
    const fetchLessons = async () => {
      const accessToken = localStorage.getItem("accessToken");
      if (!accessToken) {
        setError("You are not logged in. Please log in to view lessons.");
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get(
          `http://localhost:8000/api/lessons/with_progress/?course=${courseId}`,
          { headers: { Authorization: `Bearer ${accessToken}` } }
        );
        const lessonsWithProgress = response.data;
        setLessons(lessonsWithProgress);
        setCompletedLessons(
          lessonsWithProgress
            .filter((lesson) => lesson.is_completed)
            .map((l) => l.id)
        );
      } catch (err) {
        console.error("Failed to fetch lessons:", err);
        setError("Failed to load lessons. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchLessons();
  }, [courseId]);

  useEffect(() => {
    if (lessons.length > 0 && completedLessons.length === lessons.length) {
      setCourseCompleted(true);
    }
  }, [lessons, completedLessons]);

  const handleCompleteLesson = async (lessonId) => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      setError("You are not logged in. Please log in to complete the lesson.");
      return;
    }

    try {
      await axios.post(
        `http://localhost:8000/api/progress/complete/`,
        { lesson_id: lessonId },
        {
          headers: { Authorization: `Bearer ${accessToken}` },
        }
      );

      setCompletedLessons((prev) => {
        const newCompletedLessons = [...prev, lessonId];
        return newCompletedLessons;
      });

      setSuccessMessage("Lesson completed! The next lesson is now unlocked.");
      setTimeout(() => setSuccessMessage(""), 3000);
      setSelectedLesson(null);
    } catch (err) {
      console.error("Failed to complete lesson:", err);
      setError("Failed to complete lesson. Please try again.");
    }
  };

  const handleCourseCompletion = () => {
    navigate(`/quiz/${courseId}`);
  };

  const handleLessonClick = (lessonId) => {
    if (selectedLesson === lessonId) {
      setSelectedLesson(null);
    } else {
      setSelectedLesson(lessonId);
    }
  };

  if (loading) {
    return <p>Loading lessons...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <div className="lessons-container">
        {successMessage && (
          <p className={styles.successMessage}>{successMessage}</p>
        )}

        <div className={styles.lessonBox}>
          {lessons.length > 0 ? (
            lessons.map((lesson, index) => {
              const isCompleted = completedLessons.includes(lesson.id);
              const isAccessible =
                index === 0 ||
                completedLessons.includes(lessons[index - 1]?.id);

              return (
                <div
                  key={lesson.id}
                  className={`${styles.lessonBoxItem} ${
                    isCompleted
                      ? styles.completed
                      : isAccessible
                      ? styles.incomplete
                      : styles.locked
                  }`}
                >
                  <h4 onClick={() => handleLessonClick(lesson.id)}>
                    {lesson.title}
                  </h4>
                  <p>{lesson.short_description}</p>

                  {selectedLesson === lesson.id && isAccessible && (
                    <div className={styles.lessonContent}>
                      {lesson.detailed_content ? (
                        <div
                          className={styles.detailedContent}
                          dangerouslySetInnerHTML={{
                            __html: fixImagePaths(lesson.detailed_content),
                          }}
                        />
                      ) : (
                        <p>No detailed content available.</p>
                      )}

                      {lesson.video_url && (
                        <div className={styles.videoPlayer}>
                          {lesson.video_url.includes("youtube.com") ||
                          lesson.video_url.includes("youtu.be") ? (
                            // Embed YouTube video
                            <iframe
                              width="100%"
                              height="500"
                              src={`https://www.youtube.com/embed/${new URLSearchParams(
                                new URL(lesson.video_url).search
                              ).get("v")}`}
                              frameBorder="0"
                              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                              allowFullScreen
                              title="YouTube Video"
                            ></iframe>
                          ) : (
                            // Fallback for direct video files
                            <video controls>
                              <source src={lesson.video_url} type="video/mp4" />
                              Your browser does not support the video tag.
                            </video>
                          )}
                        </div>
                      )}

                      {!isCompleted && (
                        <button
                          onClick={() => handleCompleteLesson(lesson.id)}
                          disabled={isCompleted || !isAccessible}
                        >
                          Complete Lesson
                        </button>
                      )}
                      {isCompleted && <p>This lesson is completed.</p>}
                    </div>
                  )}
                </div>
              );
            })
          ) : (
            <p>No lessons available for this course.</p>
          )}
        </div>

        {courseCompleted && (
          <div className={styles.courseCompletion}>
            <h3>Congratulations! You've completed the course.</h3>
            <button onClick={handleCourseCompletion}>
              Take the Course Quiz
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default LessonPage;
