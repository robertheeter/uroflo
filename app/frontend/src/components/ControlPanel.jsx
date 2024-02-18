import axios from "axios";
import { useState } from "react";
import { Switch } from "@chakra-ui/react";
import { TbTriangleFilled } from "react-icons/tb";
import { TbTriangleInvertedFilled } from "react-icons/tb";
import { useNavigate } from "react-router-dom";

const increaseFlow = () => {
  const url = "http://localhost:8000/uroflo/user/inflow_level_increase";
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
  const url = "http://localhost:8000/uroflo/user/inflow_level_decrease";
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

const replaceWaste = () => {
  const url = "http://localhost:8000/uroflo/user/waste_replace_volume";
  const data = {
    waste_replace_volume: "TRUE",
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

const mute = () => {
  const url = "http://localhost:8000/uroflo/user/mute";
  const data = {
    mute_count: "TRUE",
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

const ControlPanel = () => {
  // [#7fb4df] uroflo blue
  // amber-600
  // red-600
  const navigate = useNavigate();
  const [auto, setAuto] = useState(true);

  const handleSwitch = () => {
    setAuto(!auto);
    const data = {};
    const url = "http://localhost:8000/uroflo/user/automatic";
    if (auto) {
      data["automatic"] = "TRUE";
    } else {
      data["automatic"] = "FALSE";
    }
    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const reset = () => {
    const url = "http://localhost:8000/uroflo/user/reset";
    const data = {
      reset_count: "TRUE",
    };
    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    navigate("/start");
  };

  const replaceSupply = () => {
    const url = "http://localhost:8000/uroflo/user/supply_replace_volume";
    const data = {
      supply_replace_volume: "TRUE",
    };
    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    navigate("/replace/supply/step1");
  };

  return (
    <div className="flex flex-col justify-start items-center w-full h-full gap-y-6">
      <div
        className="flex flex-col rounded-2xl text-slate-200 
                      bg-red-600 w-full h-[162px] px-5 py-4 gap-y-1"
      >
        <div className="text-3xl">
          STATUS <p className="font-bold">CAUTION</p>
        </div>
        <p className="text-xl">SEVERE HEMATURIA FOR &gt; 30 min</p>
      </div>
      <div className="flex flex-row justify-center items-center gap-x-6 w-full">
        <button
          className="flex items-center justify-center text-center rounded-lg font-bold bg-slate-200 text-slate-950 text-2xl w-[45%] h-[90px] px-3 py-1"
          onClick={replaceSupply}
        >
          REPLACE SUPPLY
        </button>
        <button
          className="flex items-center justify-center text-center rounded-lg font-bold bg-slate-200 text-slate-950 text-2xl w-[45%] h-[90px] px-3 py-1"
          onClick={replaceWaste}
        >
          REPLACE WASTE
        </button>
      </div>
      <div className="flex flex-row justify-center items-center gap-x-6 w-full">
        <button
          className="flex items-center justify-center rounded-lg font-bold bg-slate-200 text-slate-950 text-2xl w-[45%] h-[90px] px-3 py-1"
          onClick={mute}
        >
          MUTE
        </button>
        <button
          className="flex items-center justify-center rounded-lg font-bold bg-slate-900 border-2 border-slate-200 text-slate-200 text-2xl w-[45%] h-[90px] px-3 py-1"
          onClick={reset}
        >
          RESET
        </button>
      </div>
      <div className="flex flex-row justify-between items-center w-full">
        <p className="text-2xl text-slate-200">AUTO CONTROL</p>
        <Switch
          colorScheme="green"
          size="lg"
          style={{ transform: "scale(1.2)" }}
          isChecked={auto}
          onChange={handleSwitch}
        />
      </div>
      <div className="flex flex-row justify-between items-center w-full">
        <p className={`text-2xl ${auto ? "text-slate-700" : "text-slate-200"}`}>
          SUPPLY INFLOW
        </p>
        <div className="flex flex-row gap-x-6">
          <button
            className={`h-[50px] w-[50px] rounded-lg ${
              auto ? "bg-slate-700" : "bg-slate-200"
            } flex justify-center items-center`}
            onClick={increaseFlow}
            disabled={auto}
          >
            <TbTriangleFilled className="text-3xl text-slate-950" />
          </button>
          <button
            className={`h-[50px] w-[50px] rounded-lg ${
              auto ? "bg-slate-700" : "bg-slate-200"
            } flex justify-center items-center`}
            onClick={decreaseFlow}
            disabled={auto}
          >
            <TbTriangleInvertedFilled className="text-3xl text-slate-950" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ControlPanel;
