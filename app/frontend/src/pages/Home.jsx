import Hematuria from "../components/Hematuria";
import Volume from "../components/Volume";
import Rate from "../components/Rate";
import ControlPanel from "../components/ControlPanel";
import PatientInfo from "../components/PatientInfo";
import Time from "../components/Time";
import { ChakraProvider } from "@chakra-ui/react";

function Home() {
  return (
    <ChakraProvider>
      <div>
        <div
          className="bg-slate-950 flex flex-col justify-start items-center 
                    fixed text-4xl w-3/4 h-[584px] p-6 gap-y-6 border-r-2 border-slate-800"
        >
          <Hematuria />
          <Volume />
          <Rate />
        </div>
        <div className="fixed bg-slate-900 w-1/4 h-[584px] right-0 p-6">
          <ControlPanel />
        </div>
        <div className="fixed bg-slate-950 text-white text-4xl right-0 bottom-0 w-1/4 h-[136px] pr-6 pb-6 border-t-2 border-slate-800">
          <Time />
        </div>
        <div className="fixed bg-slate-950 text-white text-4xl bottom-0 w-3/4 h-[136px] px-6 pb-6 border-t-2 border-slate-800">
          <PatientInfo />
        </div>
      </div>
    </ChakraProvider>
  );
}

export default Home;
