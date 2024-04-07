import axios from "axios";
import { useState, useEffect } from "react";
import { Switch } from "@chakra-ui/react";
import { TbTriangleFilled } from "react-icons/tb";
import { TbTriangleInvertedFilled } from "react-icons/tb";
import { useNavigate } from "react-router-dom";

const increaseFlow = () => {
  const url = "http://localhost:8000/interface/inflow_level_increase";
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
  const url = "http://localhost:8000/interface/inflow_level_decrease";
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

const mute = () => {
  const url = "http://localhost:8000/interface/mute";
  const data = {
    mute: "TRUE",
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

const getStatusColor = (statusLevel) => {
  if (statusLevel === "NORMAL") {
    return "bg-green-500";
  } else if (statusLevel === "CAUTION") {
    return "bg-yellow-600";
  } else if (statusLevel === "CRITICAL") {
    return "bg-red-600";
  } else {
    return "bg-green-500";
  }
};

const ControlPanel = () => {
  const navigate = useNavigate();
  const [auto, setAuto] = useState(true);
  const [statusLevel, setStatusLevel] = useState("NORMAL");
  const [statusMessage, setStatusMessage] = useState(
    "System and patient normal."
  );

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/system") // replace with your API endpoint
        .then((response) => setStatusLevel(response.data.status_level)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/system") // replace with your API endpoint
        .then((response) => setStatusMessage(response.data.status_message)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  const handleSwitch = () => {
    setAuto(!auto);
    const data = {};
    const url = "http://localhost:8000/interface/automatic";
    if (!auto) {
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
    const url = "http://localhost:8000/interface/reset";
    const data = {
      reset: "TRUE",
    };
    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    navigate("/landing");
  };

  const click = () => {
    const url = "http://localhost:8000/interface/click";
    const data = {
      click: "TRUE",
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

  const replaceSupply = () => {
    navigate("/replace/supply/step1", { state: { resetInitiated } });
  };

  const replaceWaste = () => {
    navigate("/replace/waste/step1", { state: { resetInitiated } });
  };

  return (
    <div className="flex flex-col justify-start items-center w-full h-full gap-y-6">
      <div
        className={`flex flex-col rounded-2xl text-slate-200 
              ${getStatusColor(
                statusLevel
              )} w-full h-[162px] px-5 py-4 gap-y-1`}
      >
        <div className="text-3xl">
          STATUS <p className="font-bold">{statusLevel}</p>
        </div>
        <p className="text-xl">{statusMessage}</p>
      </div>
      <div className="flex flex-row justify-center items-center gap-x-6 w-full">
        <button
          className="flex items-center justify-center text-center rounded-lg font-bold bg-slate-200 text-slate-950 text-2xl w-[45%] h-[90px] px-3 py-1"
          onClick={() => {
            replaceSupply();
            click();
          }}
        >
          REPLACE SUPPLY
        </button>
        <button
          className="flex items-center justify-center text-center rounded-lg font-bold bg-slate-200 text-slate-950 text-2xl w-[45%] h-[90px] px-3 py-1"
          onClick={() => {
            replaceWaste();
            click();
          }}
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
