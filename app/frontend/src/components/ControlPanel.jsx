import { Switch } from "@chakra-ui/react";
import { IoTriangle } from "react-icons/io5";
import UroFloLogo from "../assets/uroflo_blue_name_cropped.svg";

const ControlPanel = () => {
  return (
    <div className="flex flex-col justify-between items-center w-full">
      <div className="flex flex-row justify-left items-center w-full mb-2">
        <img src={UroFloLogo} alt="Description of Image" className="w-[60%]" />
      </div>
      <div className="flex flex-col gap-y-2 w-full">
        <div className="flex flex-row justify-between items-center w-full">
          <p className="text-xl text-slate-200">AUTO CONTROL</p>
          <Switch size="lg" colorScheme="green" />
        </div>
        <div className="flex flex-row justify-between items-center w-full">
          <p className="text-xl text-slate-200">INFLOW RATE</p>
          <div className="flex flex-row gap-x-2">
            <div className="h-[40px] w-[40px] rounded-lg bg-slate-300 flex justify-center items-center">
              <IoTriangle className="text-3xl text-slate-950" />
            </div>
            <div className="h-[40px] w-[40px] rounded-lg bg-slate-300 flex justify-center items-center">
              <IoTriangle className="text-3xl text-slate-950 rotate-180" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ControlPanel;
