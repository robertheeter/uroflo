import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaArrowRightLong } from "react-icons/fa6";

const ReplaceSupplyStep1 = () => {
  const navigate = useNavigate();

  const cancel = () => {
    navigate("/home");
  };

  const next = () => {
    const url = "http://localhost:8000/user/supply_replace_removed";
    const data = {
      supply_replace_count_removed: "TRUE",
    };
    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    navigate("/replace/supply/step2");
  };

  return (
    <div className="w-screen h-screen bg-slate-950 flex flex-col justify-center items-center">
      <div className="w-[50%] h-[60%] bg-slate-800 rounded-2xl flex flex-col justify-between items-center pt-16 pb-10">
        <h1 className="text-5xl text-slate-200 font-bold">Remove supply bag</h1>

        <div className="w-full flex flex-row justify-between items-center px-10">
          <button
            className="bg-slate-800 border-slate-200 border-2 w-40 h-20 rounded-lg text-3xl text-slate-200"
            onClick={cancel}
          >
            Cancel
          </button>
          <button
            className="bg-green-600 w-40 h-20 rounded-lg flex justify-center items-center"
            onClick={next}
          >
            <FaArrowRightLong className="text-6xl" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReplaceSupplyStep1;
