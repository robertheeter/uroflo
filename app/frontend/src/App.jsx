// import "./App.css";
import Hematuria from "./components/Hematuria";
import Supply from "./components/Supply";
import Waste from "./components/Waste";

function App() {
  return (
    <div>
      <div className="bg-slate-800 flex flex-col justify-center items-center gap-y-5 fixed text-4xl w-3/4 h-4/5">
        <Hematuria />
        <Supply />
        <Waste />
      </div>
      <div className="fixed bg-slate-800 text-white text-4xl w-1/4 h-4/5 right-0">
        UROFLO + CONTROLS
      </div>
      <div className="fixed bg-slate-800 text-white text-4xl right-0 bottom-0 w-1/4 h-1/5">
        CONTACT
      </div>
      <div className="fixed bg-slate-800 text-white text-4xl bottom-0 w-3/4 h-1/5">
        PATIENT INFO
      </div>
    </div>
  );
}

export default App;
