import Hematuria from "./components/Hematuria";
import Supply from "./components/Supply";
import Waste from "./components/Waste";
import ControlPanel from "./components/ControlPanel";

function App() {
  return (
    <div>
      <div
        className="bg-slate-900 flex flex-col justify-center items-center 
                    gap-y-5 fixed text-4xl w-3/4 h-4/5 px-4"
      >
        <Hematuria />
        <Supply />
        <Waste />
      </div>
      <div className="fixed bg-slate-900 w-1/4 h-4/5 right-0">
        <ControlPanel />
      </div>
      <div className="fixed bg-slate-900 text-white text-4xl right-0 bottom-0 w-1/4 h-1/5">
        CONTACT
      </div>
      <div className="fixed bg-slate-900 text-white text-4xl bottom-0 w-3/4 h-1/5">
        PATIENT INFO
      </div>
    </div>
  );
}

export default App;
