import Home from "./pages/Home";
import Start from "./pages/Start";
import ReplaceSupplyStep1 from "./pages/ReplaceSupplyStep1";
import ReplaceSupplyStep2 from "./pages/ReplaceSupplyStep2";
import ReplaceSupplyStep3 from "./pages/ReplaceSupplyStep3";
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
      </Routes>
    </Router>
  );
}

export default App;
