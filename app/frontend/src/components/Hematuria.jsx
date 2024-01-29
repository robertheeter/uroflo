import { IoTriangle } from "react-icons/io5";

const convertPercentToSeverity = (percent) => {
  if (percent < 25) {
    return "CLEAR";
  } else if (percent >= 25 && percent < 50) {
    return "MILD";
  } else if (percent >= 50 && percent < 75) {
    return "MODERATE";
  } else {
    return "SEVERE";
  }
};

const setTextSize = (severity) => {
  if (severity === "CLEAR") {
    return "text-3xl";
  } else if (severity === "MILD") {
    return "text-4xl";
  } else if (severity === "MODERATE") {
    return "text-xl";
  } else if (severity === "SEVERE") {
    return "text-3xl";
  } else {
    return "text-base";
  }
};

const Hematuria = () => {
  let percent = 23; // Change this value to a number between 0 and 100
  let severity = convertPercentToSeverity(percent); // Change this value to "CLEAR", "MILD", "MODERATE", or "SEVERE"
  let textSize = setTextSize(severity); // Change this value to "text-3xl", "text-4xl", "text-xl", or "text-3xl"

  return (
    <div
      className="w-[750px] h-[136px] bg-red-300 rounded-xl 
                       flex flex-col justify-center items-center"
    >
      <div className="w-full flex justify-between px-6">
        <div className="text-3xl font-bold text-slate-900">
          HEMATURIA SEVERITY
        </div>
        <div className="text-3xl text-slate-900">{percent}% BLOOD</div>
      </div>
      <div className="w-full flex justify-center gap-5 items-center">
        <div
          className={`w-[125px] h-[54px] font-bold bg-red-50 flex justify-center items-center rounded-lg border-black border-4 ${textSize}`}
        >
          {severity}
        </div>
        <div className="w-3/4 h-20 flex flex-col justify-center items-center relative">
          <div className="w-full h-10 rounded-lg bg-slate-200 border-slate-200 border-[6px] flex flex-row">
            <div className="w-1/4 h-full bg-[#ddc588] text-xl relative flex justify-center items-center rounded-l-md">
              <p className="absolute -bottom-8 font-bold">CLEAR</p>
            </div>
            <div className="w-1/4 h-full bg-[#cf8f70] text-xl relative flex justify-center items-center">
              <p className="absolute -bottom-8 font-bold">MILD</p>
            </div>
            <div className="w-1/4 h-full bg-[#a8372a] text-xl relative flex justify-center items-center">
              <p className="absolute -bottom-8 font-bold">MODERATE</p>
            </div>
            <div className="w-1/4 h-full bg-[#491210] text-xl relative flex justify-center items-center rounded-r-md">
              <p className="absolute -bottom-8 font-bold">SEVERE</p>
            </div>
          </div>

          <div
            className="w-10 h-5/6 absolute transition-all duration-500 -translate-x-1/2 flex flex-col justify-between items-center"
            style={{ left: `${percent}%` }}
          >
            <IoTriangle className="text-3xl text-slate-200 rotate-180" />
            <IoTriangle className="text-3xl text-slate-200" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hematuria;
