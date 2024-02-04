import { useEffect, useState } from "react";
import axios from "axios";
import { IoTriangle } from "react-icons/io5";

const convertLevelToSeverity = (level) => {
  if (level < 25) {
    return "CLEAR";
  } else if (level >= 25 && level < 50) {
    return "MILD";
  } else if (level >= 50 && level < 75) {
    return "MODERATE";
  } else {
    return "SEVERE";
  }
};

const Hematuria = () => {
  const [percent, setPercent] = useState(0);
  const [level, setLevel] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/interface/api/device") // replace with your API endpoint
        .then((response) => setPercent(response.data.hematuria_percent)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/interface/api/device") // replace with your API endpoint
        .then((response) => setLevel(response.data.hematuria_level)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  let severity = convertLevelToSeverity(level); // Change this value to "CLEAR", "MILD", "MODERATE", or "SEVERE"

  return (
    <div
      className="w-full h-[136px] bg-slate-700 rounded-xl 
                       flex flex-col justify-between items-center px-4 py-3"
    >
      <div className="w-full flex justify-between">
        <div className="text-2xl text-slate-200">HEMATURIA SEVERITY</div>
        <div className="text-2xl text-slate-200">
          {percent.toFixed(1)}% BLOOD
        </div>
      </div>
      <div className="w-full flex justify-between items-center">
        <div
          className={`h-[54px] font-bold bg-slate-200 flex rounded-xl justify-left items-center text-slate-950 text-3xl px-3`}
        >
          {severity}
        </div>
        <div className="w-[480px] h-20 flex flex-col justify-center items-center relative">
          <div className="w-full h-7 rounded-3xl text-slate-200 bg-slate-200 flex flex-row">
            <div className="w-1/4 h-full bg-[#ddc588] text-lg relative flex justify-center items-center rounded-l-2xl">
              <p className="absolute -bottom-7">CLEAR</p>
            </div>
            <div className="w-1/4 h-full bg-[#cf8f70] text-lg relative flex justify-center items-center">
              <p className="absolute -bottom-7">MILD</p>
            </div>
            <div className="w-1/4 h-full bg-[#a8372a] text-lg relative flex justify-center items-center">
              <p className="absolute -bottom-7">MODERATE</p>
            </div>
            <div className="w-1/4 h-full bg-[#491210] text-lg relative flex justify-center items-center rounded-r-2xl">
              <p className="absolute -bottom-7">SEVERE</p>
            </div>
          </div>

          <div
            className="w-10 h-5/6 absolute transition-all duration-500 -translate-x-1/2 flex flex-col justify-between items-center"
            style={{ left: `${level}%` }}
          >
            <IoTriangle className="text-3xl text-slate-200 rotate-180" />
            {/* <IoTriangle className="text-3xl text-slate-200" /> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hematuria;
