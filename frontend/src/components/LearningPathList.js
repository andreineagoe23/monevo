import React from "react";

function LearningPathList({ learningPaths, activePathId, onTogglePath, onCourseClick }) {
  return (
    <div className="learning-paths">
      {learningPaths.map((path) => (
        <div key={path.id} className="learning-path">
          <h3 onClick={() => onTogglePath(path.id)}>{path.title}</h3>
          {activePathId === path.id && (
            <ul>
              {path.courses.map((course) => (
                <li key={course.id} onClick={() => onCourseClick(course.id)}>
                  {course.title}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
}

export default LearningPathList;
