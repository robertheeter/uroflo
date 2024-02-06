import Hematuria from "./components/Hematuria";
import Supply from "./components/Supply";
import Waste from "./components/Waste";
import ControlPanel from "./components/ControlPanel";
import { ChakraProvider } from "@chakra-ui/react";

function App() {
  return (
    <ChakraProvider>
      <div>
        <div
          className="bg-slate-950 flex flex-col justify-between items-center 
                    py-8 fixed text-4xl w-3/4 h-5/6 px-8"
        >
          <Hematuria />
          <Supply />
          <Waste />
        </div>
        <div className="fixed bg-slate-950 w-1/4 h-5/6 right-0 pt-5 pr-6">
          <ControlPanel />
        </div>
        <div className="fixed bg-slate-950 text-white text-4xl right-0 bottom-0 w-1/4 h-1/6">
          CONTACT
        </div>
        <div className="fixed bg-slate-950 text-white text-4xl bottom-0 w-3/4 h-1/6">
          PATIENT INFO
        </div>
      </div>
    </ChakraProvider>
  );
}

export default App;
