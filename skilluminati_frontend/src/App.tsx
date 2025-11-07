import "./App.css";
import { ThemeProviderWrapper } from "./app/providers/ThemeProviderWrapper";
import { BrowserRouter } from "react-router-dom";
import { AppRoutes } from "./app/routes";

function App() {
  return (
    <ThemeProviderWrapper>
      <BrowserRouter basename={import.meta.env.BASE_URL}>
        <AppRoutes />
      </BrowserRouter>
    </ThemeProviderWrapper>
  );
}

export default App;
