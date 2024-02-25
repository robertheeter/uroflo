import axios from "axios";
import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { FaArrowLeftLong } from "react-icons/fa6";
import { FaArrowRightLong } from "react-icons/fa6";

const ReplaceWasteStep3 = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const resetInitiated = location.state?.resetInitiated;
  const [volume, setVolume] = useState(null);

  const back = () => {
    navigate("/replace/waste/step2", { state: { resetInitiated } });
  };

  const done = () => {
    const url = "http://localhost:8000/interface/waste_replace_volume";
    const data = {
      waste_replace_volume: volume,
    };
    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    if (resetInitiated) {
      navigate("/replace/tubing", { state: { resetInitiated } });
    } else {
      navigate("/home");
    }
  };

  const selectVolume = (vol) => {
    setVolume(parseInt(vol));
  };

  const buttonStyle = (vol) => {
    return volume === vol
      ? "bg-slate-200 text-slate-800"
      : "bg-slate-800 text-slate-200";
  };

  return (
    <div className="w-screen h-screen bg-slate-950 flex flex-col justify-center items-center">
      <div className="w-[50%] h-[60%] bg-slate-800 rounded-2xl flex flex-col justify-between items-center pt-16 pb-10">
        <h1 className="text-5xl text-slate-200 font-bold">Select volume</h1>
        <div className="w-full flex flex-row justify-between items-center px-20">
          <button
            className={`border-slate-200 border-2 w-24 h-20 rounded-lg text-3xl font-bold transition-all duration-150 ${buttonStyle(
              1000
            )}`}
            onClick={() => selectVolume("1000")}
          >
            1 L
          </button>
          <button
            className={`border-slate-200 border-2 w-24 h-20 rounded-lg text-3xl font-bold transition-all duration-150 ${buttonStyle(
              2000
            )}`}
            onClick={() => selectVolume("2000")}
          >
            2 L
          </button>
          <button
            className={`border-slate-200 border-2 w-24 h-20 rounded-lg text-3xl font-bold transition-all duration-150 ${buttonStyle(
              3000
            )}`}
            onClick={() => selectVolume("3000")}
          >
            3 L
          </button>
        </div>
        <div className="w-full flex flex-row justify-between items-center px-10">
          <button
            className="bg-slate-800 border-slate-200 border-2 w-40 h-20 rounded-lg flex justify-center items-center"
            onClick={back}
          >
            <FaArrowLeftLong className="text-6xl text-slate-200" />
          </button>
          <button
            className="bg-green-600 w-40 h-20 rounded-lg flex justify-center items-center text-3xl text-slate-200"
            onClick={done}
            disabled={!volume}
          >
            {resetInitiated ? (
              <FaArrowRightLong className="text-6xl text-slate-950" />
            ) : (
              "Done"
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReplaceWasteStep3;
