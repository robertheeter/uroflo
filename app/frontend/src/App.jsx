// import "./App.css";
import Hematuria from "./components/Hematuria";

function App() {
  return (
    <div>
      <div className="fixed text-white text-4xl w-3/4 h-4/5">
        <Hematuria />
      </div>
      <div className="fixed bg-blue-500 text-white text-4xl w-1/4 h-4/5 right-0">
        UROFLO + CONTROLS
      </div>
      <div className="fixed bg-green-400 text-white text-4xl right-0 bottom-0 w-1/4 h-1/5">
        CONTACT
      </div>
      <div className="fixed bg-slate-700 text-white text-4xl bottom-0 w-3/4 h-1/5">
        PATIENT INFO
      </div>
    </div>
  );
}

export default App;
