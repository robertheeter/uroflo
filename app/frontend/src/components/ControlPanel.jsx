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
            <button
              className="h-[42px] w-[42px] rounded-lg bg-slate-300 flex justify-center items-center"
              onClick={increaseFlow}
            >
              <TbTriangleFilled className="text-3xl text-slate-950" />
            </button>
            <button
              className="h-[42px] w-[42px] rounded-lg bg-slate-300 flex justify-center items-center"
              onClick={decreaseFlow}
            >
              <TbTriangleInvertedFilled className="text-3xl text-slate-950" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ControlPanel;
