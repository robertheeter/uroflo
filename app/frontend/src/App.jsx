import Home from "./pages/Home";
import Start from "./pages/Start";
import ReplaceSupplyStep1 from "./pages/ReplaceSupplyStep1";
import ReplaceSupplyStep2 from "./pages/ReplaceSupplyStep2";
import ReplaceSupplyStep3 from "./pages/ReplaceSupplyStep3";
import ReplaceWasteStep1 from "./pages/ReplaceWasteStep1";
import ReplaceWasteStep2 from "./pages/ReplaceWasteStep2";
import ReplaceWasteStep3 from "./pages/ReplaceWasteStep3";
import ReplaceTubing from "./pages/ReplaceTubing";
import Landing from "./pages/Landing";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="*" element={<Home />} />
        <Route path="/start" element={<Start />} />
        <Route path="/replace/supply/step1" element={<ReplaceSupplyStep1 />} />
        <Route path="/replace/supply/step2" element={<ReplaceSupplyStep2 />} />
        <Route path="/replace/supply/step3" element={<ReplaceSupplyStep3 />} />
        <Route path="/replace/waste/step1" element={<ReplaceWasteStep1 />} />
        <Route path="/replace/waste/step2" element={<ReplaceWasteStep2 />} />
        <Route path="/replace/waste/step3" element={<ReplaceWasteStep3 />} />
        <Route path="/replace/tubing" element={<ReplaceTubing />} />
        <Route path="/landing" element={<Landing />} />
      </Routes>
    </Router>
  );
}

export default App;
