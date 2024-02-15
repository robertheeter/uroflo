import axios from "axios";
import { Switch } from "@chakra-ui/react";
import { TbTriangleFilled } from "react-icons/tb";
import { TbTriangleInvertedFilled } from "react-icons/tb";

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
  // [#7fb4df] uroflo blue
  // amber-600
  // red-600
  return (
    <div className="flex flex-col justify-start items-center w-full h-full gap-y-6">
      <div
        className="flex flex-col rounded-2xl text-slate-200 
                      bg-red-600 w-full h-[162px] px-5 py-4 gap-y-1"
      >
        <p className="text-3xl">
          STATUS <p className="font-bold">CAUTION</p>
        </p>
        <p className="text-xl">SEVERE HEMATURIA FOR &gt; 30 MIN</p>
      </div>
      <div className="flex flex-row justify-center items-center gap-x-6 w-full">
        <div className="flex items-center justify-center text-center rounded-lg font-bold bg-slate-200 text-slate-950 text-2xl w-[45%] h-[90px] px-3 py-1">
          REPLACE SUPPLY
        </div>
        <div className="flex items-center justify-center text-center rounded-lg font-bold bg-slate-200 text-slate-950 text-2xl w-[45%] h-[90px] px-3 py-1">
          REPLACE WASTE
        </div>
      </div>
      <div className="flex flex-row justify-center items-center gap-x-6 w-full">
        <div className="flex items-center justify-center rounded-lg font-bold bg-slate-300 text-slate-950 text-2xl w-[45%] h-[90px] px-3 py-1">
          MUTE
        </div>
        <div className="flex items-center justify-center rounded-lg font-bold bg-slate-950 border-2 border-slate-200 text-slate-200 text-2xl w-[45%] h-[90px] px-3 py-1">
          RESET
        </div>
      </div>
      <div className="flex flex-row justify-between items-center w-full">
        <p className="text-2xl text-slate-200">AUTO CONTROL</p>
        <Switch
          colorScheme="green"
          size="lg"
          style={{ transform: "scale(1.2)" }}
        />
      </div>
      <div className="flex flex-row justify-between items-center w-full">
        <p className="text-2xl text-slate-200">SUPPLY INFLOW</p>
        <div className="flex flex-row gap-x-6">
          <button
            className="h-[50px] w-[50px] rounded-lg bg-slate-200 flex justify-center items-center"
            onClick={increaseFlow}
          >
            <TbTriangleFilled className="text-3xl text-slate-950" />
          </button>
          <button
            className="h-[50px] w-[50px] rounded-lg bg-slate-200 flex justify-center items-center"
            onClick={decreaseFlow}
          >
            <TbTriangleInvertedFilled className="text-3xl text-slate-950" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ControlPanel;
