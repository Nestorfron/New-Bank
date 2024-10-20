import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { NextUIProvider } from "@nextui-org/react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import Appcontext from "../src/store/appContext.jsx";
import App from "./App.jsx";
import "../src/styles/index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <NextUIProvider>
      <Appcontext>
        <NextThemesProvider attribute="class" defaultTheme="dark">
          <App />
        </NextThemesProvider>
      </Appcontext>
    </NextUIProvider>
  </StrictMode>
);
