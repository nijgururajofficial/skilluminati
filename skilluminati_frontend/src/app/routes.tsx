// src/routes/routes.tsx
import { Routes, Route } from "react-router-dom";
import { Home } from "../features/home/pages/Home";
import { LandingPage } from "../features/landing-page/pages/LandingPage";
import { LoginWindow } from "../features/registration/components/LoginWindow";
import { Registration } from "../features/registration/pages/Registration";
import { JobAnalyzer } from "../features/job-analyzer/pages/JobAnalyzer";
import { JobMatcher } from "../features/job-matcher/pages/JobMatcher";
import { JobProgressTracker } from "../features/job-progress-tracker/pages/JobProgressTracker";
import { SignUpWindow } from "../features/registration/components/SignUpWindow";
import { LearningPath } from "../features/learning-path/pages/LearningPath";
// import other pages as needed

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/home" element={<Home />} />
      <Route path="/login" element={<LoginWindow />} />
      <Route path="/signup" element={<SignUpWindow />} />
      <Route path="/landing-page" element={<LandingPage />} />
      <Route
        path="/registration"
        element={<Registration firstTimeUser={false} />}
      />
      <Route path="/job-analyzer" element={<JobAnalyzer />} />
      <Route path="/job-matcher" element={<JobMatcher />} />
      <Route path="/job-progress-tracker" element={<JobProgressTracker />} />
      <Route path="/learning-path" element={<LearningPath />} />
    </Routes>
  );
};
