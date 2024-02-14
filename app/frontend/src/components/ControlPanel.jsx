import axios from "axios";
import { Switch } from "@chakra-ui/react";
import { TbTriangleFilled } from "react-icons/tb";
import { TbTriangleInvertedFilled } from "react-icons/tb";
import UroFloLogo from "../assets/uroflo_blue_name_cropped.svg";

const ControlPanel = () => {
  const increaseFlow = () => {
    const url = "http://localhost:8000/uroflo/control/inflow_level_increase";
    const data = {
      inflow_level_increase: "TRUE",
    };

    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const decreaseFlow = () => {
    const url = "http://localhost:8000/uroflo/control/inflow_level_decrease";
    const data = {
      inflow_level_decrease: "TRUE",
    };

    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className="flex flex-col justify-between items-center w-full h-full pb-6">
      <div
        className="flex flex-col rounded-2xl text-slate-200 
                      bg-red-500 w-full h-40 px-5 py-4 gap-y-1"
      >
        <p className="font-bold text-3xl">STATUS CRITICAL</p>
        <p className="text-xl">SEVERE HEMATURIA DETECTED FOR &gt; 30 MIN</p>
      </div>
      <div className="flex flex-row justify-left items-center w-full mb-4">
        <img src={UroFloLogo} alt="Description of Image" className="w-[60%]" />
      </div>
      <div className="flex flex-row justify-between items-center w-full">
        <p className="text-3xl text-slate-200">AUTO CONTROL</p>
        <Switch
          colorScheme="green"
          size="lg"
          style={{ transform: "scale(1.4)" }}
        />
      </div>
      <div className="flex flex-row justify-between items-center w-full">
        <p className="text-3xl text-slate-200">SUPPLY INFLOW</p>
        <div className="flex flex-row gap-x-3">
          <button
            className="h-[58px] w-[58px] rounded-lg bg-slate-300 flex justify-center items-center"
            onClick={increaseFlow}
          >
            <TbTriangleFilled className="text-4xl text-slate-950" />
          </button>
          <button
            className="h-[58px] w-[58px] rounded-lg bg-slate-300 flex justify-center items-center"
            onClick={decreaseFlow}
          >
            <TbTriangleInvertedFilled className="text-4xl text-slate-950" />
          </button>
        </div>
      </div>
      <div className="flex flex-row justify-center items-center gap-x-3 w-full">
        <div className="rounded-lg bg-blue-900 text-slate-200 text-xl w-[48%] h-16 px-3 py-1">
          REPLACE SUPPLY BAG
        </div>
        <div className="rounded-lg bg-yellow-900 text-slate-200 text-xl w-[48%] h-16 px-3 py-1">
          REPLACE WASTE BAG
        </div>
      </div>
      <div className="flex flex-row justify-between items-center w-full">
        <p className="text-3xl text-slate-200">MUTE ALERTS</p>
        <Switch
          colorScheme="linkedin"
          size="lg"
          style={{ transform: "scale(1.4)" }}
        />
      </div>
    </div>
  );
};

export default ControlPanel;
